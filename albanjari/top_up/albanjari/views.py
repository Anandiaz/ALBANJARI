from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Product, TopUpPackage, Transaction, Payment, Category, UserProfile
from .forms import (
    ProductForm, 
    TopUpPackageForm, 
    TransactionForm, 
    PaymentForm, 
    RegistrationForm
)

def is_player_or_agent(user):
    """Check if user is either a player or an agent"""
    return user.groups.filter(name__in=['Player', 'Agent']).exists()

def is_agent(user):
    """Check if user is an agent"""
    return user.groups.filter(name='Agent').exists()

def is_admin(user):
    """Check if user is an admin"""
    return user.groups.filter(name='Admin').exists()

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our platform.')
            
            # Redirect based on role
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
    transactions = Transaction.objects.all()
    products = Product.objects.all()
    context = {
        'transactions': transactions,
        'products': products,
        'total_transactions': transactions.count()
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
    if not is_player_or_agent(request.user):
        messages.error(request, "You don't have permission to view products.")
        return redirect('homepage')
    
    products = Product.objects.all()
    context = {
        'products': products,
        'is_agent': is_agent(request.user)
    }
    return render(request, 'product/index.html', context)

@login_required
def package_list(request, product_id):
    """List packages for a specific product with role-based pricing"""
    if not is_player_or_agent(request.user):
        messages.error(request, "You don't have permission to view packages.")
        return redirect('homepage')
    
    product = get_object_or_404(Product, product_id=product_id)
    packages = TopUpPackage.objects.filter(product=product)
    
    # Calculate prices based on role
    is_agent_user = is_agent(request.user)
    for package in packages:
        if is_agent_user:
            package.display_price = float(package.price) * 0.9  # 10% discount
            package.savings = float(package.price) * 0.1  # Calculate savings
        else:
            package.display_price = float(package.price)
            package.savings = 0
    
    context = {
        'product': product,
        'packages': packages,
        'is_agent': is_agent_user
    }
    return render(request, 'package/index.html', context)

@login_required
def transaction_list(request):
    """List user's transactions"""
    if not is_player_or_agent(request.user):
        messages.error(request, "You don't have permission to view transactions.")
        return redirect('homepage')
    
    transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': transactions,
        'is_agent': is_agent(request.user)
    }
    return render(request, 'transaction/index.html', context)

@login_required
def create_transaction(request, package_id):
    """Create a new transaction"""
    if not is_player_or_agent(request.user):
        messages.error(request, "You don't have permission to create transactions.")
        return redirect('homepage')
    
    package = get_object_or_404(TopUpPackage, package_id=package_id)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.package = package
            
            # Set price based on role
            transaction.total_price = package.agent_price if is_agent(request.user) else package.price
            
            transaction.save()
            messages.success(request, 'Transaction created successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(initial={'package': package})
    
    context = {
        'form': form,
        'package': package,
        'is_agent': is_agent(request.user)
    }
    return render(request, 'transaction/create.html', context)

@login_required
@user_passes_test(is_admin)
def transaction_update(request, transaction_id):
    """Update transaction status (Admin only)"""
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('dashboard_admin')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'transaction/update.html', {'form': form})

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