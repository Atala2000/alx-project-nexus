# Use Python 3.10 base image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing .pyc files
# and to keep stdout/stderr unbuffered (useful for logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project code
COPY . /app/

# Collect static files (optional, if using Django static files)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Command to run the app (gunicorn for production)
CMD ["gunicorn", "nexus.wsgi:application", "--bind]()
