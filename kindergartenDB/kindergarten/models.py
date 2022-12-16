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

    @property
    def sum_to_pay(self):
        return sum((
            attendance.final_sum
            for child in Child.objects.filter(parent=self.user)
            for attendance in Attendance.objects.filter(child=child, is_paid=False)
        ))


class Kindergarten(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    work_day_in_week = models.IntegerField()
    month_price = models.IntegerField()

    @property
    def children_count(self):
        return sum((
            kindergarten.children_count for kindergarten in
            KindergartenGroup.objects.filter(kindergarten=self.id)
        ))

    def __str__(self):
        return self.name


class KindergartenGroup(models.Model):
    kindergarten = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    @property
    def children_count(self):
        return Child.objects.filter(group=self.id).count()

    @property
    def kindergarten_name(self):
        return self.kindergarten.name

    def __str__(self):
        return self.name


class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(KindergartenGroup, on_delete=models.CASCADE)
    birthday = models.DateTimeField('birthday')
    surname = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'

    @property
    def get_parent_name(self):
        return str(UserAdditionInfo.objects.get(user=self.parent))

    @property
    def birthday_str(self):
        return f'{self.birthday.day}.{self.birthday.month}.{self.birthday.year}'


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
        return self.child.group.kindergarten.month_price * self.days_attended / self.month.work_day_count

    def __str__(self):
        return f'days:{self.days_attended}/{self.month.work_day_count}'
