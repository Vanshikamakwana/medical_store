# Generated by Django 5.1.5 on 2025-02-12 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0014_batch_batch_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='batch_number',
            field=models.CharField(default=0, max_length=50),
        ),
    ]
