from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps

def admin_required(function):
    @wraps(function)
    @login_required
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            messages.warning(request, "You do not have permission to access this page.")
            return redirect("home")  # Change to your homepage URL name
    return wrap
