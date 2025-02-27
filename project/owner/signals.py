# your_app_name/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import sales_details, Batch
from django.db import transaction

@receiver(post_save, sender=sales_details)
def reduce_stock(sender, instance, **kwargs):
    """
    This signal is triggered when a new sale detail is added. 
    It reduces the stock quantity in the batches accordingly.
    """
    print(f"Sale recorded for product: {instance.product_id.product_name}")
    print(f"Order quantity: {instance.qty}")

    # Get the product and the ordered quantity
    product = instance.product_id
    ordered_quantity = instance.qty

    # Get the batches for this product, ordered by expiry date (FIFO approach)
    batches = Batch.objects.filter(product=product).order_by('batch_expiry_date')

    for batch in batches:
        print(f"Checking batch: {batch.batch_number}, available quantity: {batch.batch_quantity}")

        if ordered_quantity <= 0:
            break  # No more stock to deduct

        if batch.batch_quantity >= ordered_quantity:
            print(f"Reducing stock from batch: {batch.batch_number}")
            batch.batch_quantity -= ordered_quantity
            batch.save()
            ordered_quantity = 0
        else:
            ordered_quantity -= batch.batch_quantity
            batch.batch_quantity = 0
            batch.save()

    # If there is still remaining quantity, raise an error
    if ordered_quantity > 0:
        print(f"Not enough stock for product {product.product_name}")
        raise ValueError(f"Not enough stock available for {product.product_name}!")


# your_app_name/signals.py


@receiver(post_save, sender=sales_details)
def reduce_stock(sender, instance, **kwargs):
    """
    This signal is triggered when a new sale detail is added. 
    It reduces the stock quantity in the batches accordingly.
    """
    with transaction.atomic():
        print(f"Sale recorded for product: {instance.product_id.product_name}")
        print(f"Order quantity: {instance.qty}")

        product = instance.product_id
        ordered_quantity = instance.qty
        batches = Batch.objects.filter(product=product).order_by('batch_expiry_date')

        for batch in batches:
            print(f"Checking batch: {batch.batch_number}, available quantity: {batch.batch_quantity}")

            if ordered_quantity <= 0:
                break

            if batch.batch_quantity >= ordered_quantity:
                print(f"Reducing stock from batch: {batch.batch_number}")
                batch.batch_quantity -= ordered_quantity
                batch.save()
                ordered_quantity = 0
            else:
                ordered_quantity -= batch.batch_quantity
                batch.batch_quantity = 0
                batch.save()

        if ordered_quantity > 0:
            print(f"Not enough stock for product {product.product_name}")
            raise ValueError(f"Not enough stock available for {product.product_name}!")
