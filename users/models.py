from django.db import models


class UserModel(models.Model):
    col = models.CharField(max_length=15)
