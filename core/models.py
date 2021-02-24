from django.contrib.auth.models import AbstractUser
from django.db import models

from Test_BP import settings


class Cities(models.Model):
    municipalityCode = models.TextField()
    municipalityName = models.TextField()
    countyIdentifier = models.IntegerField()
    status = models.TextField()

    def __str__(self):
        return self.municipalityName


class User(AbstractUser):
    SEX_CHOICES = (
        ('F', 'Zena',),
        ('M', 'Muz',),
        ('O', 'Ine',),
    )

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        null=False,
        default='M'
    )
    is_editor = models.BooleanField(default=False, null=False)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    street = models.TextField(null=False)
    date_of_birth = models.DateField(blank=False)

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


class Prisoner(models.Model):
    first_name = models.TextField(max_length=255, blank=False)
    last_name = models.TextField(max_length=255, blank=False)
    date_of_birth = models.DateField(blank=False)
    prisoner_num = models.TextField(max_length=255, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


class MatchPrisoner(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    prisoner_id = models.ForeignKey(Prisoner, on_delete=models.CASCADE)