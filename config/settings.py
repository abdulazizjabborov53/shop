from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
 
 
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/
 
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-abqaql=y8w8w77vv9&aq(tnqj5j-c1a1030nfnl$bdwe#wbc(y'
 
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']
 
 
# Application definition
 
INSTALLED_APPS = [
    'django.contrib.sites',
    'modeltranslation', # <-- S
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'rosetta', # <-- Mana bu yerga qo'shing
    'dashboard',
]
SITE_ID = 1

# Autentifikatsiya backend'larini qo'shish
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Kirish va chiqishdan keyin qayerga yo'naltirilishi
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
 
ROOT_URLCONF = 'config.urls'
 
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
 
WSGI_APPLICATION = 'config.wsgi.application'
 
 
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
 
 
# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators
 
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
# https://docs.djangoproject.com/en/6.0/topics/i18n/
 
LANGUAGE_CODE = 'uz'
 
LANGUAGES = [
    ('uz', 'Uzbek'),
    ('ru', 'Russian'),
    ('en', 'English'),
]
 
LOCALE_PATHS = [BASE_DIR / 'locale']
 
TIME_ZONE = 'Asia/Tashkent'
 
 
USE_I18N = True
 
USE_TZ = True
 
 
# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = [BASE_DIR / 'static']
 
# STATIC_ROOT = BASE_DIR / 'staticfiles'
 
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'
 
AUTH_USER_MODEL = 'main.User'
 
LOGIN_URL = '/dashboard/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/dashboard/login/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
 