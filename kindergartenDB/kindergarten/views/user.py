from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authorization import decorators
from .. import forms
from .. import models


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


def group_list(request):
    return render(
        request,
        'kindergarten/group_list.html',
        {
            'groups': models.KindergartenGroup.objects.all()
        }
    )


@decorators.post_method_only
@decorators.authenticated_only
def parent_delete_child(request, child_id):
    if (child := get_object_or_404(models.Child, id=child_id)).parent == request.user:
        child.delete()
    return HttpResponseRedirect('/profile/')


@decorators.authenticated_only
def parent_add_child(request):
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

        child = models.Child(**form_data)
        child.parent = request.user
        child.save()

        return HttpResponseRedirect('/profile/')

    form = forms.ChildForm()

    return render(
        request,
        'kindergarten/child.html',
        {
            'form': form,
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


@decorators.post_method_only
@decorators.authenticated_only
def child_pay(request, payment_id):
    payment = get_object_or_404(models.Attendance, id=payment_id)
    if payment.child.parent == request.user:
        payment.is_paid = 1
        payment.save()
        return HttpResponseRedirect(f'/child/{payment.child.id}/payments')
    else:
        return HttpResponseRedirect('/profile/')
