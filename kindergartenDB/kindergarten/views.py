from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from . import models
from .forms import KindergartenForm
from .models import Kindergarten


def index(request):
    return render(request, 'kindergarten/index.html')


@decorators.staff_only
def kindergarten_list(request):
    return render(
        request,
        'kindergarten/kindergarten_list.html',
        {
            'kindergartens': models.Kindergarten.objects.all()
        }
    )


@decorators.post_method_only
@decorators.staff_only
def delete_kindergarten(request, kindergarten_id):
    if (kindergarten := models.Kindergarten.objects.get(id=kindergarten_id)) is not None:
        kindergarten.delete()

    return HttpResponseRedirect('/kindergartens/')


@decorators.staff_only
def add_kindergarten(request):
    if request.method == 'POST':
        form = KindergartenForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/kindergarten.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        Kindergarten(**form_data).save()

        return HttpResponseRedirect('/kindergartens/')

    form = KindergartenForm()

    return render(
        request,
        'kindergarten/kindergarten.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def kindergarten_view(request, kindergarten_id):
    kindergarten = get_object_or_404(Kindergarten, id=kindergarten_id)

    if request.method == 'POST':
        form = KindergartenForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/kindergarten.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        kindergarten.name = form_data['name']
        kindergarten.address = form_data['address']
        kindergarten.work_day_in_week = form_data['work_day_in_week']
        kindergarten.month_price = form_data['month_price']

        kindergarten.save()

        return HttpResponseRedirect('/kindergartens/')

    form = KindergartenForm(
        initial={
            'name': kindergarten.name,
            'address': kindergarten.address,
            'work_day_in_week': kindergarten.work_day_in_week,
            'month_price': kindergarten.month_price,
        }
    )

    return render(
        request,
        'kindergarten/kindergarten.html',
        {
            'form': form
        }
    )
