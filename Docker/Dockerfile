# ─── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.13-slim AS base

# Prevent .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed by Pillow & psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Collect static files (runs at build time so the image is self-contained)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Default: run the Django dev server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
