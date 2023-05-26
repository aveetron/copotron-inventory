from django.shortcuts import redirect
from django.views import View


def check_login():
    def decorator_wrapper(func):
        def warp(request, *args, **kwargs):
            if request.user.is_authenticated:
                pass
            else:
                return redirect("login")
            return decorator_wrapper(request, *args, **kwargs)

        return func
