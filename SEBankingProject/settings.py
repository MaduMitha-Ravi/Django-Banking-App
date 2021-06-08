import os
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,'templates')
STATIC_DIR = os.path.join(BASE_DIR,'static')
BOOT_DIR = os.path.join(BASE_DIR,'boot')
MEDIA_DIR = os.path.join(BASE_DIR,'media')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h-y2gz04oc&4zc!(q$t6n^9@tp0km@7ff%n!0_s2#m2u8-tnmc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True #False

ALLOWED_HOSTS = ['cs872seproject.herokuapp.com', '127.0.0.1']

TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID'] 
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN'] 


#gmail_send/settings.py

EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER'] 
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD'] 
EMAIL_PORT = '2525'

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',

 }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Banker',
    'Customer',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'widget_tweaks',
    'djmoney',
    'phone_field',
    'django_tables2',
    'bootstrapform',
    'dpd_static_support',
    'bootstrap4',
    'whitenoise.runserver_nostatic',
    'django_twilio',
]



MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django_plotly_dash.middleware.BaseMiddleware',
   # 'django_plotly_dash.middleware.ExternalRedirectionMiddleware',
]

ROOT_URLCONF = 'SEBankingProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                # '/Users/madumitharavi/Documents/UniversityOfRegina/Semester4/SoftwareEngineering/SEProject/SEBankingProject/templates',
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

WSGI_APPLICATION = 'SEBankingProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases



import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

# Adding ASGI Application
ASGI_APPLICATION = 'Customer.routing.application'


STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR,
                 ]

MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = '/media/'
LOGIN_URL = '/Banker/user_login/'
REGISTER_URL = '/Banker/registercustomer/'
CUSTOMERLOGIN_URL = '/Customer/customer_login/'
CUSTOMERMAINPG_URL = '/Customer/customermainpage/'
APPLYLOAN_URL = '/Customer/applyloan'
