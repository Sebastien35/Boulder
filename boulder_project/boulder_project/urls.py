
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home_view, name='home'),
    path('upload/',views.upload_media,name='upload_media'),
   
]

if settings.DEBUG:
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
