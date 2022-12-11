from django.db import models


class Kindergarten(models.Model):
    Name = models.CharField(max_length=30)
    Address = models.CharField(max_length=30)
    WorkDaysInWeek = models.IntegerField()
    NominalSum = models.IntegerField()

    @property
    def ChildrenNumber(self):
        return

    def __str__(self):
        return self.Name


class KindergartenGroup(models.Model):
    KindergartenID = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    Name = models.CharField(max_length=30)

    @property
    def ChildrenNumber(self):
        return

    def __str__(self):
        return self.Name


class Child(models.Model):
    GroupID = models.ForeignKey(KindergartenGroup, on_delete=models.CASCADE)
    KindergartenID = models.ForeignKey(Kindergarten, on_delete=models.CASCADE)
    Surname = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Patronymic = models.CharField(max_length=30)
    Birthday = models.DateTimeField('birthday')

    def __str__(self):
        return f'{self.Surname} {self.Name} {self.Patronymic}'


class Parent(models.Model):
    Surname = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Patronymic = models.CharField(max_length=30)
    Phone = models.CharField(max_length=13)
    Comments = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.Surname} {self.Name} {self.Patronymic}'


class Family(models.Model):
    ChildID = models.ForeignKey(Child, on_delete=models.CASCADE)
    ParentID = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return self.ParentID.Surname


class Month(models.Model):
    MonthAndYear = models.DateTimeField('monthAndYear')
    WorkDaysNumber = models.IntegerField()

    def __str__(self):
        return f'{self.MonthAndYear.month}.{self.MonthAndYear.year}'


class Attendance(models.Model):
    MonthID = models.ForeignKey(Month, on_delete=models.CASCADE)
    ChildID = models.ForeignKey(Child, on_delete=models.CASCADE)
    DaysAttended = models.IntegerField()
    isPaid = models.BooleanField(default=False)

    @property
    def FilalSum(self):
        return

    def __str__(self):
        return f'days:{self.DaysAttended}/{self.MonthID.WorkDaysNumber}'
