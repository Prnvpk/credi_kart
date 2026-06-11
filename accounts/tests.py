from django.test import TestCase

from .forms import RegisterForm
from .models import User


class RegisterFormTests(TestCase):
    def form_data(self, **overrides):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuser',
            'email': 'test@example.com',
            'phone': '9876543210',
            'address': 'Test address',
            'role': User.CUSTOMER,
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        data.update(overrides)
        return data

    def test_register_accepts_exactly_10_digit_phone(self):
        form = RegisterForm(data=self.form_data())

        self.assertTrue(form.is_valid())

    def test_register_rejects_phone_with_less_than_10_digits(self):
        form = RegisterForm(data=self.form_data(phone='987654321'))

        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)

    def test_register_rejects_non_digit_phone(self):
        form = RegisterForm(data=self.form_data(phone='98765abc10'))

        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
