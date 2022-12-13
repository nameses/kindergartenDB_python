from django import forms

from . import models


class KindergartenForm(forms.ModelForm):
    class Meta:
        model = models.Kindergarten
        fields = ['name', 'address', 'work_day_in_week', 'month_price']


class KindergartenGroupForm(forms.ModelForm):
    class Meta:
        model = models.KindergartenGroup
        fields = ['name', 'kindergarten']


class ChildForm(forms.ModelForm):
    class Meta:
        model = models.Child
        fields = ['group', 'birthday', 'surname', 'name', 'patronymic']
