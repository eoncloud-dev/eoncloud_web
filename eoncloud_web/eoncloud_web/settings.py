"""
Django settings for eoncloud_web project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import logging.config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@ybbpz49p^1x#0&un2!8i4*!9k#dav&83l7sl-ib%)-$t3jyfj'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ["*",]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'biz',
    'biz.account',
    'biz.idc',
    'biz.instance',
    'biz.image',
    'biz.floating',
    'biz.network',
    'biz.volume',
    'cloud',
    'render',
    'biz.firewall',
    'biz.forum',
    'biz.backup',
)

#AUTHENTICATION_BACKENDS = ('biz.cloud_auth.backend.ComputeCenterBackend',) 

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
)

REST_FRAMEWORK = {
    "PAGE_SIZE": 10,
    "PAGE_SIZE_QUERY_PARAM": "page_size",
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),  

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),  

}

ROOT_URLCONF = 'eoncloud_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
            ],
        },
    },
]


WSGI_APPLICATION = 'eoncloud_web.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization

LANGUAGE_CODE = 'zh_CN'
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

FORMAT_MODULE_PATH = 'eoncloud_web.formats'
DATETIME_FORMAT="Y-m-d H:i"


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
LOGIN_URL = '/login'
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "verbose": {
            'format': '%(asctime)s %(levelname)s [Line: %(lineno)s] -- %(message)s',
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/eoncloud.log',
            'formatter': 'verbose'
        },

        'cloud.tasks.handler': {
            'level': 'DEBUG',
            'filters': None,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/celery_task.log',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },

    },
    'loggers': {
        'root': {
            'handlers': ['default'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },

        'biz': {
            'handlers': ['default'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },

        'cloud.tasks': {
            'handlers': ['cloud.tasks.handler'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handers': ['console'],
        },
    }
}


logging.config.dictConfig(LOG_CONFIG)


from eoncloud_web.local.local_settings import *
from eoncloud_web.local.db_settings import *
from eoncloud_web.local.celery_settings import *
