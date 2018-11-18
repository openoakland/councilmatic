# These are all the settings that are specific to a deployment

import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4l1ttl3l3ssconv3rs4ti0n*'

# SECURITY WARNING: don't run with debug turned on in production!
# Set this to True while you are developing
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oakland_councilmatic',
        'USER': 'postgres',
        'PASSWORD': 'str0ng*p4ssw0rd',
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://solr:8983/solr'
        # ...or for multicore...
        # 'URL': 'http://127.0.0.1:8983/solr/chicago',
    },
}

# Remember to run python manage.py createcachetable so this will work! 
# developers, set your BACKEND to 'django.core.cache.backends.dummy.DummyCache'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'councilmatic_cache',
    }
}

# Set this to flush the cache at /flush-cache/{FLUSH_KEY}
FLUSH_KEY = 'secret_flush'

# Set this to allow Disqus comments to render
DISQUS_SHORTNAME = None

# analytics tracking code
ANALYTICS_TRACKING_CODE = 'foo'

HEADSHOT_PATH = os.path.join(os.path.dirname(__file__), '..'
                             '/oakland/static/images/')

EXTRA_APPS = ()



