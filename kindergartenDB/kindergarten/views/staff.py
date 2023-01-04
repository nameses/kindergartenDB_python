from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from .. import forms
from .. import models


@decorators.post_method_only
@decorators.staff_only
def delete_kindergarten(request, kindergarten_id):
    if (kindergarten := models.Kindergarten.objects.get(id=kindergarten_id)) is not None:
        kindergarten.delete()

    return HttpResponseRedirect('/kindergartens/')


@decorators.staff_only
def add_kindergarten(request):
    if request.method == 'POST':
        form = forms.KindergartenForm(request.POST)

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

        models.Kindergarten(**form_data).save()

        return HttpResponseRedirect('/kindergartens/')

    form = forms.KindergartenForm()

    return render(
        request,
        'kindergarten/kindergarten.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def kindergarten_view(request, kindergarten_id):
    kindergarten = get_object_or_404(models.Kindergarten, id=kindergarten_id)

    if request.method == 'POST':
        form = forms.KindergartenForm(request.POST)

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

    form = forms.KindergartenForm(instance=kindergarten)

    return render(
        request,
        'kindergarten/kindergarten.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def kindergarten_list_payments(request, kindergarten_id):
    kindergarten = get_object_or_404(models.Kindergarten, id=kindergarten_id)

    return render(
        request,
        'kindergarten/kindergarten_list_payments.html',
        {
            'kindergarten': kindergarten,
        }
    )


@decorators.staff_only
def payments_by_kindergarten_month(request, kindergarten_id, month_id):
    kindergarten = get_object_or_404(models.Kindergarten, id=kindergarten_id)
    groups = models.KindergartenGroup.objects.filter(kindergarten_id=kindergarten_id)
    children = models.Child.objects.filter(group__in=groups)
    child_to_attendance = {}
    for child in children:
        if models.Attendance.objects.filter(child=child, month_id=month_id, is_paid=False).exists():
            child_to_attendance[child] = models.Attendance.objects.get(child=child, month_id=month_id, is_paid=False)
    return render(
        request,
        'kindergarten/payments_by_children_kindergarten_month_list.html',
        {
            'kindergarten': kindergarten,
            'child_to_attendance': child_to_attendance,
            'month': get_object_or_404(models.Month, id=month_id)
        }
    )


@decorators.post_method_only
@decorators.staff_only
def delete_group(request, group_id):
    get_object_or_404(models.KindergartenGroup, id=group_id).delete()

    return HttpResponseRedirect('/groups/')


@decorators.staff_only
def add_group(request):
    if request.method == 'POST':
        form = forms.KindergartenGroupForm(request.POST)

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

        models.KindergartenGroup(**form_data).save()

        return HttpResponseRedirect('/groups/')

    form = forms.KindergartenGroupForm()

    return render(
        request,
        'kindergarten/group.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def group_view(request, group_id=None):
    group = get_object_or_404(models.KindergartenGroup, id=group_id)

    if request.method == 'POST':
        form = forms.KindergartenGroupForm(request.POST)

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

    form = forms.KindergartenGroupForm(instance=group)

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
    get_object_or_404(models.Child, id=child_id).delete()
    return HttpResponseRedirect(f'/group/{group_id}/children')


@decorators.staff_only
def child_view(request, child_id):
    child = get_object_or_404(models.Child, id=child_id)

    if request.method == 'POST':
        form = forms.ChildForm(request.POST)

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

    form = forms.ChildForm(instance=child)

    return render(
        request,
        'kindergarten/child.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def month_list(request):
    return render(
        request,
        'kindergarten/month_list.html',
        {
            'months': models.Month.objects.all()
        }
    )


@decorators.staff_only
def add_month(request):
    if request.method == 'POST':
        form = forms.MonthForm(request.POST)

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
        models.Month(**form_data).save()
        return HttpResponseRedirect('/months/')

    form = forms.MonthForm()

    return render(
        request,
        'kindergarten/month.html',
        {
            'form': form,
        }
    )


@decorators.staff_only
def month_view(request, month_id=None):
    month = get_object_or_404(models.Month, id=month_id)

    if request.method == 'POST':
        form = forms.MonthForm(request.POST)

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

    form = forms.MonthForm(instance=month)

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
    month = get_object_or_404(models.Month, id=month_id)
    month.delete()
    return HttpResponseRedirect('/months/')


@decorators.staff_only
def child_add_payment(request, child_id):
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)

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

        child = get_object_or_404(models.Child, id=child_id)

        if models.Attendance.objects.filter(child=child, month=form_data['month']).exists():
            return render(
                request,
                'kindergarten/add_payment.html',
                {
                    'form': form,
                    'error': 'Attendance to this month already exists'
                }
            )

        if form_data['month'].work_day_count < form_data['days_attended']:
            return render(
                request,
                'kindergarten/add_payment.html',
                {
                    'form': form,
                    'error': 'Attended days more than work day count'
                }
            )

        models.Attendance(
            child=child,
            month=form_data['month'],
            days_attended=form_data['days_attended']
        ).save()

        return HttpResponseRedirect(f'/group/{child.group.id}/children/')

    form = forms.AttendanceForm()

    return render(
        request,
        'kindergarten/add_payment.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def child_edit_payment_group(request, child_id, month_id):
    payment = get_object_or_404(models.Attendance,
                                child_id=child_id,
                                month_id=month_id)

    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/edit_payment.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        child = get_object_or_404(models.Child, id=child_id)

        if form_data['month'].work_day_count < form_data['days_attended']:
            return render(
                request,
                'kindergarten/edit_payment.html',
                {
                    'form': form,
                    'error': 'Attended days more than work day count'
                }
            )

        get_object_or_404(models.Attendance, child=child, month=form_data['month']) \
            .delete()

        models.Attendance(
            child=child,
            month=form_data['month'],
            days_attended=form_data['days_attended']
        ).save()

        return HttpResponseRedirect(f'/group/{child.group.id}/children/month/{month_id}/')

    form = forms.AttendanceForm(instance=payment)

    return render(
        request,
        'kindergarten/edit_payment.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def child_edit_payment_kindergarten(request, child_id, month_id):
    payment = get_object_or_404(models.Attendance,
                                child_id=child_id,
                                month_id=month_id)

    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/edit_payment.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        child = get_object_or_404(models.Child, id=child_id)

        if form_data['month'].work_day_count < form_data['days_attended']:
            return render(
                request,
                'kindergarten/edit_payment.html',
                {
                    'form': form,
                    'error': 'Attended days more than work day count'
                }
            )

        get_object_or_404(models.Attendance, child=child, month=form_data['month']) \
            .delete()

        models.Attendance(
            child=child,
            month=form_data['month'],
            days_attended=form_data['days_attended']
        ).save()

        return HttpResponseRedirect(f'/kindergarten/{child.group.kindergarten.id}/payments/month/{month_id}')

    form = forms.AttendanceForm(instance=payment)

    return render(
        request,
        'kindergarten/edit_payment.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def child_add_payment_multiple(request, group_id):
    if request.method == 'POST':
        form = forms.AttendanceMonthForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/add_multiple_payments.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        group = get_object_or_404(models.KindergartenGroup, id=group_id)
        children = models.Child.objects.filter(group=group)

        days_attended = form_data['month'].work_day_count
        month = form_data['month']
        for child in children:
            if not models.Attendance.objects.filter(child=child, month=month).exists():
                models.Attendance(
                    child=child,
                    month=month,
                    days_attended=days_attended
                ).save()

        return HttpResponseRedirect(f'/group/{group_id}/children/month/{month.id}/')

    form = forms.AttendanceMonthForm()

    return render(
        request,
        'kindergarten/add_multiple_payments.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def child_show_payment_multiple(request, group_id):
    if request.method == 'POST':
        form = forms.AttendanceMonthForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/add_multiple_payments.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        group = get_object_or_404(models.KindergartenGroup, id=group_id)
        children = models.Child.objects.filter(group=group)

        ifAllExists = True
        for child in children:
            if not models.Attendance.objects.filter(child=child, month=form_data['month']).exists():
                ifAllExists = False

        if not ifAllExists:
            return render(
                request,
                'kindergarten/add_multiple_payments.html',
                {
                    'form': form,
                    'error': 'Not all children have payments!'
                }
            )

        month = form_data['month']
        return HttpResponseRedirect(f'/group/{group_id}/children/month/{month.id}/')

    form = forms.AttendanceMonthForm()

    return render(
        request,
        'kindergarten/add_multiple_payments.html',
        {
            'form': form
        }
    )


@decorators.staff_only
def children_by_group_by_month_list(request, group_id, month_id):
    children = models.Child.objects.filter(group=group_id)
    month = models.Month.objects.get(id=month_id)
    child_to_attendance = {}
    for child in children:
        child_to_attendance[child] = models.Attendance.objects.get(child=child, month=month)

    return render(
        request,
        'kindergarten/payments_by_children_group_month_list.html',
        {
            'child_to_attendance': child_to_attendance,
            'group': models.KindergartenGroup.objects.get(id=group_id),
            'month': month,
        }
    )
