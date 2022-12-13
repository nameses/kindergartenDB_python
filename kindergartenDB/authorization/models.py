from django.contrib.auth.models import User
from django.db import models


class UserAdditionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, default=None, blank=True)
    comments = models.CharField(max_length=60, default=None, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
