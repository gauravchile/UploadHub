import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'dev-secret'
DEBUG = False
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'files',  # your app for file uploads
]

ROOT_URLCONF = 'uploadhub.urls'

# ✅ Database configuration (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'filesdb'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASS', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'uploadhub_db'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ✅ MinIO configuration
MINIO_STORAGE_ENDPOINT = os.getenv('MINIO_STORAGE_ENDPOINT', 'uploadhub_minio:9000')
MINIO_STORAGE_ACCESS_KEY = os.getenv('MINIO_STORAGE_ACCESS_KEY', 'minioadmin')
MINIO_STORAGE_SECRET_KEY = os.getenv('MINIO_STORAGE_SECRET_KEY', 'minioadmin')
MINIO_STORAGE_BUCKET_NAME = os.getenv('MINIO_STORAGE_BUCKET_NAME', 'uploads')

# ✅ REST Framework config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny']
}

# ✅ Static files
STATIC_URL = '/static/'

