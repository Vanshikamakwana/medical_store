 
# Create your models here.
from gettext import translation
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models herfrom django.db import models
from datetime import date, datetime
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
from django.contrib.auth.models import User

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# ✅ 2. Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    User_id = models.AutoField(primary_key=True)  
    Fname = models.CharField(max_length=20, null=False)
    Lname = models.CharField(max_length=20, null=False)
    Gender = models.CharField(max_length=2, null=False)
    Address = models.CharField(max_length=20, null=False)
    Mob_no = models.CharField(max_length=13, null=False)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = ['Fname', 'Lname']

    class Meta:
        db_table = 'user'  # ✅ MySQL ke existing "user" table se match karega

    def __str__(self):
        return self.Email


class state(models.Model):
    
    state_id=models.AutoField(primary_key=True)
    state_name=models.CharField(max_length=20,null=False)
     
    def __str__(self):
         return self.state_name

class City(models.Model):
    
    city_id=models.AutoField(primary_key=True)
    city_name=models.CharField(max_length=20,null=False)
    state_id=models.ForeignKey(state,on_delete=models.CASCADE)
    #state_id delete thase to city ma state_id delete thase

    def __str__(self):
         return self.city_name

class Area(models.Model):
     Area_id=models.AutoField(primary_key=True)
     Area_name=models.CharField(max_length=20,null=False)
     city_id=models.ForeignKey(City,on_delete=models.CASCADE)
     
     def __str__(self):
         return self.Area_name

class shop(models.Model):
     shop_id=models.AutoField(primary_key=True)
     shop_name=models.CharField(max_length=20,null=False)
     Address=models.CharField(max_length=50,null=False)
     Area_id=models.ForeignKey(Area,on_delete=models.CASCADE)

     def __str__(self):
         return f"shop from {self.Area_id}"

class role (models.Model):
    role_id=models.AutoField(primary_key=True)
    role_type=models.CharField(max_length=20,null=False)
    shop_id=models.ForeignKey(shop,on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.shop_id}:{self.role_type}"


class user(models.Model):
    User_id = models.AutoField(primary_key=True)
    Fname = models.CharField(max_length=20, null=False)
    Lname = models.CharField(max_length=20, null=False)
    Gender = models.CharField(max_length=2, null=False)
    Address = models.CharField(max_length=20, null=False)
    Mob_no = models.CharField(max_length=13, null=False)
    Email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=False)
    Area_id = models.ForeignKey('Area', on_delete=models.CASCADE)
    shop_id = models.ForeignKey('shop', on_delete=models.CASCADE)
    role_id = models.ForeignKey('role', on_delete=models.CASCADE,default="customer")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

# # ✅ Custom User Manager
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The Email field must be set")
#         email = self.normalize_email(email)
#         extra_fields.setdefault('is_active', True)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# # ✅ Custom User Model
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     User_id = models.AutoField(primary_key=True)  
#     Fname = models.CharField(max_length=20, null=False)
#     Lname = models.CharField(max_length=20, null=False)
#     Gender = models.CharField(max_length=2, null=False)
#     Address = models.CharField(max_length=20, null=False)
#     Mob_no = models.CharField(max_length=13, null=False)
#     Email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128, null=False)
#     Area_id = models.ForeignKey('Area', on_delete=models.CASCADE)
#     shop_id = models.ForeignKey('shop', on_delete=models.CASCADE)
#     role_id = models.ForeignKey('role', on_delete=models.CASCADE, default=1)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     # ✅ related_name set karein to avoid conflicts
#     groups = models.ManyToManyField(
#         "auth.Group",
#         related_name="customuser_groups",
#         blank=True
#     )
#     user_permissions = models.ManyToManyField(
#         "auth.Permission",
#         related_name="customuser_permissions",
#         blank=True
#     )

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'Email'
#     REQUIRED_FIELDS = ['Fname', 'Lname', 'Mob_no']

#     class Meta:
#         db_table = 'user'  # ✅ Existing MySQL table ka naam

#     def __str__(self):
#         return self.Email

    
class complains (models.Model):
    cmp_id=models.AutoField(primary_key=True)
    cmp_message=models.CharField(max_length=20,null=False)
    Date=models.DateTimeField()
    cmp_response=models.CharField(max_length=20,null=False)
    User_id=models.ForeignKey(user,on_delete=models.CASCADE)

class  Product_company(models.Model):
    comp_id=models.AutoField(primary_key=True)
    comp_name=models.CharField(max_length=20,null=False)
    comp_mob_no=models.CharField(max_length=13,null=False)
    comp_email=models.EmailField(unique=True)

class category(models.Model):
    cat_id=models.AutoField(primary_key=True)
    cat_name=models.CharField(max_length=20,null=False, unique=True)
    comp_id=models.ForeignKey(Product_company,on_delete=models.CASCADE)

class subcategory(models.Model):
    Sub_cat_id=models.AutoField(primary_key=True)
    Sub_cat_name=models.CharField(max_length=20,null=False)
    cat_id=models.ForeignKey(category,on_delete=models.CASCADE)

class unit_of_measurement(models.Model):
    unit_measurement_id=models.AutoField(primary_key=True)
    unit_measurement=models.CharField(max_length=20,null=False)

class Prescription(models.Model):
    pre_id=models.AutoField(primary_key=True)
    pre_image_url=models.ImageField(upload_to="shop/images",default="")
    date=models.DateTimeField()
    User_id=models.ForeignKey(user,on_delete=models.CASCADE)

    def __str__(self):
         return f"prescription of {self.User_id.Fname}"

class  Delivery_person(models.Model):
    Del_person_id=models.AutoField(primary_key=True)
    Del_name=models.CharField(max_length=20,null=False)
    mobile_no=models.CharField(max_length=13,null=False)
    Address=models.CharField(max_length=20,null=False)
    is_active=models.BooleanField(default=True)
    role_id=models.ForeignKey(role,on_delete=models.CASCADE)
    # Sales_id=models.ForeignKey(Sales,on_delete=models.CASCADE)

    def __str__(self):
        return self.Del_name
    
class Sales(models.Model):
     ORDER_STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('dispatched', 'Dispatched'),
        ('delivered', 'Delivered'),
        ('pending', 'Pending'),
    ]

     Sales_id=models.AutoField(primary_key=True)
     SGST=models.FloatField(null=False)
     CGST=models.FloatField(null=False)
     Sales_date=models.DateTimeField()
     pre_id=models.ForeignKey(Prescription,on_delete=models.CASCADE)
     User_id=models.ForeignKey(user,on_delete=models.CASCADE)
     Del_person_id = models.ForeignKey(Delivery_person, on_delete=models.CASCADE, null=True, blank=True)
# kya order ne delivery person ne assign karva mate
     order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='assigned')
# order nu status batava mate
     def __str__(self):
        return f"Order {self.order_id} for {self.customer_name}"


    
 
class Sales_return(models.Model):
    sel_ret_id=models.AutoField(primary_key=True)
    sal_ret_date=models.DateTimeField()
    reason=models.CharField(max_length=20,null=False)

class Product(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=50,null=False)
    product_des=models.CharField(max_length=40,null=False)
    product_ingredient=models.FloatField(null=False)
    product_price=models.DecimalField(max_digits=10,decimal_places=2)
    product_manuf_date=models.DateField()
    product_expiry_date=models.DateField()
    comp_id=models.ForeignKey(Product_company,on_delete=models.CASCADE)
    Sub_cat_id=models.ForeignKey(subcategory,on_delete=models.CASCADE)
    # Sub_cat_id=models.ForeignKey(subcategory,on_delete=models.CASCADE)
    unit_measurement_id=models.ForeignKey(unit_of_measurement,on_delete=models.CASCADE)
    # Sales_id=models.ForeignKey(Sales,on_delete=models.CASCADE)
    # sel_ret_id=models.ForeignKey(Sales_return,on_delete=models.CASCADE)
    pro_photo_url=models.ImageField(upload_to="products/",default="")
    stock_quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.product_name
# class Product_photo(models.Model):
#     pro_photo_id=models.AutoField(primary_key=True)
#     pro_photo_url=models.ImageField(upload_to="shop/images",default="")
#     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
   

class Batch(models.Model):
    batch_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    batch_quantity = models.IntegerField(null=False, default=0)
    batch_number = models.CharField(max_length=50,null=False,default=0)
    batch_expiry_date = models.DateField()

    def is_expired(self):
        return self.batch_expiry_date < date.today()

    def __str__(self):
        return f"{self.product.name} - {self.batch_number}"
   

class payment(models.Model):
     payment_id=models.AutoField(primary_key=True)
     payment_type=models.CharField(max_length=50,choices=[('cash','cash'),('Credit Card','Credit Card'),('Debit Card','Debit Card'),('cheque','cheque'),('other','other')])
     date=models.DateTimeField()
     Total_amount=models.DecimalField(max_digits=10,decimal_places=2)
     Sales_id=models.ForeignKey(Sales,on_delete=models.CASCADE)

     def __str__(self):
         return f"Payment ID:{self.payment_id},Payment Type:{self.payment_type}"

class suppliers(models.Model):
    
    suppliers_id=models.AutoField(primary_key=True)
    suppliers_name=models.CharField(max_length=20,null=False)
    suppliers_contact=models.CharField(max_length=13,null=False)
    comp_id=models.ForeignKey(Product_company,on_delete=models.CASCADE)

class purchase(models.Model):  
    purchase_id=models.AutoField(primary_key=True)
    purchase_name=models.CharField(max_length=20,null=False)
    purchase_desc=models.CharField(max_length=50,null=False)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    suppliers_id=models.ForeignKey(suppliers,on_delete=models.CASCADE)

class purchase_return(models.Model):
    
    purchase_return_id=models.AutoField(primary_key=True)
    reason=models.CharField(max_length=50,null=False)
    date=models.DateTimeField()
    purchase_id=models.ForeignKey(purchase,on_delete=models.CASCADE)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)

class sales_details(models.Model):
     Sales_id=models.ForeignKey(Sales,on_delete=models.CASCADE)
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     qty=models.IntegerField(null=False,default=0)
     price=models.DecimalField(max_digits=10,decimal_places=2)
     class meta:
      primary_key  =('Sales_id','product_id')

     

class sales_return_details(models.Model):
     sel_ret_id=models.ForeignKey(Sales_return,on_delete=models.CASCADE)
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     qty=models.IntegerField(null=False,default=0)
     price=models.DecimalField(max_digits=10,decimal_places=2)
     class meta:
       primary_key=('Sel_ret_id','product_id')

     

class purchase_details(models.Model):
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     purchase_id=models.ForeignKey(purchase,on_delete=models.CASCADE)
     qty=models.IntegerField(null=False,default=0)
     price=models.DecimalField(max_digits=10,decimal_places=2)
     class meta:
        primary_key=('product_id','purchase_id')

     

class purchase_return_details(models.Model):
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     purchase_return_id=models.ForeignKey(purchase,on_delete=models.CASCADE)
     qty=models.IntegerField(null=False,default=0)
     price=models.DecimalField(max_digits=10,decimal_places=2)
     class meta:
        primary_key=('product_id','purchase_return_id')


class unit_of_measurement_product(models.Model):

     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     unit_measurement_id=models.ForeignKey(unit_of_measurement,on_delete=models.CASCADE)
       
     class meta:
        primary_key=('product_id','unit_measurement_id')


class Cart(models.Model):
     User_id=models.ForeignKey(user,on_delete=models.CASCADE)
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     qty=models.IntegerField(null=False,default=0)
     totalamount=models.DecimalField(max_digits=10,decimal_places=2)
     class meta:
       primary_key=('User_id','product_id')
     def __str__(self):
        return f"User:{self.user.Fname} Product:{self.product.product_name}"
     

class feedback(models.Model):
     User_id=models.ForeignKey(user,on_delete=models.CASCADE)
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     feedbacks=models.CharField(max_length=25,null=False)
     Date=models.DateTimeField()
     class meta:
       primary_key=('User_id','product_id')
       
     def __str__(self):
        return f"User:{self.user.Fanme} Product:{self.product.product_name}"
     
class rating(models.Model):
     User_id=models.ForeignKey(user,on_delete=models.CASCADE)
     product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
     rate=models.IntegerField()
     rate_Date=models.DateTimeField()
     class meta:
       primary_key=('User_id','product_id')
     def __str__(self):
        return f"User:{self.user.Fname} Product:{self.product.product_name}"
    

@receiver(post_save, sender=sales_details)
def reduce_stock(sender, instance, **kwargs):
    """
    Reduce stock from the batches when a sale happens.
    """
    product = instance.product_id
    ordered_quantity = instance.qty
    batches = Batch.objects.filter(product=product).order_by('batch_expiry_date')

    for batch in batches:
        if batch.batch_quantity >= ordered_quantity:
            batch.batch_quantity -= ordered_quantity
            batch.save()
            break
        else:
            ordered_quantity -= batch.batch_quantity
            batch.batch_quantity = 0
            batch.save()

    if ordered_quantity > 0:
        raise ValueError("Stock adjustment issue: Not enough stock available!")

def allocate_stock(sales_detail):
    """
    Customer ke requested product quantity ko available batches se allocate karega.
    """
    product = sales_detail.product_id
    required_qty = sales_detail.qty

    # ✅ Step 1: Get all available batches sorted by expiry date (FIFO)
    available_batches = Batch.objects.filter(product_id=product).order_by('batch_expiry_date')

    if not available_batches.exists():
        raise ValueError(f"Product '{product.product_name}' is out of stock!")

    remaining_qty = required_qty

    # ✅ Step 2: Iterate through batches and allocate stock
    for batch in available_batches:
        if remaining_qty <= 0:
            break  # Agar puri quantity mil gayi, loop se bahar niklo
        
        if batch.stock_quantity >= remaining_qty:
            # ✅ Step 3a: Batch me sufficient stock hai, poora deduct karo
            batch.stock_quantity -= remaining_qty
            batch.save()
            remaining_qty = 0
        else:
            # ✅ Step 3b: Batch ka poora stock use karo aur remaining dusri batch se lo
            remaining_qty -= batch.stock_quantity
            batch.stock_quantity = 0
            batch.save()

    # ✅ Step 4: Agar ab bhi quantity fulfill nahi hui, raise error
    if remaining_qty > 0:
        raise ValueError(f"Not enough stock available for '{product.product_name}'!")

    return True

# ✅ Django Signal: Order Place Hote Hi Stock Deduct Ho Jaye
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=sales_details)
def update_stock_on_order(sender, instance, **kwargs):
    try:
        with translation.atomic():  # ✅ Ensure atomicity
            allocate_stock(instance)
    except ValueError as e:
        print(f"Stock Error: {str(e)}")
