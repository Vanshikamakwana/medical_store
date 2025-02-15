from django.shortcuts import redirect
from .models import CustomUser

def admin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_id = request.session.get('user_id')
        if user_id:
            user = CustomUser.objects.get(User_id=user_id)
            if user.role_id.role_type == 'admin':
                return view_func(request, *args, **kwargs)
        return redirect('login_view')
    return wrapper_func