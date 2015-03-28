# Django settings for rendezvous project.
import os

PROJECT_PATH = 'C:/django/rendezvous/'
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
	('Tuomas Rintamaki', 'tuomas.rintamaki@aalto.fi')
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'C:/django/rendezvous/db.sqlite3',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_PATH + 'media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	PROJECT_PATH + '/static/',
	PROJECT_PATH + '/static/bootstrap/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0xji=92sgq1i)(6f^*b+b4ls7#&amp;r1_+!mcemn+j+4ri1&amp;d$z+&amp;'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	'social_auth.backends.contrib.linkedin.LinkedinBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
	'django.core.context_processors.static',
	'django.core.context_processors.csrf',
    'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'django.contrib.auth.context_processors.auth',
	'social_auth.context_processors.social_auth_by_name_backends',
	'social_auth.context_processors.social_auth_backends',
	'social_auth.context_processors.social_auth_by_type_backends',
	'social_auth.context_processors.social_auth_login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rendezvous.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rendezvous.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	PROJECT_PATH + '/rendezvous/templates/',
	PROJECT_PATH + '/scheme/templates/',
	PROJECT_PATH + '/users/templates/',
	PROJECT_PATH + '/skills/templates/',
	PROJECT_PATH + '/linkedin_integration/templates/',
	PROJECT_PATH + '/messaging/templates/',
	PROJECT_PATH + '/positions/templates/',
)

# New in Django 1.5
AUTH_USER_MODEL = 'users.UserProfile'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'positions',
	'schemes',
	'users',
	'skills',
	'social_auth',
	'linkedin_integration',
	'messaging',
    'django.contrib.admin',
    'cities_light',
    'geolocation',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

SOCIAL_AUTH_USER_MODEL = 'users.UserProfile'

LINKEDIN_CONSUMER_KEY = 'yfj4did167fh'
LINKEDIN_CONSUMER_SECRET = '6fIQHa4uIJWAs8Ci'

LOGIN_URL          = '/login/'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/linkedin/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = SOCIAL_AUTH_NEW_USER_REDIRECT_URL
LOGIN_ERROR_URL    = '/error/'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

# Add email to requested authorizations.
LINKEDIN_SCOPE = ['r_basicprofile', 'r_emailaddress', 'r_fullprofile', 'r_network']
# Add the fields so they will be requested from linkedin.
LINKEDIN_EXTRA_FIELD_SELECTORS = [
    'email-address',
    'headline',
    'industry',
    'location',
    'summary',
    'specialties',
    'positions',
    'educations',
    'skills',
    'public-profile-url',
    'location',
    'connections',
    'num-connections',
]
# Arrange to add the fields to UserSocialAuth.extra_data
LINKEDIN_EXTRA_DATA = [('id', 'id'),
                       ('first-name', 'first_name'),
                       ('last-name', 'last_name'),] + [
                           (field, field.replace('-', '_'), True)
                           for field in LINKEDIN_EXTRA_FIELD_SELECTORS
                       ]
					   
SOCIAL_AUTH_PIPELINE = (
	'social_auth.backends.pipeline.social.social_auth_user',
	'social_auth.backends.pipeline.user.get_username',
	'social_auth.backends.pipeline.user.create_user',
	'social_auth.backends.pipeline.social.associate_user',
	'social_auth.backends.pipeline.social.load_extra_data',
	'social_auth.backends.pipeline.user.update_user_details',
	'social_auth.backends.pipeline.associate.associate_by_email',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
