from pathlib import Path
# Configuración GeoDjango para Windows usando QGIS 4.0.2
import os

if os.name == "nt":
    QGIS_ROOT = r"C:\Program Files\QGIS 4.0.2"
    QGIS_BIN = os.path.join(QGIS_ROOT, "bin")

    # Agregar binarios de QGIS al PATH
    os.environ["PATH"] = QGIS_BIN + os.pathsep + os.environ.get("PATH", "")

    # Permitir carga de DLLs en Python 3.8+
    try:
        os.add_dll_directory(QGIS_BIN)
    except Exception:
        pass

    # Rutas explícitas para GeoDjango
    GDAL_LIBRARY_PATH = os.path.join(QGIS_BIN, "gdal312.dll")
    GEOS_LIBRARY_PATH = os.path.join(QGIS_BIN, "geos_c.dll")

    # Rutas auxiliares recomendadas
    os.environ["GDAL_DATA"] = os.path.join(QGIS_ROOT, "share", "gdal")
    os.environ["PROJ_LIB"] = os.path.join(QGIS_ROOT, "share", "proj")
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-change-me')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') if h.strip()]

INSTALLED_APPS = [
    "gobernanza",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'encuestas',
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

ROOT_URLCONF = 'config.urls'

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
                'encuestas.context_processors.turnstile_site_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'planifico_municipio'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

LANGUAGE_CODE = 'es-bo'
TIME_ZONE = 'America/La_Paz'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TURNSTILE_SITE_KEY = os.getenv('TURNSTILE_SITE_KEY', '')
TURNSTILE_SECRET_KEY = os.getenv('TURNSTILE_SECRET_KEY', '')

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'