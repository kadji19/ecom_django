# Generated by Django 4.2.13 on 2024-05-20 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
    ]
