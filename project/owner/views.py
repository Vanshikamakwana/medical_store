from datetime import datetime
from django.db import transaction
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render,redirect,get_object_or_404
from owner.models import Batch, Product_company, Sales, sales_details,CustomUser
from owner.models import purchase, suppliers,Product,payment,purchase_details,Delivery_person,role,Area,shop
from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string
from django.db.models import Sum
from owner.forms import LoginForm, ProductForm, RegisterForm
from owner.decorators import admin_required
from django.core.mail import send_mail
# Create your views here.
@admin_required
def index(request):
    total_sales = Sales.objects.aggregate(total_sales=Sum('sales_details__qty'))['total_sales'] or 0

    # Calculate total revenue
    total_revenue = Sales.objects.aggregate(total_revenue=Sum('sales_details__price'))['total_revenue'] or 0

    # Calculate new users
    # new_users = CustomUser.objects.filter(date_joined__month=datetime.now().month).count()

    # Fetch sales data for the chart
    # sales_data = Sales.objects.values('sales_date__month').annotate(total_sales=Sum('salesdetails__qty')).order_by('sales_date__month')

    # Fetch orders and users for the tables
    orders = Sales.objects.all()
    users = CustomUser.objects.all()

    return render(request, 'owner/template/index.html', {
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        # 'new_users': new_users,
        # 'sales_data': sales_data,
        'orders': orders,
        'users': users,
    })
          
def view_order(request):
    orders = Sales.objects.all()
    # sales_details=sales_details.objects.all()
    users=CustomUser.objects.all()
    return render(request, 'view_order.html', {'orders': orders,'users':users})

def purchase_order(request):
   if request.method == 'POST':
        # Form data ko handle kar rahe hain
        purchase_name = request.POST.get('purchase_name')
        purchase_desc = request.POST.get('purchase_desc')
        total_price = request.POST.get('total_price')
        suppliers_id = request.POST.get('suppliers_id')
        product_id = request.POST.get('product_id')
        qty = request.POST.get('qty')
        price = request.POST.get('price')

        # Convert qty and price to appropriate types
        qty = int(qty)
        price = float(price)
        total_price = float(total_price)

        # Supplier instance ko fetch kar rahe hain using the ID
        supplier_instance = suppliers.objects.get(suppliers_id=suppliers_id)
        product_instance = Product.objects.get(product_id=product_id)

        try:
            with transaction.atomic():
                # New Purchase Order create karna
                new_purchase = purchase(
                    purchase_name=purchase_name,
                    purchase_desc=purchase_desc,
                    total_price=total_price,
                    suppliers_id=supplier_instance
                )
                new_purchase.save()

                # New Purchase Details create karna
                new_purchase_details = purchase_details(
                    product_id=product_instance,
                    purchase_id=new_purchase,
                    qty=qty,
                    price=price
                )
                new_purchase_details.save()

                # Update the stock quantity of the product
                product_instance.stock_quantity += qty
                product_instance.save()

                # Redirect to some success page or purchase list
                return redirect('ownerhome')  # Modify this URL as per your app structure

        except Exception as e:
            # Handle any errors that occur during the transaction
            print(f"Error: {e}")

   else:
        # GET request ke liye suppliers aur products ko fetch kar rahe hain
        suppliers_list = suppliers.objects.all()
        products_list = Product.objects.all()

        # Template render karna
        return render(request, 'purchase_order.html', {'suppliers_list': suppliers_list, 'products_list': products_list})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def product_update(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

def product_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})
     
# ✅ 1. Supplier List View
def supplier_list(request):
    all_suppliers = suppliers.objects.all()  # Sare suppliers fetch karega
    return render(request, "supplier_list.html", {"suppliers": all_suppliers})

# ✅ 2. Add Supplier
def add_supplier(request):
    companies = Product_company.objects.all()  # Sare companies fetch karega
    
    if request.method == "POST":
        supplier_name = request.POST["suppliers_name"]
        supplier_contact = request.POST["suppliers_contact"]
        comp_id = request.POST["comp_id"]  # Selected company ID

        company = Product_company.objects.get(comp_id=comp_id)  # Get selected company object
        new_supplier = suppliers(suppliers_name=supplier_name, suppliers_contact=supplier_contact, comp_id=company)
        new_supplier.save()
        return redirect("supplier_list")  # Redirect to supplier list page

    return render(request, "supplier_form.html", {"companies": companies})

# ✅ 3. Update Supplier
def update_supplier(request, supplier_id):
    supplier = get_object_or_404(suppliers, pk=supplier_id)
    companies = Product_company.objects.all()  # Fetch all companies for dropdown

    if request.method == "POST":
        supplier.suppliers_name = request.POST["suppliers_name"]
        supplier.suppliers_contact = request.POST["suppliers_contact"]
        comp_id = request.POST["comp_id"]
        supplier.comp_id = Product_company.objects.get(comp_id=comp_id)  # Update company
        
        supplier.save()
        return redirect("supplier_list")

    return render(request, "update_supplier.html", {"supplier": supplier, "companies": companies})

# ✅ 4. Delete Supplier
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(suppliers, pk=supplier_id)
    supplier.delete()
    return redirect("supplier_list")

def delivery_person_list(request):
    delivery_persons = Delivery_person.objects.all()
    return render(request, "delivery_person_list.html", {"delivery_persons": delivery_persons})

def add_delivery_person(request):
    if request.method == "POST":
        name = request.POST["name"]
        mobile_no = request.POST["mobile_no"]
        address = request.POST["address"]
        role_id = request.POST["role_id"]
        is_active = request.POST.get("is_active", False) == "on"

        role_instance = role.objects.get(pk=role_id)

        Delivery_person.objects.create(
            Del_name=name, 
            mobile_no=mobile_no, 
            Address=address, 
            is_active=is_active,
            role_id=role_instance
        )
        return redirect("delivery_person_list")

    roles = role.objects.all()  # Role dropdown ke liye
    return render(request, "add_delivery_person.html", {"roles": roles})

def update_delivery_person(request, delivery_id):
    delivery_person = get_object_or_404(Delivery_person, pk=delivery_id)
    roles = role.objects.all() 
    if request.method == "POST":
        delivery_person.Del_name = request.POST["name"]
        delivery_person.mobile_no = request.POST["mobile_no"]
        delivery_person.Address = request.POST["address"]
        delivery_person.role_id = role.objects.get(role_id=request.POST["role_id"])
        delivery_person.is_active = request.POST.get("is_active", False) == "on"
        delivery_person.save()
        return redirect("delivery_person_list")

    roles = role.objects.all()  # Role dropdown ke liye
    return render(request, "update_delivery_person.html", {"delivery_person": delivery_person, "roles": roles})

def delete_delivery_person(request, delivery_id):
    delivery_person = get_object_or_404(Delivery_person, delivery_id=delivery_id)
    delivery_person.delete()
    return redirect("delivery_person_list")

def create_batch(request):
    if request.method == 'POST':
        product_id = request.POST['product_id']
        batch_number = request.POST['batch_number']
        batch_quantity = request.POST['batch_quantity']
        batch_expiry_date = request.POST['batch_expiry_date']

        product = Product.objects.get(product_id=product_id)

        Batch.objects.create(
            product_id=product,
            batch_number=batch_number,
            batch_quantity=batch_quantity,
            batch_expiry_date=batch_expiry_date
        )
        return redirect('list_batches')

    products = Product.objects.all()  # Dropdown ke liye
    return render(request, 'batch_add.html', {'products': products})

def update_batch(request, batch_id):
   batch = get_object_or_404(Batch, batch_id=batch_id)

   if request.method == 'POST':
        batch.batch_number = request.POST['batch_number']
        batch.batch_quantity = request.POST['batch_quantity']
        batch.batch_expiry_date = request.POST['batch_expiry_date']
        batch.save()
        return redirect('list_batches')

   return render(request, 'batch_update.html', {'batch': batch})

def delete_batch(request, batch_id):
    batch = get_object_or_404(Batch, batch_id=batch_id)
    batch.delete()
    return redirect('batch_list')

def list_batches(request):
    batches = Batch.objects.all().order_by('-batch_expiry_date')
    return render(request, 'batch_list.html', {'batches': batches})

# def allocate_product_to_order(product_id, order_qty, sales_id):
    """
    कस्टमर द्वारा ऑर्डर किए गए product की quantity को available batches में से allocate करता है।
    अगर quantity एक batch में उपलब्ध नहीं है तो दूसरी batch से घटाएगा।
    """
    product = get_object_or_404(Product, pk=product_id)
    batches = Batch.objects.filter(product_id=product, batch_quantity__gt=0).order_by('batch_expiry_date')

    remaining_qty = order_qty
    allocated_batches = []

    with transaction.atomic():  # Ensures atomic transaction
        for batch in batches:
            if remaining_qty <= 0:
                break

            if batch.batch_quantity >= remaining_qty:
                batch.batch_quantity -= remaining_qty
                allocated_batches.append((batch, remaining_qty))
                remaining_qty = 0
            else:
                allocated_batches.append((batch, batch.batch_quantity))
                remaining_qty -= batch.batch_quantity
                batch.batch_quantity = 0  # Batch is now empty

            batch.save()

        if remaining_qty > 0:
            raise ValueError(f"Not enough stock available for product {product.product_name}")

        # Sales details में entry करना
        for batch, qty in allocated_batches:
            sales_details.objects.create(
                Sales_id=Sales.objects.get(pk=sales_id),
                product_id=product,
                qty=qty,
                price=product.product_price * qty
            )

    return f"Order placed successfully for {order_qty} units of {product.product_name}"
# @login_required
def manage_profile(request):
    user_id = request.session.get('user_id')
    user = CustomUser.objects.get(User_id=user_id)
    roles = role.objects.values('role_id', 'role_type').distinct()
    shops = shop.objects.all()
    areas = Area.objects.all()

    if request.method == "POST":
        if "current_password" in request.POST:  # Change Password Logic
            current_password = request.POST["current_password"]
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]

            if not check_password(current_password, user.password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match.")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Keep user logged in
                messages.success(request, "Password updated successfully!")

        else:  # Update Profile Logic
            user.Fname = request.POST["Fname"]
            user.Lname = request.POST["Lname"]
            user.Gender = request.POST["Gender"]
            user.Address = request.POST["Address"]
            user.Mob_no = request.POST["Mob_no"]
            user.role_id = role.objects.get(role_id=request.POST["role_id"])
            user.shop_id = shop.objects.get(shop_id=request.POST["shop_id"])
            user.Area_id = Area.objects.get(Area_id=request.POST["area_id"])
            user.is_active = request.POST.get("is_active", False) == "on"
            user.save()
            messages.success(request, "Profile updated successfully!")

        return redirect("manage_profile")

    return render(request, "manage_profile.html", {"user": user, "roles": roles, "shops": shops, "areas": areas})
def register_view(request):   
    
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        mob_no = request.POST.get('mob_no')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        area_id = request.POST.get('area_id')
        shop_id = request.POST.get('shop_id')
        role_id = request.POST.get('role_id')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register_view')

        if CustomUser.objects.filter(Email=email).exists():
            # messages.error(request, "Email already registered!")
            return redirect('register_view')

        hashed_password = make_password(password1)  # Password hashing
        new_user = CustomUser(
            Fname=fname, Lname=lname, Gender=gender, Address=address,
            Mob_no=mob_no, Email=email, password=hashed_password,
            Area_id_id=area_id, shop_id_id=shop_id, role_id_id=role_id
        )
        new_user.save()
        # messages.success(request, "Account created successfully!")
        return redirect('login_view')

    shops = shop.objects.all()
    roles = role.objects.all()
    areas = Area.objects.all()
    return render(request, 'register_view.html', {'shops': shops, 'roles': roles, 'areas': areas})
# 🟢 User Login View
def login_view(request):
    # if request.method == "POST":
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     try:
    #         user_obj = CustomUser.objects.get(Email=email)
    #         if check_password(password, user_obj.password):  # ✅ Password verify
    #             request.session['user_id'] = user_obj.User_id  # ✅ Session store
    #             # messages.success(request, "Login successful!")
    #             return redirect('ownerhome')
    #         else:
    #             pass
    #             # messages.error(request, "Invalid password!")
    #     except CustomUser.DoesNotExist:
    #         # messages.error(request, "User does not exist!")
    #         pass
    # return render(request, 'login_view.html')
     if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = CustomUser.objects.get(Email=email)
            if check_password(password, user_obj.password):  # Password verify
                if user_obj.role_id.role_type == 'admin':  # Check if the user is an admin
                    request.session['user_id'] = user_obj.User_id  # Session store
                    # messages.success(request, "Login successful!")
                    return redirect('ownerhome')
                else:
                    pass
                    # messages.error(request, "You do not have permission to access this page.")
            else:
                pass
                # messages.error(request, "Invalid password!")
        except CustomUser.DoesNotExist:
           pass
            # messages.error(request, "User does not exist!")
     return render(request, 'login_view.html')
def logout(request):
    request.session.flush()  # ✅ Session clear
    # messages.success(request, "Logged out successfully!")
    return redirect('login_view')



def sales_report(request):
    # Aggregate sales data by month
    sales_data = Sales.objects.values('Sales_date__month').annotate(total_sales=Sum('sales_details__qty')).order_by('Sales_date__month')
    total_revenue = Sales.objects.aggregate(total_revenue=Sum('sales_details__price'))['total_revenue']
    total_orders = Sales.objects.count()
    total_customers = CustomUser.objects.count()

    return render(request, 'sales_report.html', {
        'sales_data': sales_data,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_customers': total_customers,
    })

def forgot_pass(request):
   if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(Email=email)
            reset_token = get_random_string(length=32)
            user.reset_token = reset_token
            user.save()
            reset_url = request.build_absolute_uri(f'/owner/reset_password/{reset_token}/')
            send_mail(
                'Password Reset Request',
                f'Click the link below to reset your password:\n{reset_url}',
                'noreply@example.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('login_view')
        except CustomUser.DoesNotExist:
            messages.error(request, "User with this email does not exist.")
   return render(request, 'forgot_pass.html')

def reset_password(request, reset_token):
    try:
        user = CustomUser.objects.get(reset_token=reset_token)
        if request.method == "POST":
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.password = make_password(new_password)
                user.reset_token = None
                user.save()
                messages.success(request, "Password has been reset successfully.")
                return redirect('login_view')
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, 'reset_password.html', {'reset_token': reset_token})
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid password reset token.")
        return redirect('forgot_pass')
    

def manage_payment(request):
    payment_type = request.GET.get('payment_type')
    if payment_type:
        payments = payment.objects.filter(payment_type=payment_type)
    else:
        payments = payment.objects.all()

    return render(request, "manage_payment.html", {"payments": payments, "selected_method": payment_type})


def allocate_stock(sales_detail):
    """
    Allocate stock from batches for the given sales detail.
    """
    product = sales_detail.product_id
    required_qty = sales_detail.qty

    # Step 1: Get all available batches sorted by expiry date (FIFO)
    available_batches = Batch.objects.filter(product_id=product).order_by('batch_expiry_date')

    if not available_batches.exists():
        raise ValueError(f"Product '{product.product_name}' is out of stock!")

    remaining_qty = required_qty

    # Step 2: Iterate through batches and allocate stock
    for batch in available_batches:
        if remaining_qty <= 0:
            break  # No more stock needed, exit loop

        remaining_qty = batch.allocate_stock(remaining_qty)

    # Step 3: If there is remaining quantity that couldn't be fulfilled, raise an error
    if remaining_qty > 0:
        raise ValueError(f"Not enough stock available for '{product.product_name}'!")

    return True
