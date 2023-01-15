from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True)
