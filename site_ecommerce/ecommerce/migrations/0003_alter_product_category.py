# Generated by Django 4.2.13 on 2024-05-14 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('CM', 'Collection Men'), ('CW', 'Collection Women'), ('CT', 'Collection Watches'), ('CB', 'Collection bag'), ('CS', 'Collection shoes')], max_length=2),
        ),
    ]
