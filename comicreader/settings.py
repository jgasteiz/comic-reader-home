import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
SECRET_KEY = os.environ.get("SECRET_KEY", "1234")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "reader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "comicreader.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "comicreader.context_processors.source_revision",
            ]
        },
    }
]

WSGI_APPLICATION = "comicreader.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "NAME": os.environ.get("DATABASE_NAME", "comics"),
        "USER": os.environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "postgres"),
        "PORT": os.environ.get("DATABASE_PORT", 5432),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "collectedstatic")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

IGNORED_FILE_NAMES = [".DS_Store", ".yacreaderlibrary"]

PAGE_NOT_FOUND = "/static/img/404.jpg"

# DRF
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ]
}

# Reader settings
DEFAULT_COMIC_EXTRACT_PATH = os.path.join(BASE_DIR, "static/comics/tmp")
COMIC_EXTRACT_PATH = os.environ.get("COMIC_EXTRACT_PATH", DEFAULT_COMIC_EXTRACT_PATH)
COMICS_ROOT = os.environ.get("COMICS_ROOT")
