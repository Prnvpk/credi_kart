from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import LoginForm, ProfileForm, RegisterForm, ShopProfileForm
from .models import Shopkeeper, User


class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_shopkeeper and not user.is_approved:
            messages.warning(self.request, 'Your shopkeeper account is waiting for admin approval.')
            return redirect('accounts:login')
        login(self.request, user)
        return redirect('dashboard:home')


class UserLogoutView(LogoutView):
    pass


def register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user.is_shopkeeper:
            messages.success(request, 'Registration submitted. Admin approval is required before login.')
            return redirect('accounts:login')
        login(request, user)
        messages.success(request, 'Welcome to CREDI-KART.')
        return redirect('dashboard:home')
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    shop_form = None
    if request.user.is_shopkeeper:
        shop_form = ShopProfileForm(request.POST or None, request.FILES or None, instance=request.user.shopkeeper_profile)
    if request.method == 'POST' and form.is_valid() and (shop_form is None or shop_form.is_valid()):
        form.save()
        if shop_form:
            shop_form.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form, 'shop_form': shop_form})


@login_required
@role_required(User.ADMIN)
def shopkeeper_approvals(request):
    shopkeepers = Shopkeeper.objects.select_related('user').order_by('-created_at')
    return render(request, 'accounts/shopkeeper_approvals.html', {'shopkeepers': shopkeepers})


@login_required
@role_required(User.ADMIN)
def toggle_shopkeeper(request, pk):
    shopkeeper = get_object_or_404(Shopkeeper.objects.select_related('user'), pk=pk)
    if request.method == 'POST':
        approve = request.POST.get('action') == 'approve'
        shopkeeper.is_active = approve
        shopkeeper.user.is_approved = approve
        shopkeeper.user.is_active = approve
        shopkeeper.user.save(update_fields=['is_approved', 'is_active'])
        shopkeeper.save(update_fields=['is_active'])
        messages.success(request, f'{shopkeeper.shop_name} has been {"approved" if approve else "deactivated"}.')
    return redirect('accounts:shopkeeper_approvals')

