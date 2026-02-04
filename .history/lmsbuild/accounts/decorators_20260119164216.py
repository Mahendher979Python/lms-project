from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_superuser and request.user.role != 'admin':
            messages.error(request, "Access denied")
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper
