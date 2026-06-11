from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.crypto import get_random_string

from accounts.decorators import role_required
from accounts.models import User
from cart.models import Cart
from credits.models import CreditTransaction
from notifications.models import Notification
from .forms import CheckoutForm
from .models import Order, OrderItem


def _fake_payment_reference(payment_method):
    prefix = 'UPI' if payment_method == Order.UPI else 'CARD'
    return f'{prefix}-{get_random_string(12).upper()}'


@login_required
def order_list(request):
    if request.user.is_shopkeeper:
        orders = Order.objects.filter(shopkeeper=request.user.shopkeeper_profile)
    elif request.user.is_customer:
        orders = Order.objects.filter(customer=request.user.customer_profile)
    else:
        orders = Order.objects.all()
    return render(request, 'orders/list.html', {'orders': orders.select_related('customer__user', 'shopkeeper')})


@login_required
@role_required(User.CUSTOMER)
def checkout(request):
    cart = get_object_or_404(Cart, customer=request.user.customer_profile)
    items = list(cart.items.select_related('product', 'product__shopkeeper'))
    if not items:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')
    shopkeeper = items[0].product.shopkeeper
    if any(item.product.shopkeeper_id != shopkeeper.id for item in items):
        messages.error(request, 'Checkout supports one shop at a time. Please remove items from other shops.')
        return redirect('cart:detail')
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        total = Decimal(cart.total_amount)
        payment_type = form.cleaned_data['payment_type']
        payment_method = form.cleaned_data.get('payment_method', '') if payment_type == Order.READY else ''
        with transaction.atomic():
            order = Order.objects.create(
                customer=request.user.customer_profile,
                shopkeeper=shopkeeper,
                order_number=f'CK{get_random_string(8).upper()}',
                payment_type=payment_type,
                payment_method=payment_method,
                payment_status=Order.PAYMENT_PAID if payment_type == Order.READY else Order.PAYMENT_CREDIT,
                payment_reference=_fake_payment_reference(payment_method) if payment_type == Order.READY else '',
                total_amount=total,
                due_date=form.cleaned_data.get('due_date'),
                notes=form.cleaned_data.get('notes', ''),
            )
            if order.customer.shopkeeper_id is None:
                order.customer.shopkeeper = shopkeeper
                order.customer.save(update_fields=['shopkeeper'])
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    unit_price=item.product.price,
                    quantity=item.quantity,
                    line_total=item.line_total,
                )
                item.product.stock -= item.quantity
                item.product.save(update_fields=['stock'])
            if order.payment_type == Order.PAY_LATER:
                credit = CreditTransaction.objects.create(
                    order=order,
                    customer=order.customer,
                    shopkeeper=shopkeeper,
                    principal_amount=total,
                    due_date=order.due_date,
                )
                order.customer.outstanding_balance += total
                order.customer.save(update_fields=['outstanding_balance'])
                Notification.objects.create(
                    user=shopkeeper.user,
                    title='New pay-later order',
                    message=f'{order.customer} created credit order {order.order_number}.',
                    notification_type=Notification.INFO,
                )
            cart.items.all().delete()
        if order.payment_type == Order.READY:
            messages.success(request, f'Fake payment successful. Transaction ID: {order.payment_reference}')
        else:
            messages.success(request, 'Order placed successfully.')
        return redirect('orders:receipt', pk=order.pk)
    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form})


@login_required
def receipt(request, pk):
    order = get_object_or_404(Order.objects.select_related('customer__user', 'shopkeeper'), pk=pk)
    if request.user.is_customer and order.customer != request.user.customer_profile:
        messages.error(request, 'You cannot view this receipt.')
        return redirect('orders:list')
    if request.user.is_shopkeeper and order.shopkeeper != request.user.shopkeeper_profile:
        messages.error(request, 'You cannot view this receipt.')
        return redirect('orders:list')
    return render(request, 'orders/receipt.html', {'order': order})

