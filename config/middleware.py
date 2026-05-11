# from django.utils.deprecation import MiddlewareMixin
# from django.shortcuts import redirect
# from django.urls import resolve
# from django.http import HttpResponse


# class RoleBasedDashboardMiddleware(MiddlewareMixin):
#     """
#     Middleware to redirect non-superusers to chat and superusers to dashboard
#     """

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Skip for non-authenticated users
#         if not request.user.is_authenticated:
#             return None

#         # Skip for API endpoints and admin
#         path = request.path
#         if path.startswith('/admin') or path.startswith('/api'):
#             return None

#         # If accessing the root dashboard redirect
#         if path == '/chat/':
#             if request.user.is_superuser:
#                 # Superuser should go to employee dashboard
#                 return redirect('employees:dashboard')
#             else:
#                 # Non-superuser should go to chat list
#                 return redirect('chat:chat_list')

#         return None
