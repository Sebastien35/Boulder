from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User


fs=FileSystemStorage(location='media/')

class Media(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='', storage=fs)
    date=models.DateField(auto_now=True)
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_posts', default=None, null=True, blank=True)
  
    
    
    

    class Meta:
        db_table = 'boulder_project_media'

    def __str__(self):
        return self.title


class text_post(models.Model):
    content=models.CharField(max_length=5000)
    date=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.content