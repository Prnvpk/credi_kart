from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from credits.models import CreditTransaction
from notifications.models import Notification
from .forms import PaymentForm
from .models import Payment


@login_required
def payment_list(request):
    if request.user.is_shopkeeper:
        payments = Payment.objects.filter(shopkeeper=request.user.shopkeeper_profile)
    elif request.user.is_customer:
        payments = Payment.objects.filter(customer=request.user.customer_profile)
    else:
        payments = Payment.objects.all()
    return render(request, 'payments/list.html', {'payments': payments.select_related('customer__user', 'shopkeeper', 'credit')})


@login_required
def record_payment(request, credit_id):
    credit = get_object_or_404(CreditTransaction.objects.select_related('customer__user', 'shopkeeper__user'), pk=credit_id)
    if request.user.is_customer and credit.customer != request.user.customer_profile:
        messages.error(request, 'You cannot pay this credit.')
        return redirect('credits:list')
    if request.user.is_shopkeeper and credit.shopkeeper != request.user.shopkeeper_profile:
        messages.error(request, 'You cannot record this payment.')
        return redirect('credits:list')
    form = PaymentForm(request.POST or None, credit=credit)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            payment = form.save(commit=False)
            payment.credit = credit
            payment.customer = credit.customer
            payment.shopkeeper = credit.shopkeeper
            payment.save()
            credit.amount_paid += payment.amount
            credit.save(update_fields=['amount_paid', 'updated_at'])
            credit.refresh_status()
            credit.customer.outstanding_balance = max(credit.customer.outstanding_balance - payment.amount, 0)
            credit.customer.save(update_fields=['outstanding_balance'])
            recipient = credit.shopkeeper.user if request.user.is_customer else credit.customer.user
            Notification.objects.create(
                user=recipient,
                title='Payment recorded',
                message=f'Payment of Rs. {payment.amount} was recorded for {credit.order.order_number}.',
                notification_type=Notification.SUCCESS,
            )
        messages.success(request, 'Payment recorded successfully.')
        return redirect('credits:list')
    return render(request, 'payments/form.html', {'form': form, 'credit': credit})


