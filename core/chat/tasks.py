from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from core.chat.models import ChatMessage, ChatActivity, ChatRoom


@shared_task(bind=True, max_retries=3)
def send_email_to_offline_users(self, message_id):
    """
    Task to send email notification to offline users in a chat room

    Args:
        message_id: ID of the ChatMessage that was just created
    """
    try:
        # Get the message
        message = ChatMessage.objects.select_related(
            'chat_room', 'user'
        ).get(id=message_id)

        chat_room = message.chat_room
        sender = message.user

        # Get all active participants in the chat room
        participants = chat_room.participant_info.filter(
            is_active=True
        ).select_related('user').values_list('user', flat=True)

        # Find offline users
        offline_users = ChatActivity.objects.filter(
            user_id__in=participants,
            is_online=False
        ).select_related('user').values('user__email', 'user__first_name', 'user__id')

        if not offline_users.exists():
            return f"No offline users to notify for message {message_id}"

        # Prepare email data
        for activity in offline_users:
            user_email = activity['user__email']
            user_name = activity['user__first_name'] or activity['user__id']

            if not user_email:
                continue

            # Email subject and content
            subject = f"New message from {sender.get_full_name()} in {chat_room.name}"

            context = {
                'user_name': user_name,
                'sender_name': sender.get_full_name(),
                'room_name': chat_room.name,
                'message': message.message,
                'chat_url': f"{settings.BASE_URL}/chat/{chat_room.id}/"
                if hasattr(settings, 'BASE_URL')
                else f"/chat/{chat_room.id}/",
            }

            # Try to render HTML email, fallback to plain text
            try:
                html_message = render_to_string(
                    'email/new_message_notification.html',
                    context
                )
            except:
                html_message = None

            plain_message = f"""
Hello {user_name},

{sender.get_full_name()} sent a new message in {chat_room.name}:

"{message.message}"

Check your chat room for more details.
"""

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                html_message=html_message,
                fail_silently=False,
            )

        return f"Email sent to {offline_users.count()} offline users for message {message_id}"

    except ChatMessage.DoesNotExist:
        return f"Message {message_id} not found"
    except Exception as exc:
        # Retry the task with exponential backoff
        raise self.retry(exc=exc, countdown=5 ** self.request.retries)


@shared_task
def cleanup_offline_status():
    """
    Periodic task to reset offline status after a certain period of inactivity
    This ensures that the online status is eventually reset to offline
    """
    from django.utils import timezone
    from datetime import timedelta

    # After 30 minutes of no activity, mark as offline
    threshold_time = timezone.now() - timedelta(minutes=30)

    offline_count = ChatActivity.objects.filter(
        is_online=True,
        last_active__lt=threshold_time
    ).update(is_online=False, current_room=None)

    return f"Cleaned up {offline_count} users' offline status"
