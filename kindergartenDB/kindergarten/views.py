from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from . import models
from .forms import KindergartenForm, KindergartenGroupForm, ChildForm, AttendanceForm, MonthForm
from .models import Kindergarten, KindergartenGroup, Child, Attendance, Month


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


@decorators.staff_only
def kindergarten_list_payments(request):
    pass


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


@decorators.staff_only
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


@decorators.authenticated_only
def payments_by_child_list(request, child_id):
    child = models.Child.objects.get(id=child_id)
    return render(
        request,
        'kindergarten/payments_by_child_list.html',
        {
            'child': child,
            'payments': models.Attendance.objects.filter(child=child)
        }
    )


@decorators.staff_only
def month_list(request):
    return render(
        request,
        'kindergarten/month_list.html',
        {
            'months': Month.objects.all()
        }
    )


@decorators.staff_only
def add_month(request):
    if request.method == 'POST':
        form = MonthForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/month.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data
        month = form_data['month']
        year = form_data['year']
        if models.Month.objects.filter(month=month, year=year).exists():
            return render(
                request,
                'kindergarten/month.html',
                {
                    'form': form,
                    'error': 'Month already exists.'
                }
            )
        Month(**form_data).save()
        return HttpResponseRedirect('/months/')

    form = MonthForm()

    return render(
        request,
        'kindergarten/month.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def month_view(request, month_id=None):
    month = get_object_or_404(Month, id=month_id)

    if request.method == 'POST':
        form = MonthForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/month.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        month.month = form_data['month']
        month.year = form_data['year']

        month.work_day_count = form_data['work_day_count']

        month.save()

        return HttpResponseRedirect('/months/')

    form = MonthForm(instance=month)

    return render(
        request,
        'kindergarten/month.html',
        {
            'form': form
        }
    )


@decorators.post_method_only
@decorators.staff_only
def delete_month(request, month_id):
    month = get_object_or_404(Month, id=month_id)
    month.delete()
    return HttpResponseRedirect('/months/')


@decorators.staff_only
def child_add_payment(request, child_id):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/add_payment.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        child = get_object_or_404(Child, id=child_id)

        Attendance(
            child=child,
            month=form_data['month'],
            days_attended=form_data['days_attended']
        ).save()

        return HttpResponseRedirect(f'/group/{child.group.id}/children/')

    form = AttendanceForm()

    return render(
        request,
        'kindergarten/add_payment.html',
        {
            'form': form
        }
    )


@decorators.post_method_only
@decorators.authenticated_only
def child_pay(request, payment_id):
    payment = get_object_or_404(Attendance, id=payment_id)
    if payment.child.parent == request.user:
        payment.is_paid = 1
        payment.save()
        return HttpResponseRedirect(f'/child/{payment.child.id}/payments')
    else:
        return HttpResponseRedirect('/profile/')
