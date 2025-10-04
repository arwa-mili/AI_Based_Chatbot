from .base import *
from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG = True

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

SECRET_KEY = config('SECRET_KEY')

ENCRYPTION_KEY=config('ENCRYPTION_KEY')


###### DB CONFIG ######
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default=5432, cast=int),
        "ATOMIC_REQUESTS": True,
    }
}

INSTALLED_APPS += [
    
]

###### SMTP CONFIG ######
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'



STATIC_ROOT = BASE_DIR / "staticfiles"  

###### LOG CONFIG ######
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': './logs/erros.log',
            'maxBytes': 5 * 1024 * 1024,
            'backupCount': 5, 
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'config': {
            'handlers': ['file', 'console'],
            'level': 'ERROR', 
            'propagate': False,
        },
    },
}
