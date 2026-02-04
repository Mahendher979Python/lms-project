from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect("login")

        if request.user.is_superuser or getattr(request.user, "role", None) == "admin":
            return view_func(request, *args, **kwargs)

        return redirect("login")

    return wrapper
