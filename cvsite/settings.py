import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: read secret key from env in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-change-me')

# DEBUG toggled via env var
DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

# Allow hosts from environment or default to all for quick deploy (override in prod)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '')
if ALLOWED_HOSTS:
    ALLOWED_HOSTS = [h.strip() for h in ALLOWED_HOSTS.split(',')]
else:
    ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'resume',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cvsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'resume' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'cvsite.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'hu'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Available languages for the site
LANGUAGES = [
    ('hu', 'Magyar'),
    ('en', 'English'),
]

# Where translation files will live
LOCALE_PATHS = [BASE_DIR / 'locale']

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'resume' / 'static']
# collectstatic will target this directory on deploy
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise static files compression
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (user uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# If DATABASE_URL is present, dj_database_url will configure DB from it
# Ensure SECURE_PROXY_SSL_HEADER when behind a proxy/railway
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
