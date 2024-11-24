from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
from .models import Product, TopUpPackage, Transaction, Payment
from .forms import ProductForm, TopUpPackageForm, TransactionForm, PaymentForm
from .models import Category 


# def homepage(request):
#     """Public homepage accessible to all users"""
#     products = Product.objects.all()
#     return render(request, 'homepage/index.html', {'products': products})

def homepage(request):
    categories = Category.objects.prefetch_related('product_set').all()
    return render(request, 'home/index.html', {'categories': categories})

@login_required
def dashboard(request):
    """Main dashboard that redirects based on user role"""
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Agent').exists():
        return redirect('dashboard_agent')
    elif user.groups.filter(name='Player').exists():
        return redirect('dashboard_player')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
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
def dashboard_agent(request):
    """Agent dashboard view"""
    agent_transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': agent_transactions,
        'total_earnings': sum(t.total_price for t in agent_transactions)
    }
    return render(request, 'dashboard/agent.html', context)


@login_required
def dashboard_player(request):
    """Player dashboard view"""
    player_transactions = Transaction.objects.filter(user=request.user)
    context = {
        'transactions': player_transactions
    }
    return render(request, 'dashboard/player.html', context)

# READ Views
@login_required
def product_list(request):
    """List products with search functionality"""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__category_name__icontains=query)
        )
    else:
        products = Product.objects.all()
    return render(request, 'product/index.html', {'products': products, 'query': query})


@login_required
def package_list(request, product_id):
    """List packages for a specific product with role-based pricing"""
    packages = TopUpPackage.objects.filter(product_id=product_id)
    is_agent = request.user.groups.filter(name='Agent').exists()
    
    for package in packages:
        package.display_price = package.agent_price if is_agent else package.price
        
    return render(request, 'package/index.html', {'packages': packages})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'transaction/index.html', {'transactions': transactions})

# CREATE Views
@login_required
def create_transaction(request, package_id):
    """Create a new transaction with role-based pricing"""
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.package_id = package_id
            package = TopUpPackage.objects.get(id=package_id)
            
            # Set price based on user role
            if request.user.groups.filter(name='Agent').exists():
                transaction.total_price = package.agent_price
            else:
                transaction.total_price = package.price
                
            transaction.save()
            messages.success(request, 'Transaction created successfully!')
            return redirect('dashboard')
    else:
        form = TransactionForm(initial={'package': package_id})
    
    return render(request, 'transaction/create.html', {'form': form})

# UPDATE
@login_required
def transaction_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    
    # Hanya admin yang bisa update status transaksi
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to update this transaction.')
        return redirect('transaction_list')
        
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'transaction/update.html', {'form': form, 'transaction': transaction})

# DELETE
@login_required
def transaction_update(request, transaction_id):
    """Update transaction status (Admin only)"""
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You do not have permission to update transactions.")
        
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
def transaction_delete(request, transaction_id):
    """Delete transaction (Admin only)"""
    if not request.user.groups.filter(name='Admin').exists():
        return HttpResponseForbidden("You do not have permission to delete transactions.")
        
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('dashboard_admin')
    
    return render(request, 'transaction/delete.html', {'transaction': transaction}) 