# Generated by Django 5.1.5 on 2025-02-04 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0006_remove_product_sales_id_remove_product_sel_ret_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=50),
        ),
    ]
