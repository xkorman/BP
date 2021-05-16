"""
Django settings for Test_BP project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import locale
import os
from pathlib import Path

env = os.environ.copy()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '70l8sf9t^1&=$=ier8l$%aw(419y6%iqf2f7g2p!m$q7%*o59!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'crispy_forms',
    'django_quill',
    'admin_reorder',
    # 'channels',
    # 'django_private_chat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'Test_BP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'Test_BP.wsgi.application'

DATE_INPUT_FORMATS = ['%d-%m-%Y']

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres_db',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'sk-sk'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     '/var/www/static/',
# ]

LOGIN_REDIRECT_URL = '/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'core.User'

# # CHAT
# CHAT_WS_SERVER_HOST = 'localhost'
# CHAT_WS_SERVER_PORT = 8000
# CHAT_WS_SERVER_PROTOCOL = 'ws'
#
# ASGI_APPLICATION = "Test_BP.asgi.application"
#
# locale.setlocale(locale.LC_ALL, 'sk_SK.UTF-8')

MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
MEDIA_URL = "/media/"

ADMIN_REORDER = (

    {'app': 'core', 'label': 'Forum',
     'models': (
         'core.ForumCategory',
         'core.ForumPost',
         'core.ForumComment',
         'core.MatchForumComment',
     )
     },

    {'app': 'core', 'label': 'System sprav',
     'models': (
         'core.Message',
     )
     },

    {'app': 'core', 'label': 'System stranok podpory',
     'models': (
         'core.Page',
         'core.GroupPage',
         'core.MatchPages',
         'core.Questions'
     )
     },

    {'app': 'core', 'label': 'System prezentacnych slajdov',
     'models': (
         'core.News',
     )
     },

    {'app': 'core', 'label': 'Sprava uzivatelov a vaznov',
     'models': (
         'core.User',
         'core.Prisoner',
         'core.MatchPrisoner',
         'core.Department',
         'core.Requests',
         'core.RequestsInfo'
     )
     },

    'auth',
)