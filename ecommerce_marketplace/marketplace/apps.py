"""Application configuration for the marketplace app."""

from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    """Configuration settings for the marketplace app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'marketplace'
