from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/agent/', views.dashboard_agent, name='dashboard_agent'),
    path('dashboard/player/', views.dashboard_player, name='dashboard_player'),
    
    # Home
    path('', views.homepage, name='homepage'),
    
    # Product and Package URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/packages/', views.package_list, name='package_list'),
    
    # Transaction URLs
    path('transactions/create/<int:package_id>/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:transaction_id>/update/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:transaction_id>/delete/', views.transaction_delete, name='transaction_delete'),
]