from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import approved_shopkeeper_required, role_required
from accounts.models import User
from .forms import ProductForm
from .models import Product


@login_required
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.select_related('shopkeeper').filter(is_active=True, stock__gt=0)
    if request.user.is_shopkeeper:
        products = Product.objects.filter(shopkeeper=request.user.shopkeeper_profile)
    if query:
        products = products.filter(name__icontains=query)
    page = Paginator(products, 10).get_page(request.GET.get('page'))
    return render(request, 'products/list.html', {'page': page, 'query': query})


@login_required
@approved_shopkeeper_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.shopkeeper = request.user.shopkeeper_profile
        product.save()
        messages.success(request, 'Product added successfully.')
        return redirect('products:list')
    return render(request, 'products/form.html', {'form': form, 'title': 'Add Product'})


@login_required
@approved_shopkeeper_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, shopkeeper=request.user.shopkeeper_profile)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('products:list')
    return render(request, 'products/form.html', {'form': form, 'title': 'Edit Product'})


@login_required
@role_required(User.CUSTOMER)
def catalog(request):
    return product_list(request)
