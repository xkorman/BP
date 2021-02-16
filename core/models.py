from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_editor = models.BooleanField(default=False, null=False)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class Department(models.Model):
    name = models.CharField(blank=False, max_length=255)
    phone = models.TextField()
    email = models.TextField()

class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField()