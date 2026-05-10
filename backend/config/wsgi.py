"""
WSGI config for the Interview Question Generator project.

This is the entry point Gunicorn uses to serve the Django application.
Gunicorn calls this file directly via:
  gunicorn config.wsgi:application
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
