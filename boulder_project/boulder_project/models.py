from django.db import models
from django.core.files.storage import FileSystemStorage


fs=FileSystemStorage(location='media/')
class Media(models.Model):
    title = models.CharField(max_length=255)
    file = models.ImageField(upload_to='', storage=fs)
    

    class Meta:
        db_table = 'boulder_project_media'

    def __str__(self):
        return self.title


class text_post(models.Model):
    content=models.CharField(max_length=5000)
    created_at=models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.content