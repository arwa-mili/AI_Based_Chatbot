from .base import *
from decouple import config

DEBUG = False

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS", 
    default="",
    cast=lambda v: [s.strip() for s in v.split(",") if s]
)

SECRET_KEY = config("SECRET_KEY")

###### DB CONFIG ######
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
        "ATOMIC_REQUESTS": True,
    }
}
ENCRYPTION_KEY=config('ENCRYPTION_KEY')

###### SMTP CONFIG ######
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

###### AWS CONFIG ######
AWS_S3_BASE_FOLDER = config("AWS_S3_BASE_FOLDER")
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": config("AWS_ACCESS_KEY_ID"),
            "secret_key": config("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": config("AWS_STORAGE_BUCKET_NAME"),
            "region_name": config("AWS_S3_REGION_NAME"),
            "default_acl": config("AWS_DEFAULT_ACL", default="private"),
            "querystring_auth": config("AWS_QUERYSTRING_AUTH", cast=bool, default=True),
            "querystring_expire": config("AWS_QUERYSTRING_EXPIRE", cast=int, default=3600),
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": config("AWS_ACCESS_KEY_ID"),
            "secret_key": config("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": config("AWS_STORAGE_BUCKET_NAME"),
            "region_name": config("AWS_S3_REGION_NAME"),
        },
    },
}

SOCIAL_AUTH = {
    "GOOGLE_CLIENT_IDS": ["835828636219-dss0rs24rc6tg5q8q2vck86eua7hn501.apps.googleusercontent.com","835828636219-l3sosr7ue4fctk3bjq4aqjnq92jdo4tp.apps.googleusercontent.com","835828636219-a0loe5mt05msf92el7bceip5evi25vdb.apps.googleusercontent.com"],
    "FACEBOOK_APP_ID": "your-facebook-app-id",
    "FACEBOOK_APP_SECRET": "your-facebook-app-secret",
    "APPLE_CLIENT_IDS": ["com.your.bundle.id"],
    "APPLE_JWKS_CACHE_SECONDS": 86400,  
}

###### SECURITY CONFIG ######
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

###### LOG CONFIG ######
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
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
            'filename': '/var/log/django/errors.log',
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
