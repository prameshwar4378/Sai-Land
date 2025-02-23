from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

#BASE_URL = '/erp/'
FORCE_SCRIPT_NAME = None

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tct^rqy$hrxn)w=ej%*(de@fol5=a8qz(xer3(#&3!gxy(_bz8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['139.5.188.128','localhost', '127.0.0.1','sailanddevelopers.com', 'www.sailanddevelopers.com']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Website',
    'ERP_Admin',
    'ERP_Workshop',
    'ERP_Account',
    'ERP_Finance',
    'API',
    'rest_framework',
    'rest_framework.authtoken',
    'crispy_bootstrap5',
    'crispy_forms',
    'import_export',
    # 'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'SLD.urls'

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

WSGI_APPLICATION = 'SLD.wsgi.application'



# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         'rest_framework.authentication.TokenAuthentication',
#     ],
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.IsAuthenticated',
#     ],
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow access to everyone
    ],
}


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'sld',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

import os


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # 'LOCATION': 'C:/Users/Admin/Downloads/Pawar Sir',  # Ensure this directory exists
        'LOCATION': os.path.join(BASE_DIR, 'cache'),  # Ensure this directory exists
    }
}



# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'  # Indian Standard Time
USE_I18N = True
USE_L10N = False  # Turn off localization if you want to explicitly format datetime
USE_TZ = True

LOGIN_URL = '/login'

AUTH_USER_MODEL = 'ERP_Admin.CustomUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


STATIC_URL = 'https://sailanddevelopers.com/static/'

STATIC_ROOT = '/var/www/staticfiles/'  # This is where files will be collected

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Add your static folder explicitly
]

MEDIA_URL = 'https://sailanddevelopers.com/media/'
MEDIA_ROOT = '/var/www/media/'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'prameshwar4378@gmail.com'  # Replace with your Gmail email address
EMAIL_HOST_PASSWORD = 'uaen nuhf qwey dkfr'  # Replace with your Gmail password or App Password

CSRF_TRUSTED_ORIGINS = [
    'https://sailanddevelopers.com',
    'https://www.sailanddevelopers.com',  # If using both www and non-www versions
    'http://sailanddevelopers.com',  # Add HTTP for local or non-SSL traffic, if necessary
    'http://www.sailanddevelopers.com',  # Add HTTP for local or non-SSL traffic, if necessary
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True