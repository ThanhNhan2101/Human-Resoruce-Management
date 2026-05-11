from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.chat.models import ChatRoom, ChatParticipant


class Command(BaseCommand):
    help = 'Seed initial chat rooms'

    def handle(self, *args, **options):
        # Get or create superuser
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            self.stdout.write(self.style.ERROR(
                'No superuser found. Please create one first.'))
            return

        # Create chat rooms
        rooms_data = [
            {
                'name': 'General',
                'description': 'General discussion for all employees',
                'is_private': False,
            },
            {
                'name': 'Announcements',
                'description': 'Important announcements and updates',
                'is_private': False,
            },
            {
                'name': 'HR Support',
                'description': 'HR support and queries',
                'is_private': False,
            },
            {
                'name': 'Management',
                'description': 'Management discussions (private)',
                'is_private': True,
            },
        ]

        for room_data in rooms_data:
            room, created = ChatRoom.objects.get_or_create(
                name=room_data['name'],
                defaults={
                    'description': room_data['description'],
                    'is_private': room_data['is_private'],
                    'created_by': superuser,
                }
            )

            if created:
                # Add superuser as participant
                ChatParticipant.objects.get_or_create(
                    chat_room=room,
                    user=superuser,
                    defaults={'is_active': True}
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created chat room: {room.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Chat room already exists: {room.name}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully seeded chat rooms'))
