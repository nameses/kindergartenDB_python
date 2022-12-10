from django.db import models


class KindergartenGroup(models.Model):
    ...


class Child(models.Model):
    Surname = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Patronymic = models.CharField(max_length=30)
    Birthday = models.DateTimeField('birthday')


class Attendance(models.Model):
    ...
