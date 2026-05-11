# Use official Python slim image — smaller size, faster builds
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE — no .pyc files cluttering the container
# PYTHONUNBUFFERED — logs show in real time, not buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install curl for Docker healthcheck + clean up apt cache in the same layer
# to keep the image size small
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (Docker layer caching)
# This layer only rebuilds when requirements.txt changes,
# not every time your code changes — faster builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Django's port
EXPOSE 8000

# Start gunicorn — production WSGI server
# --workers 2  : enough for demo/development; increase for production load
# --reload is intentionally omitted — it adds overhead and causes unexpected
#   worker restarts in production. Use docker-compose.dev.yml override locally.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]