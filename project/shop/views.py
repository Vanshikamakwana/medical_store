from itertools import product
from django.contrib import messages
from urllib import request
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from .forms import RegisterForm
from owner.models import Product,category,subcategory, role,CustomUser
from django.conf import settings
# from django.contrib.auth import get_user_model

# User = get_user_model()
# Create your views here.
def index(request):
#    products = product.objects.all()  # Sare products fetch karne ke liye
#    for product in products:
#      print(product.product_name, product.product_price)
    
   return render(request,"index.html")

def about(request):
     return render(request,"shop/template/about.html")

def service(request):
     return render(request,"shop/template/service.html")

def service_details(request):
     return render(request,"shop/template/service_details.html")

def faq(request):
     return render(request,"shop/template/faq.html")

def locations(request):
     return render(request,"shop/template/locations.html")

def shop(request,cat_name=None):
    category_obj = None  # Initialize category
    subcategories = subcategory.objects.all()  # Fetch all subcategories
    products = product.objects.all()  # Fetch all products

    if cat_name:
        try:
            category_obj = category.objects.filter(cat_name=cat_name).first()  # Get first matching category
            if category_obj:
                subcategories = subcategory.objects.filter(cat_id=category_obj)
                products = product.objects.filter(Sub_cat_id__in=subcategories) 
                 # _in ka use You have a category named "Skin Care"
                    # "Skin Care" has multiple subcategories like "Face Wash", "Moisturizer", and "Sunscreen".
                    # You need to get all products that belong to any of these subcategories.
            else:
                return render(request, 'shop.html', {
                    'error': f"Category '{cat_name}' not found",
                    'products': products,
                    'cat_name': cat_name
                })
        except category.DoesNotExist:  # Not needed with .filter().first(), but keeping for safety
            pass  

    return render(request, 'shop.html', {
        'category': category_obj,  # Fix variable name
        'subcategories': subcategories,
        'products': products,
        'cat_name': cat_name,
        'MEDIA_URL': settings.MEDIA_URL
    })

def cart(request):
     return render(request,"shop/template/cart.html")
def wishlist(request):
     return render(request,"shop/template/wishlist.html")
def checkout(request):
     return render(request,"shop/template/checkout.html")
def order_tracking(request):
     return render(request,"shop/template/order_tracking.html")
def account(request):
     return render(request,"shop/template/account.html")
def login(request):
     if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            # ✅ Role ID ke basis pe redirect karna
            if user.role_id.id == 1:  # 1 means Admin
                return redirect('ownerhome')
            else:  # Any other role means Customer
                return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
    
     return render(request, "login.html") 
     

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        mob_no = request.POST['mob_no']
        address = request.POST['address']
        gender = request.POST['gender']
        area_id = request.POST['area_id']
        shop_id = request.POST['shop_id']
        role_id = request.POST['role_id']  # Role ID (1 = Admin, 2 = Customer)

        if User.objects.filter(Email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('register')

        user = User(
            Fname=fname,
            Lname=lname,
            Email=email,
            Mob_no=mob_no,
            Address=address,
            Gender=gender,
            Area_id_id=area_id,  # ForeignKey ke liye "_id" lagana zaroori hai
            shop_id_id=shop_id,  # ForeignKey ke liye "_id" lagana zaroori hai
            role_id_id=role_id  # Role assign karega
        )
        user.set_password(password)  # ✅ Password ko hash karega
        user.save()  # ✅ MySQL "user" table me save karega

        messages.success(request, "Registration successful!")
        return redirect('login')

          
    return render(request, 'register.html')
# , {'form': form}

def contact(request):
     return render(request,"shop/template/contact.html")

def blog(request):
     return render(request,"shop/template/blog.html")

def history(request):
     return render(request,"shop/template/history.html")

def protfolio(request):
     return render(request,"shop/template/portfolio.html")

def protfolio_details(request):
     return render(request,"shop/template/porttfolio-details.html")

def login_register(request):
     return render(request,"shop/template/login-register.html")

def blog_details(request):
     return render(request,"shop/template/blog-details.html")

def error(request):
     return render(request,"shop/template/404.html")

def  coming_soon(request):
     return render(request,"shop/template/coming-soon.html")

def  product_details(request):
     

      return render(request,"shop/template/product-details.html")

def  add_listing(request):
     return render(request,"shop/template/add-listing.html")


# def contact(request):
#      return HttpResponse("we are at contact")

# def productview(request):
#      return HttpResponse("we are at productview")

# def checkout(request):
#      return HttpResponse("we are at checkout")

# def tracker(request):
#      return HttpResponse("we are at tracker")

# def search(request):
#      return HttpResponse("we are at search")