from .base import *
import os
import dj_database_url

# Seguridad
DEBUG = False

# SECRET_KEY: preferir variable de entorno en producción
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_secret("SECRET_KEY")

# Hosts: permitir el host de Render y los .onrender.com
ALLOWED_HOSTS = [
    os.environ.get("RENDER_EXTERNAL_HOSTNAME", ""),
    ".onrender.com",
    "*",
]

# Database: usa DATABASE_URL (Render la provee o la obtiene desde fromDatabase)
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=False
    )
}

# Si no hay DATABASE_URL, usar sqlite temporal para que no falle en build
if not DATABASES["default"]:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.child("db.sqlite3"),
    }

# Static
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# Seguridad adicional (si deseas)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
]
