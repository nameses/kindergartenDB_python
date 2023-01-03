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

        widgets = {
            'birthday': forms.DateInput(
                format='%d-%m-%Y',
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date',
                       'style': 'width:200px; display: inline'
                       },
            ),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = models.Attendance
        fields = ['month', 'days_attended']


class AttendanceMonthForm(forms.ModelForm):
    class Meta:
        model = models.Attendance
        fields = ['month']


class MonthForm(forms.ModelForm):
    class Meta:
        model = models.Month
        fields = ['month', 'year', 'work_day_count']
