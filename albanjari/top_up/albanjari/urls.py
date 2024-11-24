from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        next_page='homepage'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='homepage'
    ), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/agent/', views.dashboard_agent, name='dashboard_agent'),
    path('dashboard/player/', views.dashboard_player, name='dashboard_player'),
    path('', views.homepage, name='homepage'),
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:product_id>/update/', views.product_update, name='product_update'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:product_id>/packages/', views.package_list, name='package_list'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/create/<int:package_id>/', views.create_transaction, name='create_transaction'),
    path('transactions/<int:transaction_id>/update/', views.transaction_update, name='transaction_update'),
    path('transactions/<int:transaction_id>/delete/', views.transaction_delete, name='transaction_delete'),
]