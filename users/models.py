from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=128)
    profile_image_url = models.URLField()
