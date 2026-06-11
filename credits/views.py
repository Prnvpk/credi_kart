from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required
from accounts.models import User
from notifications.models import Notification
from .models import CreditTransaction


@login_required
def credit_list(request):
    if request.user.is_shopkeeper:
        credits = CreditTransaction.objects.filter(shopkeeper=request.user.shopkeeper_profile)
    elif request.user.is_customer:
        credits = CreditTransaction.objects.filter(customer=request.user.customer_profile)
    else:
        credits = CreditTransaction.objects.all()
    for credit in credits:
        if credit.is_overdue and credit.status != CreditTransaction.OVERDUE:
            credit.refresh_status()
    return render(request, 'credits/list.html', {'credits': credits.select_related('customer__user', 'shopkeeper', 'order')})


@login_required
@role_required(User.CUSTOMER)
def request_extension(request, pk):
    credit = get_object_or_404(CreditTransaction, pk=pk, customer=request.user.customer_profile)
    if request.method == 'POST':
        credit.status = CreditTransaction.EXTENSION_REQUESTED
        credit.save(update_fields=['status', 'updated_at'])
        Notification.objects.create(
            user=credit.shopkeeper.user,
            title='Extension requested',
            message=f'{credit.customer} requested more time for order {credit.order.order_number}.',
            notification_type=Notification.WARNING,
        )
        messages.success(request, 'Extension request sent to the shopkeeper.')
    return redirect('credits:list')

# Create your views here.
