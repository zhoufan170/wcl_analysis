"""
Django settings for wcl_analysis project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from service.constant import CONSTANT_SERVICE

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1ai#)@_az=1a-zwtlq4e4#m#@*^84w#qp&!r+7&822ns_6^70d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'www.wclanalysis.site']

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'file_upload',
    'file_download',
    'taq',
    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'wcl_analysis.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'wcl_analysis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('WCL_MYSQL_DB'),  # Or path to database file if using sqlite3.
        'USER': os.environ.get('WCL_MYSQL_USERNAME'),  # Not used with sqlite3.
        'PASSWORD': os.environ.get('WCL_MYSQL_PASSWORD'),  # Not used with sqlite3.
        'HOST': os.environ.get('WCL_MYSQL_HOST'),  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# specify media root for user uploaded files,
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# WCL_API_KEY = os.environ.get('WCL_API_KEY')
WCL_API_KEY = '9c1df9ffb7dabbf2651007275f1da40a'
WCL_SCHEMA = 'https://cn.classic.warcraftlogs.com'

SELF_SCHEMA = 'http://www.wclanalysis.site'

DETAIL_LIST = [
    ["viscidus_poison_tick", '维度希斯毒箭伤害统计', "/scan_viscidus_poison_tick/", '/viscidus_poison_tick_info/'],
    ["boss_nature_protection", 'BOSS战自然防护药水破案', "/scan_boss_nature_protection/", '/boss_nature_protection_info/'],
]

TAQ_NATURE_PROTECTION_BOSS_LIST = [
    CONSTANT_SERVICE.Viscidus_name,
    CONSTANT_SERVICE.Hururan_name,
    CONSTANT_SERVICE.Ouro_name,
    CONSTANT_SERVICE.Cthun_name,
]

# AVAILABLE_TRASH_ID = [15252, 15249, 15250, 15246, 15247, 15725, 15334, 15728, 15984, 15726, 15233, 15230, 15240, 15235, 15236, 15667, 15630, 15802, 15264, 15311, 15277, 15262, 15312]
