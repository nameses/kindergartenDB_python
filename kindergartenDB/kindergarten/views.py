from django.shortcuts import render

from kindergartenDB.authorization.decorators import staff_only
from kindergartenDB.kindergarten.models import Kindergarten


def index(request):
    return render(request, 'kindergarten/index.html')


@staff_only
def kindergarten_list(request):
    return render(
        request,
        'kindergarten/kindergarten_list.html',
        {
            'kindergartens': Kindergarten.objects.all()
        }
    )
