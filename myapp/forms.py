from django import forms # type: ignore
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['item', 'amount', 'customer']