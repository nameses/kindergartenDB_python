from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from kindergarten.models import UserAdditionInfo
from .decorators import authenticated_only
from .forms import SignUpForm, LoginForm
from kindergarten.models import Child


def profile(request, user_id=None):
    if user_id is None:
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/signup/')

        return render(
            request,
            'authorization/profile.html',
            {
                'user': (user := request.user),
                'UAI': UserAdditionInfo.objects.get(user=user),
                'children': Child.objects.filter(parent=user),
                'is_parent': True,
            }
        )

    return render(
        request,
        'authorization/profile.html',
        {
            'user': (user := get_object_or_404(User, id=user_id)),
            'UAI': UserAdditionInfo.objects.get(user=user),
            'children': Child.objects.filter(parent=user),
            'is_parent': False
        }
    )


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
                password=form_data['password'],
            )

            UserAdditionInfo(
                user=user,
                surname=form_data['surname'],
                name=form_data['name'],
                patronymic=form_data['patronymic'],
                phone=form_data['phone'],
                comments=form_data['comments'],
            ).save()

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


def user_login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():

            form_data = form.cleaned_data

            user = authenticate(username=form_data['username'], password=form_data['password'])
            if user is None:
                return render(
                    request,
                    'authorization/login.html', {
                        'form': form,
                        'error': 'Username or Password is incorrect'
                    }
                )

            login(request, user)

            return HttpResponseRedirect('/')

        return render(
            request,
            'authorization/login.html',
            {
                'form': form,
                'error': 'Invalid form'
            }
        )

    form = LoginForm()

    return render(
        request,
        'authorization/login.html',
        {
            'form': form
        }
    )


@authenticated_only
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')
