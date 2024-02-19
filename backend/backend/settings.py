import environ
from django.utils.translation import gettext_lazy as _

# Get root dir of the project
root = environ.Path(__file__) - 3
env = environ.Env()
# Reading .env file
environ.Env.read_env()

SITE_ROOT = root()


# Get value from .env file
SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://0.0.0.0:3000',
]

CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'backend.urls'

# My custom user model
AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'django_celery_beat',
    'users',
    'pg_processing',
    'django_filters',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        # Make accessible API endpoints via browser
        'rest_framework.renderers.BrowsableAPIRenderer'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],
}

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

WSGI_APPLICATION = 'backend.wsgi.application'

# Get the DB creds from .env file
DATABASES = {'default': env.db('DATABASE_URL')}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'ru-RU'

LANGUAGES = [
    ('en', _('English')),
]

LOCALE_PATHS = [
    SITE_ROOT + r'\backend\locales'
]
print(LOCALE_PATHS)

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'pg_errs': {
            'class': 'logging.FileHandler',
            'filename': SITE_ROOT + r'\backend\pg_processing\pg_logs.log',
            'formatter': 'pg_errs',
            'level': 'ERROR',
            # 'mode': 'w'
            },
        'test': {
            'class': 'logging.FileHandler',
            'filename': SITE_ROOT + r'\pg_logs.log',
            'formatter': 'test',
            'level': 'INFO',
            # 'mode': 'w'
        },
    },
    'formatters': {
        'pg_errs': {
            'format': '[%(levelname)s: %(asctime)sms] [Module - %(name)s]\n %(message)s\n',
        },
        'test': {
            'format': '[%(levelname)s\n %(message)s]\n',
        },
    },

    'loggers': {
        'pg_processing.psycopg_module': {
            'level': 'ERROR',
            'handlers': ['pg_errs'],
            'propagate': False
        },
        'test': {
            'level': 'INFO',
            'handlers': ['test'],
            'propagate': False
        }
    }
}

# Celery settings
CELERY_BROKER_URL = env.str('BROKER_URL')
CELERY_RESULT_BACKEND = env.str('RESULT_URL')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
