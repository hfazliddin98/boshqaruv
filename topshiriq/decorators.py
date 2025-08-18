from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('kirish')
            
            if request.user.role not in allowed_roles:
                return HttpResponseForbidden("Sizda bu sahifaga kirish huquqi yo'q.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
