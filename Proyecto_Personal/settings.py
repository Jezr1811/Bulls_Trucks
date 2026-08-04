"""
Django settings for Proyecto_Personal project.
"""

import os
from pathlib import Path


import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
    "SECURE": True,
} 
# ===========================
# SEGURIDAD
# ===========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-@%$w9dtbsw)0eo(5h!k31&dl@2mm3uc2w%4%&ifkq#1jt^x(0_"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".onrender.com",
]


# ===========================
# APPS
# ===========================

INSTALLED_APPS = [
      "cloudinary_storage",
    "cloudinary",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    "usuarios",
    "conductores",
    "vehiculos",
    "trailers",
    "viajes",
    "gastos",
    "documentos",
    "mantenimientos",
    "reportes",
    "contabilidad",
]

 
# ===========================
# MIDDLEWARE
# ===========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "Proyecto_Personal.urls"


# ===========================
# TEMPLATES
# ===========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "Proyecto_Personal.wsgi.application"


# ===========================
# BASE DE DATOS
# ===========================

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ===========================
# VALIDACIÓN DE CONTRASEÑAS
# ===========================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ===========================
# INTERNACIONALIZACIÓN
# ===========================

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = "."
DECIMAL_SEPARATOR = ","
NUMBER_GROUPING = 3


# ===========================
# ARCHIVOS ESTÁTICOS
# ===========================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)
STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)


# ===========================
# ARCHIVOS MEDIA
# ===========================

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ===========================
# LOGIN
# ===========================

LOGIN_URL = "usuarios:login"

LOGIN_REDIRECT_URL = "usuarios:dashboard"

LOGOUT_REDIRECT_URL = "usuarios:login"


# ===========================
# DEFAULT PK
# ===========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ===========================
# SEGURIDAD PRODUCCIÓN
# ===========================

if not DEBUG:

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = "DENY"

    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")