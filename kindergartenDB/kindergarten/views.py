from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from . import models
from .forms import KindergartenForm, KindergartenGroupForm, ChildForm
from .models import Kindergarten, KindergartenGroup, Child


def index(request):
    return render(request, 'kindergarten/index.html')


def about(request):
    return render(request, 'authorization/about.html')


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


def children_by_group_list(request, group_id):
    return render(
        request,
        'kindergarten/children_by_group_list.html',
        {
            'children': models.Child.objects.filter(group=group_id),
            'group': models.KindergartenGroup.objects.get(id=group_id)
        }
    )


@decorators.post_method_only
@decorators.staff_only
def delete_child(request, group_id, child_id):
    if (child := models.Child.objects.get(id=child_id)) is not None:
        child.delete()
    return HttpResponseRedirect('/group/' + str(group_id) + '/children')


@decorators.post_method_only
@decorators.authenticated_only
def parent_delete_child(request, child_id):
    if (child := get_object_or_404(Child, id=child_id)).parent == request.user:
        child.delete()
    return HttpResponseRedirect('/profile/')


@decorators.authenticated_only
def parent_add_child(request):
    if request.method == 'POST':
        form = ChildForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/child.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        child = Child(**form_data)
        child.parent = request.user
        child.save()

        return HttpResponseRedirect('/profile/')

    form = ChildForm()

    return render(
        request,
        'kindergarten/child.html',
        {
            'form': form,
        }
    )

@decorators.staff_only
def child_view(request, child_id=None):
    child = get_object_or_404(Child, id=child_id)

    if request.method == 'POST':
        form = ChildForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/child.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        # child.parent = form_data['parent']
        child.group = form_data['group']
        child.birthday = form_data['birthday']
        child.surname = form_data['surname']
        child.name = form_data['name']
        child.patronymic = form_data['patronymic']

        child.save()

        return HttpResponseRedirect('/profile/')

    form = ChildForm(instance=child)

    return render(
        request,
        'kindergarten/child.html',
        {
            'form': form
        }
    )