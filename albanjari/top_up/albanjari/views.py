from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login as auth_login
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, ProtectedError
from django.core.paginator import Paginator
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, TopUpPackage, Transaction, Payment, Category, UserProfile
from .forms import (
    ProductForm, 
    TopUpPackageForm, 
    TransactionForm, 
    PaymentForm, 
    RegistrationForm,
    CustomAuthenticationForm,
    TopUpPackageInlineForm
)
from django.contrib.auth import authenticate, login

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        user = self.request.user
        if is_admin(user): 
            return reverse('dashboard_admin')
        elif hasattr(user, 'userprofile'):
            if user.userprofile.role == 'AGENT':
                return reverse('dashboard_agent')
            elif user.userprofile.role == 'PLAYER':
                return reverse('dashboard_player')
        return reverse('dashboard_player')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response

def is_player_or_agent(user):
    """Check if user is either a player or an agent"""
    return user.groups.filter(name__in=['Player', 'Agent']).exists()

def is_agent(user):
    """Check if user is an agent"""
    return user.groups.filter(name='Agent').exists()

def is_admin(user):
    """Check if user is an admin"""
    return user.is_staff or user.is_superuser or user.groups.filter(name='Admin').exists()

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our platform.')
            
            if user.userprofile.role == 'AGENT':
                return redirect('dashboard_agent')
            else:
                return redirect('dashboard_player')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def homepage(request):
    """Homepage view showing categories and featured products"""
    categories = Category.objects.prefetch_related('product_set').all()
    return render(request, 'home/index.html', {'categories': categories})

@login_required
def dashboard(request):
    """Main dashboard that redirects based on user role"""
    if is_admin(request.user):
        return redirect('dashboard_admin')
    elif is_agent(request.user):
        return redirect('dashboard_agent')
    else:
        return redirect('dashboard_player')

@login_required
@user_passes_test(is_admin)
def dashboard_admin(request):
    """Admin dashboard view"""
    transactions = Transaction.objects.all().order_by('-transaction_date')
    products = Product.objects.all()
    pending_transactions = transactions.filter(status='PENDING').count() 
    
    context = {
        'transactions': transactions,
        'products': products,
        'total_transactions': transactions.count(),
        'pending_transactions': pending_transactions,
        'is_admin': True 
    }
    return render(request, 'dashboard/admin.html', context)

@login_required
@user_passes_test(is_agent)
def dashboard_agent(request):
    """Agent dashboard view"""
    agent_transactions = Transaction.objects.filter(user=request.user)
    total_earnings = sum(t.total_price for t in agent_transactions)
    context = {
        'transactions': agent_transactions,
        'total_earnings': total_earnings,
        'is_agent': True
    }
    return render(request, 'dashboard/agent.html', context)

@login_required
def dashboard_player(request):
    """Player dashboard view"""
    if not is_player_or_agent(request.user):
        return HttpResponseForbidden("Access denied.")
        
    player_transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': player_transactions,
        'is_agent': is_agent(request.user)
    }
    return render(request, 'dashboard/player.html', context)

@login_required
def product_list(request):
    """List products"""
    if not (is_player_or_agent(request.user) or is_admin(request.user)):  
        messages.error(request, "You don't have permission to view products.")
        return redirect('homepage')
    
    # Get the search query from the request
    query = request.GET.get('q', '')
    
    # Filter products based on the search query
    if query:
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.all() 
    context = {
        'products': products,
        'query': query,  
        'is_agent': is_agent(request.user),
        'is_admin': is_admin(request.user)  
    }
    
    return render(request, 'product/index.html', context)

@login_required
def package_list(request, product_id):
    """List packages for a specific product with role-based pricing"""
    if not (is_player_or_agent(request.user) or is_admin(request.user)):  
        messages.error(request, "You don't have permission to view packages.")
        return redirect('homepage')
    
    product = get_object_or_404(Product, product_id=product_id)
    packages = TopUpPackage.objects.filter(product=product)
    
    is_agent_user = is_agent(request.user)
    for package in packages:
        if is_agent_user:
            package.display_price = float(package.price) * 0.9  
            package.savings = float(package.price) * 0.1  
        else:
            package.display_price = float(package.price)
            package.savings = 0
    
    context = {
        'product': product,
        'packages': packages,
        'is_agent': is_agent_user,
        'is_admin': is_admin(request.user) 
    }
    return render(request, 'package/index.html', context)

@login_required
@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('dashboard_admin')
    else:
        form = ProductForm()
    
    return render(request, 'product/create.html', {
        'form': form,
        'is_admin': True
    })

@login_required
@user_passes_test(is_admin)
def package_update(request, package_id):
    package = get_object_or_404(TopUpPackage, package_id=package_id)
    
    if request.method == 'POST':
        form = TopUpPackageInlineForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package updated successfully!')
        return redirect('product_update', product_id=package.product.product_id)
    
    return redirect('product_update', product_id=package.product.product_id)

@login_required
@user_passes_test(is_admin)
def product_update(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    packages = TopUpPackage.objects.filter(product=product)
    package_form = TopUpPackageInlineForm()  # Initialize form here, outside if/else
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if 'add_package' in request.POST:
            package_form = TopUpPackageInlineForm(request.POST)
            if package_form.is_valid():
                package = package_form.save(commit=False)
                package.product = product
                package.save()
                messages.success(request, 'Package added successfully!')
                return redirect('product_update', product_id=product_id)
        elif form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard_admin')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product/update.html', {
        'form': form,
        'package_form': package_form,
        'product': product,
        'packages': packages,
        'is_admin': True
    })

@login_required
@user_passes_test(is_admin)
def package_delete(request, package_id):
    package = get_object_or_404(TopUpPackage, package_id=package_id)
    product_id = package.product.product_id
    
    if request.method == 'POST':
        package.delete()
        messages.success(request, 'Package deleted successfully!')
        return redirect('product_update', product_id=product_id)
    
    return redirect('product_update', product_id=product_id)

@login_required
@user_passes_test(is_admin)
def product_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == 'POST':
        try:
            product.delete()
            messages.success(request, 'Product deleted successfully!')
        except ProtectedError:
            messages.error(request, 'Cannot delete this product because it has related transactions.')
        return redirect('dashboard_admin')
    
    return render(request, 'product/delete.html', {
        'product': product,
        'is_admin': True
    })

@login_required
@user_passes_test(is_admin)
def product_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('dashboard_admin')
    
    return render(request, 'admin/product_confirm_delete.html', {
        'product': product,
        'is_admin': True
    })

@login_required
@user_passes_test(is_admin)
def confirm_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['COMPLETED', 'FAILED']:
            transaction.status = new_status
            transaction.save()
            messages.success(request, f'Transaction {transaction_id} has been {new_status.lower()}!')
            
            if new_status == 'COMPLETED':
                messages.success(request, f'Transaction for {transaction.package.package_name} has been completed.')
            else:
                messages.error(request, f'Transaction for {transaction.package.package_name} has failed.')
                
        return redirect('dashboard_admin')
    
    return render(request, 'admin/confirm_transaction.html', {
        'transaction': transaction,
        'is_admin': True
    })

@login_required
@user_passes_test(is_admin)
def transaction_delete(request, transaction_id):
    """Delete transaction (Admin only)"""
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('dashboard_admin')
    
    return render(request, 'transaction/delete.html', {'transaction': transaction})

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(user, 'userprofile'):
                    if user.userprofile.role == 'AGENT':
                        return redirect('dashboard_agent')
                    elif user.userprofile.role == 'ADMIN':
                        return redirect('dashboard_admin')
                return redirect('dashboard_player')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def transaction_list(request):
    """List user's transactions"""
    if not (is_player_or_agent(request.user) or is_admin(request.user)):
        messages.error(request, "You don't have permission to view transactions.")
        return redirect('homepage')
    
    if is_admin(request.user):
        transactions = Transaction.objects.all().order_by('-transaction_date')
    else:
        transactions = Transaction.objects.filter(user=request.user).order_by('-transaction_date')
    
    context = {
        'transactions': transactions,
        'is_agent': is_agent(request.user),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'transaction/index.html', context)

@login_required
def create_transaction(request, package_id):
    """Create a new transaction"""
    if not (is_player_or_agent(request.user) or is_admin(request.user)):
        messages.error(request, "You don't have permission to create transactions.")
        return redirect('homepage')
    
    package = get_object_or_404(TopUpPackage, package_id=package_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.package = package
            
            if is_agent(request.user):
                transaction.total_price = float(package.price) * 0.9 
            else:
                transaction.total_price = package.price
            
            transaction.status = 'PENDING'
            transaction.save()
            
            messages.success(request, 'Transaction created successfully! Please wait for admin confirmation.')
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    if is_agent(request.user):
        package.savings = float(package.price) * 0.1
        package.agent_price = float(package.price) * 0.9
    
    context = {
        'form': form,
        'package': package,
        'is_agent': is_agent(request.user),
        'is_admin': is_admin(request.user)
    }
    return render(request, 'transaction/create.html', context)

@login_required
@user_passes_test(is_admin)
def transaction_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['COMPLETED', 'FAILED']:
            transaction.status = new_status
            transaction.save()
            
            status_display = 'completed' if new_status == 'COMPLETED' else 'marked as failed'
            messages.success(request, f'Transaction has been {status_display} successfully!')
            
            if new_status == 'COMPLETED':
                Payment.objects.create(
                    transaction=transaction,
                    payment_method='Bank Transfer',
                    payment_status='SUCCESS'
                )
        
        return redirect('dashboard_admin')
    
    return redirect('dashboard_admin')