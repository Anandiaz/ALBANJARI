from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from .models import Product, TopUpPackage, Transaction, Payment, UserProfile
from django.contrib.auth.forms import AuthenticationForm
from .models import TopUpPackage


class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('PLAYER', 'Player'),
        ('AGENT', 'Agent'),
    )

    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='PLAYER')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'phone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
           
            profile = UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone_number=self.cleaned_data['phone_number'],
                email=self.cleaned_data['email']
            )
            
            group_name = self.cleaned_data['role'].capitalize()
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'category', 'image']

class TopUpPackageForm(forms.ModelForm):
    class Meta:
        model = TopUpPackage
        fields = ['product', 'package_name', 'amount', 'price', 'agent_price']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_proof']
        widgets = {
            'transaction_proof': forms.FileInput(attrs={'class': 'form-control'})
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method']
        
class TopUpPackageInlineForm(forms.ModelForm):
    class Meta:
        model = TopUpPackage
        fields = ['package_name', 'amount', 'price', 'agent_price']

class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form"""
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def get_user(self):
        return self.user_cache