DEBUG = False

SECRET_KEY = 'test secret key'

INSTALLED_APPS = [
    'idm_suspension.tests.test_app',
    'idm_suspension',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',
]

DJANGO_ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
