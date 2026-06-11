from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from accounts.decorators import approved_shopkeeper_required
from credits.models import CreditTransaction
from orders.models import Order
from payments.models import Payment


@login_required
@approved_shopkeeper_required
def shop_reports(request):
    shop = request.user.shopkeeper_profile
    orders = Order.objects.filter(shopkeeper=shop)
    credits = CreditTransaction.objects.filter(shopkeeper=shop)
    payments = Payment.objects.filter(shopkeeper=shop)
    context = {
        'orders': orders[:20],
        'credits': credits.select_related('customer__user')[:20],
        'sales_total': orders.aggregate(total=Sum('total_amount'))['total'] or 0,
        'payment_total': payments.aggregate(total=Sum('amount'))['total'] or 0,
        'outstanding_total': sum(c.remaining_balance for c in credits),
    }
    return render(request, 'reports/shop_reports.html', context)
