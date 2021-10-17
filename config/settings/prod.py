import os

from .base import *

ALLOWED_HOSTS = ['3.35.91.242', 'board.leeyongjoo.site']

STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
]

DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']