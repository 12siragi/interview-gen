# Use official Python slim image — smaller size, faster builds
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE — no .pyc files cluttering the container
# PYTHONUNBUFFERED — logs show in real time, not buffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies first (Docker layer caching)
# This layer only rebuilds when requirements.txt changes
# not every time your code changes — faster builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose Django's port
EXPOSE 8000

# Start gunicorn — production server
# workers=2 is enough for development and demo purposes
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--reload"]
