"""URL configuration for the ecommerce_marketplace project."""

from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace.urls')),
]
