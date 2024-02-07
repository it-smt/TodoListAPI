from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    auth_token = models.CharField(max_length=256)
