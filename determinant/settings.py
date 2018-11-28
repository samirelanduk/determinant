# Settings for samireland.com

import os
from .secrets import SECRET_KEY, BASE_DIR, DATABASES

ALLOWED_HOSTS = []

DEBUG = True

ROOT_URLCONF = "determinant.urls"

INSTALLED_APPS = [
 "django.contrib.contenttypes",
 "django.contrib.staticfiles",
 "django.contrib.auth",
 "django.contrib.sessions",
 "django.contrib.messages",
 "django.contrib.humanize",
 "sass_processor",
 "determinant"
]

DATE_FORMAT = "D j M, Y"
USE_TZ = True
TIME_ZONE = "Europe/London"

MIDDLEWARE = [
 "django.contrib.sessions.middleware.SessionMiddleware",
 "django.middleware.common.CommonMiddleware",
 "django.middleware.csrf.CsrfViewMiddleware",
 "django.contrib.auth.middleware.AuthenticationMiddleware",
 "django.contrib.messages.middleware.MessageMiddleware"
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.abspath(f"{BASE_DIR}/../static")
SASS_PROCESSOR_ROOT = os.path.abspath(f"{BASE_DIR}/determinant/static")
MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")
MEDIA_URL = "/uploads/"

TEMPLATES = [{
 "BACKEND": "django.template.backends.django.DjangoTemplates",
 "APP_DIRS": True,
 "OPTIONS": {
  "context_processors": [
   "django.contrib.auth.context_processors.auth",
   "django.contrib.messages.context_processors.messages"
  ],
 },
}]
