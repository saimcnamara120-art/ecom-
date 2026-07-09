"""URL patterns for the marketplace application."""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stores/', views.store_list, name='store_list'),
    path('stores/add/', views.add_store, name='add_store'),
    path('stores/<int:pk>/edit/', views.edit_store, name='edit_store'),
    path(
        'stores/<int:pk>/delete/',
        views.delete_store,
        name='delete_store'
    ),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/add/', views.add_product, name='add_product'),
    path(
        'products/<int:pk>/edit/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'products/<int:pk>/delete/',
        views.delete_product,
        name='delete_product'
    ),
    path(
        'products/<int:pk>/review/',
        views.add_review,
        name='add_review'
    ),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path(
        'cart/remove/<int:pk>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='marketplace/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='marketplace/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='marketplace/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='marketplace/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
