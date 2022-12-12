from django.http import HttpResponseRedirect
from django.shortcuts import render

from authorization import decorators
from . import models


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


@decorators.delete_method_only
@decorators.staff_only
def delete_kindergarten(request, kindergarten_id):
    if (kindergarten := models.Kindergarten.objects.get(id=kindergarten_id)).exists():
        kindergarten.delete()

    return kindergarten_list(request)

