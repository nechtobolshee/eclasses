from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.get_full_name()
