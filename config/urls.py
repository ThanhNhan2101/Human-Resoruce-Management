from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from config.forms import LoginForm

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication URLs
    path('', LoginView.as_view(template_name='auth/login.html',
         authentication_form=LoginForm), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # App URLs
    path('dashboard/', include('core.employees.urls')),
    path('leaves/', include('core.leaves.urls')),
    path('attendance/', include('core.attendance.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
