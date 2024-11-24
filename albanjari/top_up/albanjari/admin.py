from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Category, Product, TopUpPackage, UserProfile, Transaction, Payment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        return obj.userprofile.role if hasattr(obj, 'userprofile') else '-'
    get_role.short_description = 'Role'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('product_name', 'description')

class TopUpPackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'product', 'amount', 'price', 'agent_price')
    list_filter = ('product',)
    search_fields = ('package_name',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'user', 'package', 'status', 'transaction_date', 'total_price')
    list_filter = ('status', 'transaction_date')
    search_fields = ('user__username', 'transaction_id')
    readonly_fields = ('transaction_date',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'transaction', 'payment_method', 'payment_date', 'payment_status')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('transaction__transaction_id', 'payment_id')
    readonly_fields = ('payment_date',)

# Unregister the default User admin
admin.site.unregister(User)

# Register models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(TopUpPackage, TopUpPackageAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Payment, PaymentAdmin)