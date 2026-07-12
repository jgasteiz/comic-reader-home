import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# Datadog APM + logging
# ---------------------------------------------------------------------------
DD_ENABLED = os.environ.get("DD_ENABLED", "0") == "1"

if DD_ENABLED:
    from ddtrace import config as dd_config, patch_all

    patch_all()

    dd_config.django["service_name"] = os.environ.get("DD_SERVICE", "comic-reader-home")
    dd_config.django["analytics_enabled"] = True

    # ddtrace injects trace/span IDs into log records when DD_LOGS_INJECTION=true.
    # The format below surfaces those fields so the Datadog Agent can correlate logs with traces.
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "datadog": {
                "format": (
                    "%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] "
                    "[dd.service=%(dd.service)s dd.env=%(dd.env)s "
                    "dd.version=%(dd.version)s "
                    "dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] "
                    "%(message)s"
                ),
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "datadog",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": os.environ.get("LOG_LEVEL", "INFO"),
        },
    }


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

ROOT_URLCONF = "core.urls"

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
                "core.context_processors.source_revision",
            ]
        },
    }
]

WSGI_APPLICATION = "core.wsgi.application"

if os.environ.get("USE_POSTGRES", "0") == "1":
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
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

IGNORED_FILE_NAMES = [".DS_Store", ".yacreaderlibrary"]

PAGE_NOT_FOUND = "/static/img/404.jpg"

# Reader settings
COMICS_SRC_PATH = os.environ.get("COMICS_SRC_PATH")
COMICS_EXTRACT_PATH = os.environ.get(
    "COMICS_EXTRACT_PATH", os.path.join(BASE_DIR, "static/comics/tmp")
)
