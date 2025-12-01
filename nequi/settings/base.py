import os
import json
from django.core.exceptions import ImproperlyConfigured
from unipath import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().ancestor(3)

# ======================================================
# SECRET KEY (LOCAL usa secret.json / PRODUCCIÓN usa env)
# ======================================================

def get_secret_key():
    """
    Local: lee secret.json
    Producción: usa la variable DJANGO_SECRET_KEY
    """
    # Si está en variable de entorno (Render), úsala
    env_key = os.getenv("DJANGO_SECRET_KEY")
    if env_key:
        return env_key

    # Si no existe, estamos local → leer secret.json
    secret_file = BASE_DIR.child("secret.json")

    if not secret_file.exists():
        raise ImproperlyConfigured(
            "No se encontró SECRET_KEY. Define DJANGO_SECRET_KEY "
            "o usa el archivo secret.json local."
        )

    with open(secret_file) as f:
        secrets = json.load(f)

    try:
        return secrets["SECRET_KEY"]
    except KeyError:
        raise ImproperlyConfigured("SECRET_KEY no existe dentro de secret.json")

SECRET_KEY = get_secret_key()

# ======================================================

# Apps
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
)

LOCAL_APPS = (
    'applications.users',
    'applications.account',
    'applications.transaction',
    'applications.auditlog',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nequi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nequi.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-ES'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
