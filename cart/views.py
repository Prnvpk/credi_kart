from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from products.models import Product
from .models import Cart, CartItem


def get_cart(user):
    return Cart.objects.get_or_create(customer=user.customer_profile)[0]


@login_required
@role_required(User.CUSTOMER)
def cart_detail(request):
    cart = get_cart(request.user)
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
@role_required(User.CUSTOMER)
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True, stock__gt=0)
    cart = get_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    try:
        quantity = max(int(request.GET.get('quantity', 1)), 1)
    except (TypeError, ValueError):
        quantity = 1
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.quantity = min(item.quantity, product.stock)
    item.save()
    messages.success(request, f'{product.name} added to cart.')
    return redirect('cart:detail')


@login_required
@role_required(User.CUSTOMER)
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__customer=request.user.customer_profile)
    if request.method == 'POST':
        quantity = max(int(request.POST.get('quantity', 1)), 0)
        if quantity == 0:
            item.delete()
            messages.info(request, 'Item removed from cart.')
        else:
            item.quantity = min(quantity, item.product.stock)
            item.save()
            messages.success(request, 'Cart updated.')
    return redirect('cart:detail')

# Create your views here.
