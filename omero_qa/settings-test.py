from settings import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'TEST_CHARSET': 'UTF8',
    'NAME': ':memory:',
    'TEST_NAME': ':memory:',
}

SECRET_KEY = 'test_key'

DEBUG = False
TEMPLATE_DEBUG = DEBUG

