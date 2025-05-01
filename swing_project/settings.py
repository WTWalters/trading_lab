# swing_project/settings.py
"""
Django settings for swing_project project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url # <-- Import dj-database-url
import logging # <-- Import logging for warnings

# Configure logger for settings warnings/info
logger = logging.getLogger(__name__)

# Load environment variables from .env file located at the project root
# Ensure BASE_DIR is defined before using it for env_path
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env' # Use BASE_DIR to find .env
load_dotenv(dotenv_path=env_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR already defined above

# SECRET KEY Configuration
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for Django application in .env file")

# DEBUG Configuration
# Defaults to False if not set or value is not 'True' (case-insensitive check)
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS Configuration (adjust as needed for deployment)
ALLOWED_HOSTS = []
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Optional: Load from .env for production flexibility
# allowed_hosts_str = os.getenv('ALLOWED_HOSTS', '')
# if allowed_hosts_str:
#     ALLOWED_HOSTS.extend([host.strip() for host in allowed_hosts_str.split(',')])


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard", # Your app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "swing_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'], # Project-level templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "swing_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Uses dj-database-url to parse the DATABASE_URL environment variable

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600, # Optional: Keep connections alive for 10 mins
            conn_health_checks=True, # Optional: Enable simple health checks
        )
    }
    # Ensure dj-database-url correctly inferred the PostgreSQL engine
    if DATABASES['default']['ENGINE'] != 'django.db.backends.postgresql':
         logger.warning(f"dj-database-url inferred engine {DATABASES['default']['ENGINE']}, expected postgresql. Check DATABASE_URL format.")
         # You might force it here if needed, but usually indicates URL format issue:
         # DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
else:
    # Fallback to SQLite if DATABASE_URL is not set (useful for initial setup/testing)
    logger.warning("DATABASE_URL environment variable not set. Falling back to db.sqlite3.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC" # Keep UTC for database storage
USE_I18N = True
USE_TZ = True # Enable timezone support


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
# Example: Define location for project-wide static files if you have them
# STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT is needed for 'collectstatic' during deployment
# STATIC_ROOT = BASE_DIR / "staticfiles"


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
