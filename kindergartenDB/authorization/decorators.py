from django.http import HttpResponseRedirect, Http404


def authenticated_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect('/signup')

    return wrapper


def post_method_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        raise Http404()

    return wrapper


def staff_only(func):
    @authenticated_only
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    return wrapper
