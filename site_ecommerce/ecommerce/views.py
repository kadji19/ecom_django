from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Cart, CartItem, Color, Product, Size
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.
""" def base(request, *args, **kwargs):
    return render(request, "ecommerce/index.html", {}) """

def home(request, *args, **kwargs):
    return render(request, "ecommerce/home.html", {})

def about(request, *args, **kwargs): 
    return render(request, "ecommerce/about.html", {})

def contact(request, *args, **kwargs): 
    return render(request, "ecommerce/contact.html", {})


def product_list(request):
    product = Product.objects.all()
    return render(request, 'ecommerce/product.html', {'product': product})

class ProductDetail(View):
 def get(self, request,pk):
    product=Product.objects.get(pk=pk)
    return render(request, 'ecommerce/product_detail.html', locals())
 
class CategoryView(View):
 def get(self, request, val):
        product=Product.objects.filter(category=val) 
        return render(request, "ecommerce/product.html", locals())
        title=Product.objects.filter(category=val).values('title')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'ecommerce/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'ecommerce/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    size = Size.objects.get(id=size_id) if size_id else None
    color = Color.objects.get(id=color_id) if color_id else None

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size,
        color=color,
    )
    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'ecommerce/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

def update_cart(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, user=request.user)
        for item in cart.items.all():
            item.quantity = int(request.POST.get(f'quantity-{item.id}', item.quantity))
            item.save()
    return redirect('cart_detail')