from django.http import HttpResponseRedirect
from django.shortcuts import render

from authorization import decorators
from . import models
from .forms import CreateKindergartenForm
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

    return HttpResponseRedirect('kindergartens/')


@decorators.staff_only
def add_kindergarten(request):
    if request.method == 'POST':
        form = CreateKindergartenForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                'kindergarten/add_kindergarten.html',
                {
                    'form': form,
                    'error': 'Invalid form'
                }
            )

        form_data = form.cleaned_data

        Kindergarten(**form_data).save()

        return HttpResponseRedirect('/kindergartens/')

    form = CreateKindergartenForm()

    return render(
        request,
        'kindergarten/add_kindergarten.html',
        {
            'form': form,
        }
    )
