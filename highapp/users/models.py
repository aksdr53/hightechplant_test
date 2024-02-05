import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class EmailConfirmation(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)    
