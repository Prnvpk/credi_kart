from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('shopkeeper', 'credit_limit', 'city')

    def __init__(self, *args, **kwargs):
        shopkeeper = kwargs.pop('shopkeeper', None)
        super().__init__(*args, **kwargs)
        if shopkeeper:
            self.fields['shopkeeper'].queryset = type(shopkeeper).objects.filter(pk=shopkeeper.pk)
            self.fields['shopkeeper'].initial = shopkeeper
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
