"""
Django settings for Interview Question Generator.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Fail loudly at startup if the secret key is missing.
# A missing key causes unpredictable mid-request crashes, which are
# harder to diagnose than a clear startup error.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set.")

DEBUG = os.environ.get("DEBUG", "False") == "True"

# Set ALLOWED_HOSTS in your hosting platform's env vars.
# Example: ALLOWED_HOSTS=yourdomain.railway.app,localhost
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.sessions",
    "rest_framework",
    "corsheaders",
    "questions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# Add your deployed frontend URL here if it changes.
# A wrong URL causes CORS errors in production that don't appear locally.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://interview-gen.vercel.app",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [],
}

# Cache — used by:
#   ai_service.py  → caches questions per job title (24h TTL)
#   views.py       → rate limiting per IP (1 min window)
#
# LocMemCache is fine for a single worker / single server deployment.
# To scale: swap BACKEND to django.core.cache.backends.redis.RedisCache
# and set LOCATION to your Redis URL — nothing else in the codebase changes.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "interview-generator",
    }
}

AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemini")
AI_API_KEY  = os.environ.get("AI_API_KEY", "")

STATIC_URL = "/static/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "questions": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"