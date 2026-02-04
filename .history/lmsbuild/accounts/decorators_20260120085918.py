from django.core.exceptions import PermissionDenied

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            raise PermissionDenied

        # SUPERADMIN (django superuser) OR custom admin role
        if user.is_superuser or user.role == 'admin':
            return view_func(request, *args, **kwargs)

        raise PermissionDenied
    return wrapper
