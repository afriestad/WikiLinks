"""
Django settings for kokekunster project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = (
    # Must be before any admin apps
    'dal',
    'dal_select2',

    # Must be before django.contrib.admin
    'admin_interface',
    'flat_responsive',
    'colorfield',

    # Used for backing up data to Dropbox and importing prod data
    'dbbackup',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'adminsortable2',
    'rules.apps.AutodiscoverRulesConfig',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # Dataporten API
    'dataporten',

    # Custom Dataporten oAuth2-provider for django-allauth
    'dataporten.oauth2',
    'sanitizer',
    'subdomains',
    'semesterpage',
    'django_cleanup',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'subdomains.middleware.SubdomainURLRoutingMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    # Adds dataporten API information to request.user.dataporten
    # Needs to be placed after any authentication middleware, as this
    # requires inspection of request.user
    'dataporten.middleware.DataportenGroupsMiddleware',
)

ROOT_URLCONF = 'kokekunster.urls'


# A dictionary of urlconf module paths, keyed by their subdomain.
# https://django-subdomains.readthedocs.io/en/latest/

# Possible to add new subdomains in the future!
SUBDOMAIN_URLCONFS = {
#     None: 'kokekunster.urls.urls',  # no subdomain
#     'www': 'kokekunster.urls.urls', # Should be redirected to None
#     'api': 'kokekunster.urls.api',  # no subdomain
}

SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'kokekunster.wsgi.application'


# Custom object instance based permissions with django-rules
AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Allows users to logout on get requests, making it possible
# to log out without a form confirmation or use of javascript
# Allows other websites to log out users, but is not considered
# a threat for the moment
ACCOUNT_LOGOUT_ON_GET = True


# Controls the life time of the session
ACCOUNT_SESSION_REMEMBER = True

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'nb-no'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Media files (User-uploaded course logos)

MEDIA_URL = '/media/'


# Cookie-based sessions

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_AGE = 31536000  # 1 year, instead of default 2 weeks


# Email sending from the following adress

SERVER_EMAIL = 'django@kokekunster.no'


# Which semester should be defaulted to in url handling when the study program is not specified?
# What is the slug of the associated study_program?
# NB! Must be the primary key value of the Semester object

DEFAULT_SEMESTER_PK = 1
DEFAULT_STUDY_PROGRAM_SLUG = 'fysmat'


# Dataporten settings

# Cache requests to the dataporten API
DATAPORTEN_CACHE_REQUESTS = True

# Where to save the sqlite3 cache backend
DATAPORTEN_CACHE_PATH = 'tmp/'

# Determine run environment based on the environment variable 'PRODUCTION', and load proper settings

if os.environ.get('PRODUCTION', None):
    INSTALLED_APPS += (
        # Use djange_cron to run dbbackup every day
        'django_cron',

        # Sentry error logging service
        'raven.contrib.django.raven_compat',
    )

    CRON_CLASSES = [
        'kokekunster.cronjobs.Backup',
    ]
    BACKUP_TIMES = ['3:00',]

    # Production specific settings are specified in kokekunster/setting_prod.py
    from kokekunster.settings_prod import *
else:
    # Development assistive apps
    INSTALLED_APPS += (
            'debug_toolbar',
            'django_extensions',
    )
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE
    from kokekunster.settings_dev import *


# Import local settings that are gitignored. Can be used for temporary test settings

try:
    from kokekunster.settings_local import *
except ImportError as e:
    pass
