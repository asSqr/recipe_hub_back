from django.db import models
from django.utils import timezone
import uuid

class MyUUIDModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class MRepository(MyUUIDModel):
  id_fork_from = models.CharField(max_length=36, null=True, blank=True)
  name = models.CharField(max_length=8192)
  recipe = models.CharField(max_length=16384)
  id_author = models.CharField(max_length=36)
  create_date = models.DateTimeField(default=timezone.now)
  update_date = models.DateTimeField(default=timezone.now)

class MUser(MyUUIDModel):
  name = models.CharField(max_length=8192)
  password = models.CharField(max_length=8192)
  email = models.EmailField()
  create_date = models.DateTimeField(default=timezone.now)
  update_date = models.DateTimeField(default=timezone.now)
