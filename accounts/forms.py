from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Shopkeeper, User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=((User.CUSTOMER, 'Customer'), (User.SHOPKEEPER, 'Shopkeeper')), initial=User.CUSTOMER)
    shop_name = forms.CharField(required=False)
    licence_document = forms.FileField(
        required=False,
        help_text='Required for shopkeeper approval. Upload PDF, JPG, or PNG.',
        widget=forms.FileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'maxlength': '10',
            'pattern': r'\d{10}',
            'inputmode': 'numeric',
            'placeholder': '10 digit phone number',
        }),
    )
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'phone', 'address', 'role', 'shop_name', 'licence_document', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('role') == User.SHOPKEEPER:
            if not cleaned.get('shop_name'):
                self.add_error('shop_name', 'Shop name is required for shopkeeper accounts.')
            if not cleaned.get('licence_document'):
                self.add_error('licence_document', 'Licence document is required for shopkeeper approval.')
        return cleaned

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not phone.isdigit():
            raise forms.ValidationError('Phone number must contain digits only.')
        if phone and len(phone) != 10:
            raise forms.ValidationError('Phone number must be exactly 10 digits.')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        user.phone = self.cleaned_data.get('phone', '')
        user.address = self.cleaned_data.get('address', '')
        user.is_approved = user.role == User.CUSTOMER
        if commit:
            user.save()
            if user.role == User.SHOPKEEPER:
                Shopkeeper.objects.create(
                    user=user,
                    shop_name=self.cleaned_data['shop_name'],
                    licence_document=self.cleaned_data.get('licence_document'),
                    is_active=False,
                )
        return user


class ShopkeeperApprovalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_approved', 'is_active')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'address')
        widgets = {'address': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')


class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = Shopkeeper
        fields = ('shop_name', 'business_registration', 'licence_document', 'credit_limit', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
