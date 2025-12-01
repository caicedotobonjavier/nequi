from django.core.exceptions import ImproperlyConfigured
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
from unipath import Path
BASE_DIR = Path(__file__).resolve().ancestor(3)

# ============================================================
# SECRET KEY – Manejo dual: LOCAL (secret.json) / PRODUCCIÓN (env)
# ============================================================

secret = {}

# Solo intentar abrir secret.json si existe (LOCAL)
if os.path.exists("secret.json"):
    with open("secret.json") as f:
        secret = json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except KeyError:
        msg = f"La variable {secret_name} no existe en secret.json"
        raise ImproperlyConfigured(msg)

# En producción Render usa DJANGO_SECRET_KEY
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", secret.get("SECRET_KEY"))

# Si no hay KEY en local NI en entorno → error claro
if not SECRET_KEY:
    raise ImproperlyConfigured("No se encontró SECRET_KEY. "
                               "Define DJANGO_SECRET_KEY o usa secret.json")


# ============================================================
# Application definition
# ============================================================

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

# ============================================================
# Password validation
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================
# Internationalization
# ============================================================

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ============================================================
# Default primary key field type
# ============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'
