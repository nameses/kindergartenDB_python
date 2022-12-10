from django.db import models


class Kindergarten(models.Model):
    Name = models.CharField(max_length=30)
    Address = models.CharField(max_length=30)
    WorkDaysInWeek = models.IntegerField()
    ChildrenNumber = models.IntegerField()
    NominalSum = models.IntegerField()


class KindergartenGroup(models.Model):
    KindergartenID = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    ChildrenNumber = models.IntegerField()
    Name = models.CharField(max_length=30)


class Child(models.Model):
    GroupID = models.ForeignKey(KindergartenGroup, on_delete=models.CASCADE)
    KindergartenID = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    Surname = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Patronymic = models.CharField(max_length=30)
    Birthday = models.DateTimeField('birthday')


class Parent(models.Model):
    Surname = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Patronymic = models.CharField(max_length=30)
    Phone = models.CharField(max_length=13)
    Comments = models.CharField(max_length=60)


class Family(models.Model):
    ChildID = models.ForeignKey(Child, on_delete=models.CASCADE)
    ParentID = models.ForeignKey(Parent, on_delete=models.CASCADE)


class Month(models.Model):
    MonthAndYear = models.DateTimeField('monthAndYear')
    WorkDaysNumber = models.IntegerField()


class Attendance(models.Model):
    MonthID = models.ForeignKey(Month, on_delete=models.CASCADE)
    ChildID = models.ForeignKey(Child, on_delete=models.CASCADE)
    DaysAttended = models.IntegerField()
    FinalSum = models.IntegerField()
    isPaid = models.BooleanField
