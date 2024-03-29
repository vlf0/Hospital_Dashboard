import environ

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
    '10.123.8.17',
    '0.0.0.0',
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:9000',
    'http://10.123.8.17:3000',
    'http://10.123.8.17:9000',
    'http://10.123.8.17:90',
    'http://10.123.8.17:30',
    'http://10.123.8.17:6379',
]

CSRF_TRUSTED_ORIGINS = ['http://10.123.8.17:90']

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'backend.urls'

# My custom user model
AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    'daphne',
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
    'data',
    'django_filters',
    'channels'
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
        'DIRS': [
            f'{SITE_ROOT}\\backend\\templates'
        ],
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

ASGI_APPLICATION = 'backend.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('0.0.0.0', 6379)],
        },
    },
}

# Get the DB creds from .env file
DATABASES = {'default': env.db('DMK_URL')}

# External DB data
DB_CREDS = {
    'host': env.str('HOST'),
    'port': env.str('PORT'),
    'dbname': env.str('DBNAME'),
    'user': env.str('PGUSER'),
    'password': env.str('PASSWORD'),
}

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

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = f'{SITE_ROOT}/backend/static'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'conn_errs': {
            'class': 'logging.FileHandler',
            'filename': SITE_ROOT + '/backend/data/pg_logs.log',
            'formatter': 'conn_errs',
            'level': 'ERROR',
            # 'mode': 'w'
            },
        'dmk': {
            'class': 'logging.FileHandler',
            'filename': SITE_ROOT + '/backend/data/pg_logs.log',
            'formatter': 'dmk',
            'level': 'INFO',
            # 'mode': 'w'
        },
    },
    'formatters': {
        'conn_errs': {
            'format': '[%(levelname)s: %(asctime)sms] [Class - %(name)s]\n %(message)s\n',
        },
        'dmk': {
            'format': '[%(levelname)s: %(asctime)s] [Class - %(name)s]\n %(message)s\n',
            # 'datefmt': '%Y-%m-%d',
        },
    },

    'loggers': {
        'data.psycopg_module.BaseConnectionDB': {
            'level': 'ERROR',
            'handlers': ['conn_errs'],
            'propagate': False
        },
        'data.kis_data.DataForDMK': {
            'level': 'INFO',
            'handlers': ['dmk'],
            'propagate': False
        }
    }
}

# Celery settings
CELERY_BROKER_URL = env.str('BROKER_URL')
CELERY_RESULT_BACKEND = env.str('RESULT_URL')
CELERY_TIMEZONE = 'Europe/Moscow'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://0.0.0.0:6379/2',
    }
}

KEY_PREFIX = ''
