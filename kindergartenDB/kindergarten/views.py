from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from . import models
from .forms import KindergartenForm, KindergartenGroupForm
from .models import Kindergarten, KindergartenGroup


def index(request):
    return render(request, 'kindergarten/index.html')


def about(request):
    return render(request, 'authorization/about.html')


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

    form = KindergartenForm(instance=kindergarten)

    return render(
        request,
        'kindergarten/kindergarten.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def group_list(request):
    return render(
        request,
        'kindergarten/group_list.html',
        {
            'groups': models.KindergartenGroup.objects.all()
        }
    )


@decorators.post_method_only
@decorators.staff_only
def delete_group(request, group_id):
    if (kindergarten := models.KindergartenGroup.objects.get(id=group_id)) is not None:
        kindergarten.delete()

    return HttpResponseRedirect('/groups/')


@decorators.staff_only
def add_group(request):
    if request.method == 'POST':
        form = KindergartenGroupForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/group.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        KindergartenGroup(**form_data).save()

        return HttpResponseRedirect('/groups/')

    form = KindergartenGroupForm()

    return render(
        request,
        'kindergarten/group.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def group_view(request, group_id=None):
    group = get_object_or_404(KindergartenGroup, id=group_id)

    if request.method == 'POST':
        form = KindergartenGroupForm(request.POST)

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

        group.name = form_data['name']
        group.kindergarten = form_data['kindergarten']

        group.save()

        return HttpResponseRedirect('/groups/')

    form = KindergartenGroupForm(instance=group)

    return render(
        request,
        'kindergarten/group.html',
        {
            'form': form
        }
    )
