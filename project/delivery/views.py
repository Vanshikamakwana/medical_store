from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from owner.models import Sales, CustomUser
# from .decorators import delivery_required
from django.views.decorators.csrf import csrf_exempt

# def delivery_login(request):
#     """ डिलीवरी पर्सन का लॉगिन पेज """
#     if request.user.is_authenticated:
#         if request.user.role_id_id in [2, 4]:
#             return redirect('delivery:deliveryhome')  # पहले से लॉगिन है तो सीधे डैशबोर्ड पर भेजो
#         else:
#             logout(request)
#             messages.error(request, "You do not have permission to access this page.")
#             return redirect('delivery:delivery_login')

#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         if not email or not password:
#             messages.error(request, "Email and password are required.")
#             return render(request, 'delivery/template/delivery_login.html')

#         user = authenticate(request, username=email, password=password)

#         if user is not None and user.role_id_id in [2, 4]:  # Check if user has delivery role
#             login(request, user)
#             return redirect('delivery:deliveryhome')  # ✅ लॉगिन के बाद View Sales पेज दिखेगा
#         else:
#             messages.error(request, "Invalid username or password.")  # Error Message दिखाओ

#     return render(request, 'delivery/template/delivery_login.html')

# @delivery_required
# def delivery_logout(request):
#     """ डिलीवरी पर्सन लॉगआउट करने पर वापस लॉगिन पेज पर जाएगा """
#     logout(request)
#     return redirect('delivery:delivery_login')  # ✅ लॉगआउट होने पर फिर लॉगिन पेज पर भेजो

# @delivery_required
def index(request):
    return render(request, 'delivery/template/index.html')

# @delivery_required
def view_sales(request):
    sales = Sales.objects.all()  # Filter sales by logged-in delivery person
    return render(request, 'delivery/template/view_sales.html', {'sales': sales})

# @delivery_required
def sales_history(request):
    delivered_sales = Sales.objects.filter(order_status='delivered')  # Filter sales by logged-in delivery person
    return render(request, 'delivery/template/sales_history.html', {'sales': delivered_sales})

@csrf_exempt
def update_sale_status(request, sale_id):
    if request.method == "POST":
        try:
            new_status = request.POST.get("status")
            sale = Sales.objects.get(Sales_id=sale_id)
            sale.order_status = new_status
            sale.save()
            messages.success(request, "Status updated successfully!")
        except Sales.DoesNotExist:
            messages.error(request, "Sale not found.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return redirect('delivery:delivery_view_sales')