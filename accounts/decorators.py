from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def role_required(*roles):
    def check(user):
        return user.is_authenticated and (user.is_superuser or user.role in roles)
    return user_passes_test(check)


def approved_shopkeeper_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated or not user.is_shopkeeper:
            raise PermissionDenied
        if not user.is_approved or not user.shopkeeper_profile.is_active:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper
