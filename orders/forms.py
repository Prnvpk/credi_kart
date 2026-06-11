from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Order


def _add_one_month(value):
    month = value.month + 1
    year = value.year
    if month > 12:
        month = 1
        year += 1
    month_lengths = {
        1: 31,
        2: 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31,
    }
    return value.replace(year=year, month=month, day=min(value.day, month_lengths[month]))


class CheckoutForm(forms.Form):
    TEN_DAYS = '10_days'
    ONE_MONTH = '1_month'
    CUSTOM = 'custom'
    REPAYMENT_TIMELINE_CHOICES = (
        (TEN_DAYS, '10 days'),
        (ONE_MONTH, '1 month'),
        (CUSTOM, 'Custom date'),
    )

    payment_type = forms.ChoiceField(
        choices=Order.PAYMENT_CHOICES,
        widget=forms.RadioSelect,
    )
    payment_method = forms.ChoiceField(
        choices=(('', 'Select payment method'),) + Order.PAYMENT_METHOD_CHOICES,
        required=False,
        label='Payment method',
    )
    upi_id = forms.CharField(
        required=False,
        label='UPI ID',
        widget=forms.TextInput(attrs={'placeholder': 'name@bank'}),
    )
    card_holder = forms.CharField(
        required=False,
        label='Card holder name',
        widget=forms.TextInput(attrs={'placeholder': 'Name on card'}),
    )
    card_number = forms.CharField(
        required=False,
        label='Card number',
        widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456', 'inputmode': 'numeric'}),
    )
    card_expiry = forms.CharField(
        required=False,
        label='Expiry',
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}),
    )
    card_cvv = forms.CharField(
        required=False,
        label='CVV',
        widget=forms.PasswordInput(attrs={'placeholder': '123', 'inputmode': 'numeric'}),
    )
    repayment_timeline = forms.ChoiceField(
        choices=REPAYMENT_TIMELINE_CHOICES,
        required=False,
        label='Repayment timeline',
        widget=forms.RadioSelect,
    )
    due_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_type'].initial = Order.READY
        self.fields['repayment_timeline'].initial = self.TEN_DAYS
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        self.fields['payment_type'].widget.attrs['class'] = 'payment-choice-list'
        self.fields['repayment_timeline'].widget.attrs['class'] = 'timeline-choice-list'

    def clean(self):
        cleaned = super().clean()
        payment_type = cleaned.get('payment_type')
        payment_method = cleaned.get('payment_method')
        if payment_type == Order.PAY_LATER:
            today = timezone.localdate()
            repayment_timeline = cleaned.get('repayment_timeline')
            if repayment_timeline == self.TEN_DAYS:
                cleaned['due_date'] = today + timedelta(days=10)
            elif repayment_timeline == self.ONE_MONTH:
                cleaned['due_date'] = _add_one_month(today)
            due_date = cleaned.get('due_date')
            if not due_date:
                self.add_error('due_date', 'Due date is required for pay-later checkout.')
            elif due_date < timezone.localdate():
                self.add_error('due_date', 'Due date cannot be in the past.')
        elif payment_type == Order.READY:
            if not payment_method:
                self.add_error('payment_method', 'Choose UPI or card payment.')
            elif payment_method == Order.UPI:
                upi_id = cleaned.get('upi_id', '').strip()
                if not upi_id:
                    self.add_error('upi_id', 'Enter a UPI ID.')
                elif '@' not in upi_id:
                    self.add_error('upi_id', 'Enter a valid UPI ID, for example name@bank.')
            elif payment_method == Order.CARD:
                card_number = ''.join(ch for ch in cleaned.get('card_number', '') if ch.isdigit())
                card_cvv = cleaned.get('card_cvv', '')
                for field in ('card_holder', 'card_number', 'card_expiry', 'card_cvv'):
                    if not cleaned.get(field):
                        self.add_error(field, 'This field is required for card payment.')
                if card_number and not 12 <= len(card_number) <= 19:
                    self.add_error('card_number', 'Enter a valid card number.')
                if card_cvv and (not card_cvv.isdigit() or len(card_cvv) not in (3, 4)):
                    self.add_error('card_cvv', 'Enter a valid CVV.')
        return cleaned
