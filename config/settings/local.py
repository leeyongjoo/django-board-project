from .base import *

ALLOWED_HOSTS = []

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

with open('secrets.json') as f:
    SECRET = json.loads(f.read())
SECRET_KEY = SECRET['SECRET_KEY']