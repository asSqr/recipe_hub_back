from django.db import models
from django.utils import timezone
import os
import uuid

class MyUUIDModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

# https://stackoverflow.com/questions/15140942/django-imagefield-change-file-name-on-upload/15141228
def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class MRepository(MyUUIDModel):
  id_fork_from = models.CharField(max_length=36, null=True, blank=True)
  id_fork_to_list = models.CharField(max_length=8192, default="{}")
  title = models.CharField(max_length=8192)
  name = models.CharField(max_length=8192)
  recipe = models.CharField(max_length=16384)
  id_author = models.CharField(max_length=36)
  author_photo_url = models.CharField(max_length=8192, default="")
  genre = models.CharField(max_length=8192)
  thumbnail = models.ImageField(upload_to=path_and_rename, null=True, blank=True)
  create_date = models.DateTimeField(default=timezone.now)
  update_date = models.DateTimeField(default=timezone.now)

class MUser(MyUUIDModel):
  name = models.CharField(max_length=8192)
  password = models.CharField(max_length=8192)
  email = models.EmailField()
  create_date = models.DateTimeField(default=timezone.now)
  update_date = models.DateTimeField(default=timezone.now)
