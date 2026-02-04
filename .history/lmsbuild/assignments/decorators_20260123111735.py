from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def group_required(group_name):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):

            # ✅ Superuser always allowed
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # ✅ Group check
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)

            return redirect("assignments:unauthorized")

        return wrapper
    return decorator
