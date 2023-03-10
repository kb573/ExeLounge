"""
Django settings for groupisite project.

Generated by "django-admin startproject" using Django 3.1.6.
t

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

import django_heroku

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "1y!(seh4ldt=wpgouu+^u^cz+%2gjll*)hh-bt@l7jpy!u5!#h"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://exelounge.herokuapp.com/']

STATICFILES_DIRS = [os.path.join(BASE_DIR, "users/static"),
                    os.path.join(BASE_DIR, "groupisite/static"),
                    os.path.join(BASE_DIR, "static")]

# Application definition

INSTALLED_APPS = [
    # third-party apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",

    # custom apps
    "users.apps.UsersConfig",
    "forum.apps.ForumConfig",
    "material",
    "captcha",
    "public_chat",
    "channels",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "groupisite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["users/templates", "groupisite/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "groupisite.wsgi.application"

ASGI_APPLICATION = "groupisite.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

AUTH_PROFILE_MODULE = 'groupisite.users.UserProfile'

DATE_INPUT_FORMATS = ["%d-%m-%Y", "%Y-%m-%d"]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# This uses the Django service credentials
# https://cloud.ibm.com/services/databases-for-postgresql/crn%3Av1%3Abluemix%3Apublic%3Adatabases-for-postgresql%3Aeu-gb%3Aa%2F41ad0f2c2a7140c39cf9d8ee67d4b182%3A163866f0-999d-42d5-83ff-3fe1bc5e8eb2%3A%3A?paneId=credentials
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django",
        "PASSWORD": "d319d26331683e9bd140987561e7b067d972155b8273b389cfe02afaf34a1fa1",
        "USER": "ibm_cloud_2fb865ce_a9de_475d_9542_25303b4e0940",
        "HOST": "677bf178-6cee-4d06-8d98-9b4df66a2f06.497129fd685f442ca4df759dd55ec01b.databases.appdomain.cloud",
        "PORT": "31444",
        "TEST": {
            "NAME": "django_test"
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Activate Django-Heroku
django_heroku.settings(locals())

# Google ReCaptcha
RECAPTCHA_PUBLIC_KEY = "6Lf8b3caAAAAABs2IA1DHUvmAr__hZ0gHv7Q18oy"
RECAPTCHA_PRIVATE_KEY = "6Lf8b3caAAAAAExJ0NWHGEbjP_P8c2J8RGE1WcZu"
