# -*- coding: utf-8 -*-
#!/usr/bin/env python
import os
from easy_thumbnails.conf import Settings as thumbnail_settings
# import djcelery


CURRPATH = os.path.abspath('.')

PROJECT_PATH = os.path.abspath(
    os.path.dirname(__file__).decode('utf-8')).replace('\\', '/')

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
ROOT_URLCONF = 'project.urls'

DATA_IMPORTER_EXCEL_DECODER = 'cp1252'
DATA_IMPORTER_DECODER = 'UTF-8'

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(CURRPATH, 'cover')
COVERAGE_PATH_EXCLUDES = os.path.join(CURRPATH, 'cover')
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEFAULT_CHARSET = 'utf-8'

AUTH_PROFILE_MODULE = 'accounts.MemberProfile'
ADMIN_EMAIL = 'greenteamer@bk.ru'
ADMINS = (
)

"""celery"""
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERY_ALWAYS_EAGER = False
BROKER_BACKEND = "djkombu.transport.DatabaseTransport"
"""celery end"""


MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

ugettext = lambda s: s

LANGUAGES = (
    ('en', ugettext('English')),
    ('ru', ugettext('Russian')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = 'C:/webmagazinedjango/webshop/static/media/'
# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media').replace('\\', '/')
MEDIA_ROOT = '%s/media' % CURRPATH
IMPORT_XLS = '%s/import_xls' % MEDIA_ROOT
CKEDITOR_UPLOAD_PATH = '/media/uploads'
DIRECTORY = os.path.join(CURRPATH, 'media/uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''
# STATIC_ROOT = '%s/static' % CURRPATH
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(CURRPATH, 'static').replace('\\', '/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'rs!w229&m79-)f3ohat)gd=aiodjf3)^3#3(*1)k4-)*qwc^4zgom9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'pybb.middleware.PybbMiddleware',
    #'webshop.SSLMiddleware.SSLRedirect',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates').replace('\\', '/'),
)


# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'pybb.context_processors.processor',
)


# DAJAXICE_MEDIA_PREFIX="dajaxice"

# DAJAX_FUNCTIONS=(
#     'webshop.ajaxapp.ajax.order_form',
#     'webshop.ajaxapp.ajax.send_form',
# )


TINYMCE_JS_URL = os.path.join(CURRPATH, '/libraries/tinymce/tinymce.min.js')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace",
    'theme': "advanced",
}
TINYMCE_SPELLCHECKER = True
TINYMCE_COMPRESSOR = True


SOUTH_MIGRATION_MODULES = {
    'captcha': 'captcha.south_migrations',
    # 'sitetree': 'sitetree.south_migrations',
}

INPLACEEDIT_DISABLE_CLICK = False
THUMBNAIL_DEBUG = True
INPLACEEDIT_EVENT = "click"

ADAPTOR_INPLACEEDIT = {
    'auto_fk': 'inplaceeditform_extra_fields.\
        fields.AdaptorAutoCompleteForeingKeyField',

    'auto_m2m': 'inplaceeditform_extra_fields.fields.\
        AdaptorAutoCompleteManyToManyField',

    'image_thumb': 'inplaceeditform_extra_fields.\
        fields.AdaptorImageThumbnailField',

    'tiny': 'inplaceeditform_extra_fields.\
        fields.AdaptorTinyMCEField',

    'ckeditor': 'inplaceeditform_extra_fields.fields.\
        AdaptorCKEDITORField',
}
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    # Uncomment the next line to enable the admin:
    # 'grappelli',
    'filebrowser',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'bootstrap3',
    'sorl.thumbnail',
    # 'dajaxice',
    # 'dajax',
    'south',
    'captcha',
    'ckeditor',
    'tinymce',
    # 'djcelery',
    'djkombu',
    'mptt',
    'project.core',
    'project.accounts',
    'django_coverage',
    'mptt_tree_editor',
    'pybb',
    'project.pristroy',
    'project.cart',
    'image_cropping',
    'easy_thumbnails',
    'import_export',
    'project.notifications',
    'project.documentation',
    'tastypie',
    'crispy_forms',
    'ckeditor',
    # 'debug_toolbar',
)

FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_STATIC_ROOT = STATIC_ROOT
FILEBROWSER_STATIC_URL = STATIC_URL
URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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

# Custom settings
ENABLE_SSL = False
SITE_NAME = u'Product magazine'
META_KEYWORDS = u'products, online, shop, buy'
META_DESCRIPTION = u'Product magazine is an online supplier of products'
LOGIN_REDIRECT_URL = '/accounts/my_account/'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 90  # 90 дней на хранение cookies
PRODUCTS_PER_PAGE = 300
AUTH_PROFILE_MODULE = 'accounts.UserProfile'

# ROBOKASSA_LOGIN = 'tai'
# ROBOKASSA_PASSWORD1 = 'polythai2014'
# ROBOKASSA_PASSWORD2 = 'polythai2014secondPass'
# ROBOKASSA_TEST_MODE = True

try:
    from settings_local import *
except ImportError:
    pass


PYBB_ATTACHMENT_ENABLE = True
PYBB_DEFAULT_TITLE = 'Форум сайта совместных покупок'
