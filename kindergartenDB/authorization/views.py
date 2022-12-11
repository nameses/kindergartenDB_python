from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import SignUpForm


def user_signup(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            form_data = form.cleaned_data

            if User.objects.filter(username=form_data['username']).exists():
                return render(
                    request,
                    'authorization/signup.html', {
                        'form': form,
                        'error': 'Username already used'
                    }
                )
            if form_data['password'] != form_data['password_confirm']:
                return render(
                    request,
                    'authorization/signup.html',
                    {
                        'form': form,
                        'error': 'Passwords are not the same'
                    }
                )

            user = User.objects.create_user(
                username=form_data['username'],
                first_name=form_data['first_name'],
                last_name=form_data['last_name'],
                password=form_data['password'],
            )

            login(request, user)

            return HttpResponseRedirect('/')

        return render(
            request,
            'authorization/signup.html',
            {
                'form': form,
                'error': 'Invalid form'
            }
        )

    form = SignUpForm()

    return render(
        request,
        'authorization/signup.html',
        {
            'form': form
        }
    )
