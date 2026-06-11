from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.models import Shopkeeper, User
from credits.models import CreditTransaction
from orders.models import Order
from payments.models import Payment
from products.models import Product


@login_required
def home(request):
    user = request.user
    if user.is_platform_admin:
        return admin_dashboard(request)
    if user.is_shopkeeper:
        if not user.is_approved:
            return render(request, 'dashboard/pending_approval.html')
        return shopkeeper_dashboard(request)
    if user.is_customer:
        return customer_dashboard(request)
    return redirect('accounts:login')


def admin_dashboard(request):
    credits = CreditTransaction.objects.all()
    context = {
        'total_shopkeepers': Shopkeeper.objects.count(),
        'pending_shopkeepers': Shopkeeper.objects.filter(user__is_approved=False).count(),
        'total_customers': User.objects.filter(role=User.CUSTOMER).count(),
        'total_transactions': Order.objects.count(),
        'total_revenue': Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0,
        'overdue_credits': credits.filter(status=CreditTransaction.OVERDUE).count(),
        'outstanding_credit': sum(c.remaining_balance for c in credits),
        'repayments': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_orders': Order.objects.select_related('customer__user', 'shopkeeper')[:8],
    }
    return render(request, 'dashboard/admin.html', context)


def shopkeeper_dashboard(request):
    shop = request.user.shopkeeper_profile
    credits = CreditTransaction.objects.filter(shopkeeper=shop)
    context = {
        'shop': shop,
        'products_count': Product.objects.filter(shopkeeper=shop).count(),
        'low_stock_count': Product.objects.filter(shopkeeper=shop, stock__lte=5).count(),
        'customers_count': shop.customers.count(),
        'orders_count': Order.objects.filter(shopkeeper=shop).count(),
        'outstanding_credit': sum(c.remaining_balance for c in credits),
        'overdue_count': sum(1 for c in credits if c.is_overdue),
        'payments_today': Payment.objects.filter(shopkeeper=shop, paid_at__date=timezone.localdate()).aggregate(total=Sum('amount'))['total'] or 0,
        'recent_orders': Order.objects.filter(shopkeeper=shop).select_related('customer__user')[:8],
        'recent_credits': credits.select_related('customer__user', 'order')[:8],
    }
    return render(request, 'dashboard/shopkeeper.html', context)


def customer_dashboard(request):
    customer = request.user.customer_profile
    credits = CreditTransaction.objects.filter(customer=customer)
    products = Product.objects.select_related('shopkeeper').filter(is_active=True, stock__gt=0)
    category_labels = dict(Product.CATEGORY_CHOICES)
    categories = [
        {
            'key': item['category'],
            'label': category_labels.get(item['category'], item['category'].replace('_', ' ').title()),
            'total': item['total'],
        }
        for item in products.values('category').annotate(total=Count('id')).order_by('category')
    ]
    context = {
        'customer': customer,
        'orders_count': Order.objects.filter(customer=customer).count(),
        'outstanding_credit': sum(c.remaining_balance for c in credits),
        'overdue_count': sum(1 for c in credits if c.is_overdue),
        'payments_total': Payment.objects.filter(customer=customer).aggregate(total=Sum('amount'))['total'] or 0,
        'active_credits': credits.exclude(status=CreditTransaction.PAID).select_related('shopkeeper', 'order')[:8],
        'recent_orders': Order.objects.filter(customer=customer).select_related('shopkeeper')[:8],
        'featured_products': products[:8],
        'category_counts': categories,
    }
    return render(request, 'dashboard/customer.html', context)

# Create your views here.
