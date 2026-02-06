

def role_required(allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.user.roleinfo.role   
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("You do not have permission to access this resource.")
        return _wrapped_view
    return decorator
