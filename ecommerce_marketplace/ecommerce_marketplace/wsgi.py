"""WSGI entry point for ecommerce_marketplace."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'ecommerce_marketplace.settings'
)

application = get_wsgi_application()
