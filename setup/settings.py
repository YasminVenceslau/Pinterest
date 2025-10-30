from pathlib import Path
import os

# Caminho base do projeto (pasta que contém o manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent


# --- CONFIGURAÇÕES BÁSICAS ---
SECRET_KEY = 'django-insecure-s(7q)zasc(e)e-fph59qy#f=w3frrk0i1^kie2lor#y69ky@za'
DEBUG = True  # ❗ Em produção (PythonAnywhere), idealmente usar False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'yasminV.pythonanywhere.com']


# --- APPS INSTALADOS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pinterest.apps.PinterestConfig',  # Seu app principal
    'django.contrib.humanize',
]


# --- MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- URLS E WSGI ---
ROOT_URLCONF = 'setup.urls'
WSGI_APPLICATION = 'setup.wsgi.application'


# --- TEMPLATES ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Corrigido: o caminho 'bookstore/templantes' era incorreto.
        # Se você usa apenas os templates dos apps, pode deixar vazio.
        'DIRS': [BASE_DIR / 'templates'],  # ✅ pasta 'templates' na raiz do projeto
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


# --- BANCO DE DADOS ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- VALIDAÇÃO DE SENHAS ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- INTERNACIONALIZAÇÃO ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True


# --- ARQUIVOS ESTÁTICOS E MÍDIA ---
# URL base para arquivos estáticos
STATIC_URL = '/static/'

# Onde ficam os arquivos estáticos locais (css/js/images)
STATICFILES_DIRS = [
    BASE_DIR / "static",  # pasta 'static/' dentro do projeto
]

# Onde o collectstatic vai reunir tudo (para o PythonAnywhere)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Configuração para arquivos de mídia (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# --- CHAVE PADRÃO ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
