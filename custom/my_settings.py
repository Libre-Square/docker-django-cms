## Expected Environment Variables
# LANGUAGE_CODE
# TIME_ZONE
# LANGUAGES
# DATABASE_ENGINE
# DATABASE_HOST
# DATABASE_PORT
# DATABASE_NAME
# DATABASE_USER
# DATABASE_PASSWORD
# CACHE_REDIS_HOST
# CACHE_REDIS_PORT
# DJANGOCMS_GOOGLEMAP_API_KEY

import os, io, csv
from mysite.settings import *

CUSTOM_SETTINGS_DIR = '/home/django/custom'

installed_apps_list = list(INSTALLED_APPS)
middleware_classes_list = list(MIDDLEWARE_CLASSES)

DEBUG = False
ALLOWED_HOSTS = ['*']

if 'LANGUAGE_CODE' in os.environ:    
    LANGUAGE_CODE = os.environ['LANGUAGE_CODE']

if 'TIME_ZONE' in os.environ:
    TIME_ZONE = os.environ['TIME_ZONE']

if 'LANGUAGES' in os.environ:
    LANGUAGES = ()
    CMS_LANGUAGES[1] = []
    
    language_list = list(csv.reader(io.StringIO(os.environ['LANGUAGES']), delimiter=';'))[0]
    for language in language_list:
        language_param = list(csv.reader(io.StringIO(language), delimiter=':'))[0]
        language_code = language_param[0]
        language_name = language_param[1]
        LANGUAGES += ((language_code, gettext(language_name)),)
        CMS_LANGUAGES[1] += [{
            'code': language_code,
            'name': gettext(language_name),
            'public': True,
            'redirect_on_fallback': True,
            'hide_untranslated': False,
        }]

TEMPLATES[0]['DIRS'] = [os.path.join(CUSTOM_SETTINGS_DIR, 'templates'),]
CMS_TEMPLATES = ()

for file in os.listdir(os.path.join(CUSTOM_SETTINGS_DIR, 'templates')):
    if file.endswith(".html"):
        template_name = os.path.splitext(file.capitalize())[0]
        CMS_TEMPLATES += ((file, template_name),)

## PostgreSQL
if 'DATABASE_ENGINE' in os.environ:
    DATABASES['default']['ENGINE'] = os.environ['DATABASE_ENGINE']
    
if 'DATABASE_HOST' in os.environ:
    DATABASES['default']['HOST'] = os.environ['DATABASE_HOST']

if 'DATABASE_PORT' in os.environ:
    DATABASES['default']['PORT'] = os.environ['DATABASE_PORT']
    
if 'DATABASE_NAME' in os.environ:
    DATABASES['default']['NAME'] = os.environ['DATABASE_NAME']
    
if 'DATABASE_USER' in os.environ:
    DATABASES['default']['USER'] = os.environ['DATABASE_USER']
    
if 'DATABASE_PASSWORD' in os.environ:
    DATABASES['default']['PASSWORD'] = os.environ['DATABASE_PASSWORD']

## Redis Cache
if 'CACHE_REDIS_HOST' in os.environ:
    cache_redis_host = os.environ['CACHE_REDIS_HOST']
    cache_redis_port = '6379'
    if 'CACHE_REDIS_PORT' in os.environ:
        cache_redis_portredis_port = os.environ['CACHE_REDIS_PORT']
    
    cache_redis_location = 'redis://' + cache_redis_host + ':' + cache_redis_port + '/0'
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": cache_redis_location,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
                'CONNECTION_POOL_CLASS_KWARGS': {
                    'max_connections': 100,
                    'timeout': 20,
                },
                "COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",
                "IGNORE_EXCEPTIONS": True,
            },
        }
    }
    DJANGO_REDIS_IGNORE_EXCEPTIONS = True
    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

    middleware_classes_list.insert(0, 'django.middleware.cache.UpdateCacheMiddleware')
    middleware_classes_list += ['django.middleware.cache.FetchFromCacheMiddleware']

    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 600
    CACHE_MIDDLEWARE_KEY_PREFIX = ''

    CMS_CACHE_DURATIONS = {
        'content': 600,
        'menus': 3600,
        'permissions': 3600,
    }
    CMS_CACHE_PREFIX = 'djangocms'
    CMS_PLACEHOLDER_CACHE = True
    CMS_PAGE_CACHE = True
    CMS_PLUGIN_CACHE = True

## Google Map API Key for djangocms_googlemap
if 'DJANGOCMS_GOOGLEMAP_API_KEY' in os.environ:
    DJANGOCMS_GOOGLEMAP_API_KEY = os.environ['DJANGOCMS_GOOGLEMAP_API_KEY']

INSTALLED_APPS = tuple(list(INSTALLED_APPS) + list(set(installed_apps_list) - set(INSTALLED_APPS)))
MIDDLEWARE_CLASSES = tuple(middleware_classes_list)

