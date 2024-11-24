from django import forms
from .models import Product, TopUpPackage, Transaction, Payment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'category']

class TopUpPackageForm(forms.ModelForm):
    class Meta:
        model = TopUpPackage
        fields = ['product', 'package_name', 'amount', 'price', 'agent_price']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['package', 'transaction_proof']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']