from decimal import Decimal
from django.shortcuts import render,redirect,HttpResponse
from owner.models import Product,Cart,CustomUser,shop,role,Area,category,subcategory
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib import messages
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password, check_password

import json
# Create your views here.
def index(request):
   products=Product.objects.all()
   context={'products' :products,'MEDIA_URL':settings.MEDIA_URL}

#    if 'user_id' not in request.session:
#         messages.error(request, "You must be logged in to view this page!")
#         return redirect('login')

#    user_id = request.session['user_id']
#    user_obj = CustomUser.objects.get(User_id=user_id)
   
    
   return render(request,"shop/template/index.html",context)

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

def Shop(request,cat_name=None):
    category_obj = None  # Initialize category
    subcategories = subcategory.objects.all()  # Fetch all subcategories
    products = Product.objects.all()  # Fetch all products

    if cat_name:
        try:
            category_obj = category.objects.filter(cat_name=cat_name).first()  # Get first matching category
            if category_obj:
                subcategories = subcategory.objects.filter(cat_id=category_obj)
                products = Product.objects.filter(Sub_cat_id__in=subcategories) 
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
    if not is_authenticated(request):
        return redirect('login')
    cart_items = request.session.get('cart', {})
    products = Product.objects.filter(product_id__in=cart_items.keys())
    cart_details = []
    total_price = Decimal('0.00')
    
    for product in products:
        product_id_str = str(product.product_id)
        quantity = cart_items[product_id_str]['quantity']
        price = Decimal(cart_items[product_id_str]['price'])
        subtotal = price * quantity
        total_price += subtotal
        cart_details.append({
            'product_id': product.product_id,
            'product_name': product.product_name,
            'pro_photo_url': product.pro_photo_url,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })
    
    return render(request, "cart.html", {'cart_details': cart_details, 'total_price': total_price})

def add_to_cart(request, product_id):
#      if not is_authenticated(request):
#         return redirect('login') 
#      user = CustomUser.objects.get(User_id=request.session['User_id'])
#      try:
#        products = Product.objects.get(product_id=id)
#        print(f"Product Found: {products.product_name}")
#      except Product.DoesNotExist:
#       print(f"Product with ID {id} does not exist.")
     
#      price=products.product_price
#      print(price)

#      qty = int(request.POST.get('qty', 1))

#      total_amount = price * qty
    
#     # Add or update the cart item
#      cart_item,created = Cart.objects.get_or_create(
#         User_id=user,
#         product_id=products,
#     )
    
#      cart_item.quantity += 1 
#      total_amount = products.product_price * cart_item.qty  # Recalculate total amount with new qty
    
#      cart_item.totalamount = total_amount  # Set total # Increment quantity by 1
#      cart_item.save()
    
#      return redirect('cart')
    
     if request.method == 'POST':
        product = Product.objects.get(product_id=product_id)
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)  # Convert product_id to string for dictionary key
        if product_id_str in cart:
            cart[product_id_str]['quantity'] += 1
        else:
            cart[product_id_str] = {'quantity': 1, 'price': str(product.product_price)}  # Convert Decimal to string
        request.session['cart'] = cart
        return JsonResponse({'message': 'Product added to cart', 'cart': cart})
     return JsonResponse({'error': 'Invalid request'}, status=400)

def wishlist(request):
     return render(request,"shop/template/wishlist.html")
def checkout(request):
     return render(request,"shop/template/checkout.html")
def order_tracking(request):
     return render(request,"shop/template/order_tracking.html")
def account(request):
     return render(request,"shop/template/account.html")

def is_authenticated(request):
    return 'User_id' in request.session

def login(request):
     if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Fetch the user from your custom table
            user = CustomUser.objects.get(Email=email)
            
            # Check if the provided password matches the stored hashed password
            if check_password(password, user.password):  # check_password hashes the password
                # If authentication is successful, log the user in
                request.session['User_id'] = user.User_id  # Store user info in session
                return redirect('home')  # Redirect to homepage or any other page
            else:
                return HttpResponse('Invalid password')
        
        except CustomUser.DoesNotExist:
             return HttpResponse('User does not exist')
    
     return render(request, 'shop/template/login.html') 
     
   
def register(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mob_no = request.POST.get('mob_no')
        email = request.POST.get('email')
        password = request.POST.get('password')
        area_id = request.POST.get('area_id')  # Foreign Key
        shop_id = request.POST.get('shop_id')  # Foreign Key
        role_id = request.POST.get('role_id')  # Foreign Key

        if CustomUser.objects.filter(Email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        hashed_password = make_password(password)  # ✅ Password hashing
        new_user = CustomUser(
            Fname=fname, Lname=lname, Gender=gender, Address=address,
            Mob_no=mob_no, Email=email, password=hashed_password,
            Area_id_id=area_id, shop_id_id=shop_id, role_id_id=role_id
        )
        new_user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')
    areas = Area.objects.all()
    shops = shop.objects.all()
    roles = role.objects.all()


    return render(request,"shop/template/register.html",{'areas': areas, 'shops': shops, 'roles': roles})


# 🟢 User Login View

# 🟢 User Logout View
def user_logout(request):
    logout(request)# ✅ Session clear
     
    messages.success(request, "Logged out successfully!")
    return redirect('login')

# 🟢 Dashboard/Profile View


     

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

def product_details(request,product_id):
  try:
       products=Product.objects.filter(product_id=product_id)
  except:
        products=None
  
  return render(request,"shop/template/product-details.html",{'products':products})

def  add_listing(request):
     return render(request,"shop/template/add-listing.html")

def quick_view(request, product_id):

 products = Product.objects.get(product_id=product_id)
 data = {
        'name': products.product_name,
        'description': products.product_des,
        'price': products.product_price,
        'image': products.pro_photo_url.url,
    }
 print(data)
 return JsonResponse(data)


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