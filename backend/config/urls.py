"""
Root URL configuration for Interview Question Generator.

Keeps the root clean — each app owns its own urls.py.
Adding a new app = one new line here, nothing else changes.
"""
from django.urls import path, include

urlpatterns = [
    # All question-related endpoints live under /api/questions/
    path("api/questions/", include("questions.urls")),
]
