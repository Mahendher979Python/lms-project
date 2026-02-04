from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role in ['admin', 'superadmin']:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper
