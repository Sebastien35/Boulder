
from django.contrib import admin
from django.urls import path
from .views import login_view, register_view, home_view, upload_media, logout_view
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_view, name='login'),
    path('register/', register_view, name='register'),
    path('', home_view, name='home'),
    path('upload/',upload_media,name='upload_media'),
    path('logout/',logout_view, name='logout')
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
