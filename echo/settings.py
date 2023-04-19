from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

ALLOWED_HOSTS = [
    os.environ['ALLOWED_HOSTS1'],
    os.environ['ALLOWED_HOSTS2'],
    os.environ['ALLOWED_HOSTS3'],
    'localhost'
]

INSTALLED_APPS = [
    'corsheaders',
    'oauth2_provider',
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
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'echo.urls'

CORS_ORIGIN_ALLOW_ALL = True

SESSION_COOKIE_NAME = 'oauth2server_sessionid'

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

# OAUTH2_PROVIDER = {
#     "OAUTH2_VALIDATOR_CLASS": "django_oauth2_server.oauth_validator.CustomOAuth2Validator",
#     "OIDC_ENABLED": True,
#     "PKCE_REQUIRED": False,
#     "OIDC_RSA_PRIVATE_KEY": os.environ['OIDC_RSA_PRIVATE_KEY'],
#     'SCOPES': {
#         'read': 'Read scope',
#         'write': 'Write scope',
#         'openid': "OpenID Connect scope",
#     },
# }

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
    MEDIA_ROOT = '/media/'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"

AUTH_USER_MODEL = "users.EchoUser"

if not DEBUG: 
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SAMESITE = 'None'