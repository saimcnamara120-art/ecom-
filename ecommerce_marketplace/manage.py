#!/usr/bin/env python
"""Django command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run Django management commands."""
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'ecommerce_marketplace.settings'
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it is installed and "
            "available in your virtual environment."
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
