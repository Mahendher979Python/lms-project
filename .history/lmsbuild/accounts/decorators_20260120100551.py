from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied

        if request.user.is_superuser or request.user.role == 'admin':
            return view_func(request, *args, **kwargs)

        raise PermissionDenied
    return wrapper
