from django import forms


class KindergartenForm(forms.Form):
    name = forms.CharField()
    address = forms.CharField()
    work_day_in_week = forms.IntegerField()
    month_price = forms.IntegerField()
