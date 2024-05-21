from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.
CATEGORY_CHOICES=(
 ('CM', 'Collection Men'),
 ('CW', 'Collection Women'),
 ('CT', 'Collection Watches'),
 ('CB', 'Collection bag'),
 ('CS', 'Collection shoes'),
)


class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
@receiver(post_migrate)
def create_initial_sizes_and_colors(sender, **kwargs):
    if sender.name == 'ecommerce':
        # Création des tailles
        Size.objects.get_or_create(name='S')
        Size.objects.get_or_create(name='M')
        Size.objects.get_or_create(name='L')
        Size.objects.get_or_create(name='XL')
        Size.objects.get_or_create(name='XXL')

        # Création des couleurs
        Color.objects.get_or_create(name='Red')
        Color.objects.get_or_create(name='Blue')
        Color.objects.get_or_create(name='green')
        Color.objects.get_or_create(name='gray')
        Color.objects.get_or_create(name='white')
        Color.objects.get_or_create(name='Black')

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image=models.ImageField(upload_to='product')
    sizes = models.ManyToManyField(Size, blank=True, related_name='products')
    colors = models.ManyToManyField(Color, blank=True, related_name='products')

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, blank=True, null=True, on_delete=models.SET_NULL)
    color = models.ForeignKey(Color, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        variant_name = f"{self.product.name}"
        if self.size:
            variant_name += f" - {self.size.name}"
        if self.color:
            variant_name += f" - {self.color.name}"
        return variant_name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    tel = models.CharField(max_length=15)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Panier de {self.user.username}'
    
    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in {self.cart}'
    
    def get_cost(self):
        return self.quantity * self.product.price