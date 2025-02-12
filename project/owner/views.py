from datetime import datetime
from gettext import translation
from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from owner.models import Batch, Product_company, Sales, sales_details,user
from owner.models import purchase, suppliers,Product,purchase_details,Delivery_person,role
from owner.forms import ProductForm
from owner.forms import SupplierForm
# Create your views here.
def index(request):
    orders = Sales.objects.all()
    users=user.objects.all()
    return render(request,'owner/template/index.html', {'orders': orders,'users':users})
# ,{'users':users}
          
def view_order(request):
    orders = Sales.objects.all()
    users=user.objects.all()
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
        product_id = request.POST['product']
        batch_number = request.POST['batch_number']
        batch_quantity = request.POST['batch_quantity']
        batch_expiry_date = request.POST['batch_expiry_date']

        product = Product.objects.get(product_id=product_id)

        Batch.objects.create(
            product=product,
            batch_number=batch_number,
            batch_quantity=batch_quantity,
            batch_expiry_date=batch_expiry_date
        )
        return redirect('batch_list')

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

def allocate_product_to_order(product_id, order_qty, sales_id):
    """
    कस्टमर द्वारा ऑर्डर किए गए product की quantity को available batches में से allocate करता है।
    अगर quantity एक batch में उपलब्ध नहीं है तो दूसरी batch से घटाएगा।
    """
    product = get_object_or_404(Product, pk=product_id)
    batches = Batch.objects.filter(product_id=product, batch_quantity__gt=0).order_by('batch_expiry_date')

    remaining_qty = order_qty
    allocated_batches = []

    with translation.atomic():  # Ensures atomic transaction
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

