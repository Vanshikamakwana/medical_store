from django.contrib import messages
from urllib import request
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate
from .forms import RegisterForm
from owner.models import product,category,subcategory, role,user
from django.conf import settings

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
     # if request.method == "POST":
     #    email = request.POST["email"]
     #    password = request.POST["password"]
        
     #    try:
     #        user = user.objects.get(email=email)  # Get the user by email
     #        if user.check_password(password):  # Check if the password is correct
     #            # Manually log the user in
     #            request.session['User_id'] = user.id
     #            messages.success(request, "Login successful!")
     #            return redirect("home")  # Redirect to home page
     #        else:
     #            messages.error(request, "Invalid email or password!")
     #    except user.DoesNotExist:
     #        messages.error(request, "Invalid email or password!")

     return render(request, "shop/template/login.html") 
     

def register(request):
#     if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_instance = form.save(commit=False)
            user_instance.password = make_password(form.cleaned_data['password'])  # Password hashing
            
            # Default role set karein (Customer)
            customer_role = role.objects.get(role_type="Customer")  # role_name aapke role table me hona chahiye
            user_instance.role_id = customer_role

            user_instance.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('home')
        else:
               form = RegisterForm()
          
        return render(request, 'register.html', {'form': form})

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