from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import purchase_details, sales_details, Product

# Purchase hone ke baad stock update karega
@receiver(post_save, sender=purchase_details)
def update_stock_after_purchase(sender, instance, created, **kwargs):
    if created:  # Jab naye purchase details add ho
        product = instance.product_id
        product.stock_quantity += instance.qty
        product.save()

# Sales hone ke baad stock update karega
@receiver(post_save, sender=sales_details)
def update_stock_after_sales(sender, instance, created, **kwargs):
    if created:  # Jab naye sales details add ho
        product = instance.product_id
        if product.stock_quantity >= instance.qty:
            product.stock_quantity -= instance.qty
            product.save()
        else:
            print("Error: Not enough stock available!")
