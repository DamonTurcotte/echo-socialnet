from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ADMINS = [
    ('Echo Admin', os.environ['ADMIN'])
]

ALLOWED_HOSTS = [
    os.environ['ALLOWED_HOSTS1'],
    os.environ['ALLOWED_HOSTS2'],
    os.environ['ALLOWED_HOSTS3'],
    'localhost'
]

INSTALLED_APPS = [
    'corsheaders',
    'oauth2_provider',
    'rest_framework',
    'captcha',
    'news.apps.NewsConfig',
    'notifications.apps.NotificationsConfig',
    'chat.apps.ChatConfig',
    'posts.apps.PostsConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'echo.urls'

CORS_ALLOWED_ORIGINS = [
    'https://turcotte.tech',
    'https://www.turcotte.tech',
    'https://api.turcotte.tech',
    'https://echonetwork.app',
    'https://www.echonetwork.app',
    'https://google.com',
    'https://www.google.com',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:5173',
    'http://localhost:8000',
    'http://localhost:3000',
    'http://localhost:5173',
]

CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'echo.context_processors.add_variable_to_base'
            ],
        },
    },
]

WSGI_APPLICATION = 'echo.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": os.environ['ENGINE'],
        "NAME": os.environ['NAME'],
        "USER": os.environ['USER'],
        "PASSWORD": os.environ['PASSWORD'],
        "HOST": os.environ['HOST'],
        "PORT": "",
    }
}

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.ScryptPasswordHasher',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
      'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

OAUTH2_PROVIDER = {
    "OAUTH2_VALIDATOR_CLASS": "echo.oauth_validators.CustomOAuth2Validator",
    'ACCESS_TOKEN_EXPIRE_SECONDS': 86400,
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,
    'REFRESH_TOKEN_GRACE_PERIOD_SECONDS': 120,
    "OIDC_ENABLED": True,
    # "OIDC_RSA_PRIVATE_KEY": os.environ['OIDC_RSA_PRIVATE_KEY'],
    # "OIDC_RSA_PRIVATE_KEYS_INACTIVE": [
    #     os.environ.get("OIDC_RSA_PRIVATE_KEY_2"),
    #     os.environ.get("OIDC_RSA_PRIVATE_KEY_3")
    # ],
    "OIDC_RP_INITIATED_LOGOUT_ENABLED": True,
    "OIDC_RP_INITIATED_LOGOUT_ALWAYS_PROMPT": True,
    "SCOPES": {
        'openid': "OpenID Connect scope",
        'read': 'Read scope',
        'write': 'Write scope',
        'introspection': 'Introspect token scope',
    }
}

RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']

RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']

BASE_URL = os.environ['BASE_URL']

LOGIN_URL = '/accounts/login/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    MEDIA_ROOT = os.environ['MEDIA_ROOT']

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"

AUTH_USER_MODEL = "users.EchoUser"

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = None
    SESSION_COOKIE_SAMESITE = None