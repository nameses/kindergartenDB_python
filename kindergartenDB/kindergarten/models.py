from django.contrib.auth.models import User
from django.db import models


class Kindergarten(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    work_day_in_week = models.IntegerField()
    month_price = models.IntegerField()

    @property
    def children_count(self):
        return

    def __str__(self):
        return self.name


class KindergartenGroup(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    @property
    def children_count(self):
        return

    def __str__(self):
        return self.name


class UserAdditionInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, default=None, blank=True)
    comments = models.CharField(max_length=60, default=None, blank=True)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(KindergartenGroup, on_delete=models.CASCADE)
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    birthday = models.DateTimeField('birthday')
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


class Month(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    work_day_count = models.IntegerField()

    def __str__(self):
        return f'{self.month}.{self.year}'


class Attendance(models.Model):
    month = models.ForeignKey(Month, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    days_attended = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    @property
    def final_sum(self):
        return

    def __str__(self):
        return f'days:{self.days_attended}/{self.month.work_day_number}'
