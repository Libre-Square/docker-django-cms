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
# REDIS_HOST
# REDIS_PORT

## Optional Environment Variables
# DJANGOCMS_GOOGLEMAP_API_KEY
# MAPS_BINGMAPS_API_KEY
# MAPS_GOOGLEMAPS_API_KEY
# MAPS_HERE_API_KEY = {'app_id': '<str>', 'app_code': '<str>'}
# MAPS_MAPBOX_API_KEY
# MAPS_VIAMICHELIN_API_KEY

import os, io, csv
from mysite.settings import *

CUSTOM_SETTINGS_DIR = '/home/django/custom'

thumbnail_precessors_list = list(THUMBNAIL_PROCESSORS)
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
if 'REDIS_HOST' in os.environ:
    redis_host = os.environ['REDIS_HOST']
    redis_port = '6379'
    if 'REDIS_PORT' in os.environ:
        redis_port = os.environ['REDIS_PORT']
    
    redis_location = 'redis://' + redis_host + ':' + redis_port + '/0'
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_location,
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

## Redis channels
if 'REDIS_HOST' in os.environ:
    channel_redis_host = os.environ['REDIS_HOST']
    channel_redis_port = 6379
    if 'REDIS_PORT' in os.environ:
        channel_redis_port = int(os.environ['REDIS_PORT'])

    installed_apps_list += ['channels']
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(channel_redis_host, channel_redis_port)],
            },
            "ROUTING": "livecache.routing.channel_routing",
        },
    }

## Google Map API Key for djangocms_googlemap
if 'DJANGOCMS_GOOGLEMAP_API_KEY' in os.environ:
    DJANGOCMS_GOOGLEMAP_API_KEY = os.environ['DJANGOCMS_GOOGLEMAP_API_KEY']
    MAPS_GOOGLEMAPS_API_KEY = os.environ['DJANGOCMS_GOOGLEMAP_API_KEY']

## aldryn-bootstrap3
installed_apps_list += ['aldryn_bootstrap3']

## aldryn-newsblog
installed_apps_list += [
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'reversion',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'parler',
    'sortedm2m',
    'taggit'
]

if 'easy_thumbnails.processors.scale_and_crop' in thumbnail_precessors_list:
    thumbnail_precessors_list.insert(thumbnail_precessors_list.index('easy_thumbnails.processors.scale_and_crop'), 'filer.thumbnail_processors.scale_and_crop_with_subject_location')
    thumbnail_precessors_list.remove('easy_thumbnails.processors.scale_and_crop')

## cmsplugin-markdown
installed_apps_list += [
    'django_markwhat',
    'cmsplugin_markdown'
]

## djangocms-history
installed_apps_list += ['djangocms_history']

## djangocms-timed
installed_apps_list += ['djangocms_timed']

## djangocms-light-gallery
installed_apps_list += ['light_gallery']

## djangocms-maps
installed_apps_list += ['djangocms_maps']

## livecache
installed_apps_list += ['livecache']

##  Map API Keys for djangocms-maps
if 'MAPS_BINGMAPS_API_KEY' in os.environ:
    MAPS_BINGMAPS_API_KEY = os.environ['MAPS_BINGMAPS_API_KEY']

if 'MAPS_GOOGLEMAPS_API_KEY' in os.environ:
    MAPS_GOOGLEMAPS_API_KEY = os.environ['MAPS_GOOGLEMAPS_API_KEY']

if 'MAPS_HERE_API_KEY' in os.environ:
    MAPS_HERE_API_KEY = os.environ['MAPS_HERE_API_KEY']

if 'MAPS_MAPBOX_API_KEY' in os.environ:
    MAPS_MAPBOX_API_KEY = os.environ['MAPS_MAPBOX_API_KEY']

if 'MAPS_VIAMICHELIN_API_KEY' in os.environ:
    MAPS_VIAMICHELIN_API_KEY = os.environ['MAPS_VIAMICHELIN_API_KEY']

THUMBNAIL_PROCESSORS = tuple(thumbnail_precessors_list)
INSTALLED_APPS = tuple(list(INSTALLED_APPS) + list(set(installed_apps_list) - set(INSTALLED_APPS)))
MIDDLEWARE_CLASSES = tuple(middleware_classes_list)

