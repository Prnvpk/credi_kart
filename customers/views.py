from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.decorators import approved_shopkeeper_required
from .models import Customer


@login_required
@approved_shopkeeper_required
def customer_list(request):
    query = request.GET.get('q', '')
    customers = Customer.objects.filter(shopkeeper=request.user.shopkeeper_profile).select_related('user')
    if query:
        customers = customers.filter(user__username__icontains=query)
    return render(request, 'customers/list.html', {'customers': customers, 'query': query})

# Create your views here.
