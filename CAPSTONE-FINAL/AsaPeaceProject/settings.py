from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-default-secret-key')

DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Añade tus dominios en producción

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',  # Asegúrate de que esta aplicación exista
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

ROOT_URLCONF = 'AsaPeaceProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Ruta a la carpeta de plantillas
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

WSGI_APPLICATION = 'AsaPeaceProject.wsgi.application'

# Database Pablo
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'ASApeace',
#        'USER': 'postgres',
#        'PASSWORD': '1337',
#        'HOST': 'localhost',
#        'PORT': '5433',
#    }
#}

# # Database Andres
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.getenv('DB_NAME', 'asapeace'),
#         'USER': os.getenv('DB_USER', 'postgres'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'guts_2015'),
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'asapeace',  # Nombre de tu base de datos
        'USER': 'postgres',   # Usuario de la base de datos
        'PASSWORD': 'admin123',  # Contraseña de la base de datos
        'HOST': 'localhost',  # Generalmente 'localhost'
        'PORT': '5432',       # Puerto por defecto de PostgreSQL
    }
}
# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'  # Cambiar el código de idioma a español
TIME_ZONE = 'America/Santiago'  # Cambiar la zona horaria a Chile
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Asegúrate de que está apuntando a la carpeta 'static' correctamente
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CSRF Settings
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000']

APPEND_SLASH = False

LOGIN_URL = '/login/'
# configuración de usarios portal
# desactivar auth_user_model cuando se vaya a trabajar con admin
AUTH_USER_MODEL = 'main.Usuario'  
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'tu-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'tu-contraseña'
# DEFAULT_FROM_EMAIL = 'tu-email@gmail.com'

# Define la URL para acceder a los archivos multimedia
MEDIA_URL = '/media/'

# Define la ruta en tu sistema de archivos donde se guardarán los archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Ajustes de Transbank
TRANSBANK_COMMERCE_CODE = "597055555532"
TRANSBANK_API_KEY = '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C'
TRANSBANK_ENVIRONMENT = "INTEGRACION"  # Cambia a "PRODUCCION" al pasar a producción