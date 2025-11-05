# Base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y curl vim iputils-ping && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Collect static files (optional if using Django admin)
RUN python manage.py collectstatic --noinput || true

# Expose Django port
EXPOSE 8000

# Run Gunicorn as production server
CMD ["gunicorn", "uploadhub.wsgi:application", "--bind", "0.0.0.0:8000"]
