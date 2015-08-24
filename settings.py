"""
Django settings for TracktivityPets project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://
docs.djangoproject.com/en/1.7/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_*p08ub2m&rxc2+xin_cweddn3gk-9-58e5^0j8zsbbsz^+b$u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_HOST_USER = 'john@johnkendall.net'
EMAIL_HOST_PASSWORD = 'hx--xq5iRGYZ-I3MT9kdPg'
EMAIL_PORT = 587

HOST_NAME = "tracktivitypets.me"
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fitapp',
    'djcelery',
    'tracktivityPetsWebsite',
    #    "kombu.transport.django",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'TracktivityPets.urls'

WSGI_APPLICATION = 'TracktivityPets.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

FITAPP_CONSUMER_KEY = 'b715db8e526a6f27b1223c4096ae14d5'
FITAPP_CONSUMER_SECRET = 'b06fb3fca1481a53de5aeaa5263baea9'

LOGIN_REDIRECT_URL = "/login/"
LOGIN_URL = "/login/"

FITAPP_SUBSCRIBE = True
FITAPP_SUBSCRIBER_ID = "1"

APPEND_SLASH = True

from django.contrib.auth.models import User, models
User._meta.get_field('email')._unique = True #dont want duplicate emails if they are being used as sign-in
User._meta.get_field('email')._blank = False

#extend login time
REMEMBER_ME_DURATION = 60 * 60 * 24 * 365 # a year


#########
'''
CELERY
'''
import djcelery
djcelery.setup_loader()

#Broker settings
BROKER_URL='amqp://guest:guest@localhost:5672//'

CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

#Logging options
LOG_LOCATION = BASE_DIR
#LOG_LOCATION = "/var/log/TracktivityPets/"
