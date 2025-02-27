# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required
# from functools import wraps
# from owner.models import User  # Correct import

# def delivery_required(view_func):
#     # @wraps(view_func)
#     # @login_required(login_url='delivery:delivery_login')
#     def wrapper_func(request, *args, **kwargs):
#         user_id=request.session.get('user_id')
#         if user_id:
#             request.user=User.objects.get(id=user_id)
#             if user.role_id.role_type=='delivery':
#                 return view_func(request, *args, **kwargs)
#         reteurn redirect('delivery_login')   
#     return wrapper_func

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from owner.models import User  # Correct import

def delivery_required(view_func):
    @wraps(view_func)
    @login_required(login_url='delivery:delivery_login')
    def wrapper_func(request, *args, **kwargs):
        if request.user.role_id_id in [2, 4]:  # Check if the user has the delivery role
            return view_func(request, *args, **kwargs)
        else:
            return redirect('delivery:delivery_login')
    return wrapper_func