import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-xav-1h&fix5hz@lkm^i$@#+q^avxw@vrl4c9+tanv+6#z0$rm('
DEBUG = True
ALLOWED_HOSTS = ['*']


APPS_DIR = Path(BASE_DIR) / 'apps'
sys.path.insert(0, str(APPS_DIR))
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
]

THIRD_APPS = []

PROJECT_APPS = [
    'apps.workouts',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + PROJECT_APPS
#------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#------------------------------------------------------------------------------
ROOT_URLCONF = 'CORE.urls'
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
WSGI_APPLICATION = 'CORE.wsgi.application'
#------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
#------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#------------------------------------------------------------------------------
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
#------------------------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True
USE_L10N = True
#------------------------------------------------------------------------------
STATIC_ROOT = Path(BASE_DIR) / 'staticfiles'
STATIC_URL = '/static/'
#------------------------------------------------------------------------------
MEDIA_ROOT = Path(BASE_DIR) / 'media'
MEDIA_URL = '/media/'
#------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#------------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    # os domínios que são confiáveis para enviar requisições potencialmente
    # perigosas (como POST) ao seu backend
    'http://localhost:5000',
    'http://127.0.0.1:5000',
]
#------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'CYCLING',
    'DESCRIPTION': 'App for register your workouts of cycling',
    'VERSION': '1.0.0',
    'OAS_VERSION': '3.0.3',
    'SERVE_INCLUDE_SCHEMA': False,
}
#------------------------------------------------------------------------------
