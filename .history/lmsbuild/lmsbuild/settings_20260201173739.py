"""
Django settings for lmsbuild project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-f4a!4^mv9t16@l!(w0#(d_njfhq3dr98c@g(i!q4u72q&4ca4i'

DEBUG = True

ALLOWED_HOSTS = []


# ================= INSTALLED APPS =================

INSTALLED_APPS = [

    # ---------- JAZZMIN (ADMIN UI) ----------
    "jazzmin",

    # ---------- DJANGO DEFAULT ----------
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ---------- LMS APPS ----------
    'accounts.apps.AccountsConfig',
    'courses',
    'enrollments',
    'study',
    'attendance.apps.AttendanceConfig',
    "core_settings",
    'profiles.apps.ProfilesConfig',
    'assignments.apps.AssignmentsConfig',
    "message.apps.MessageConfig",
]


AUTH_USER_MODEL = 'accounts.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "login"
LOGOUT_REDIRECT_URL = "login"


# ================= MIDDLEWARE =================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'lmsbuild.urls'


# ================= TEMPLATES =================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'lmsbuild.wsgi.application'


# ================= DATABASE =================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ================= PASSWORD VALIDATORS =================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ================= INTERNATIONAL =================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ================= STATIC & MEDIA =================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ================= FILE UPLOAD LIMITS =================

DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000   # 500MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000   # 500MB


# ================= JAZZMIN SETTINGS =================

JAZZMIN_SETTINGS = {

    "site_title": "LMS Admin",
    "site_header": "Learning Management System",
    "site_brand": "LMS",

    "site_logo": "img/logo.png",   # 👈 correct way

    "welcome_sign": "Welcome to LMS Dashboard",

    "theme": "darkly",

    "topmenu_links": [
        {"name": "Home", "url": "admin:index"},
    ],
    "icons": {
        "accounts.user": "fas fa-users",
        "courses.course": "fas fa-book",
        "assignments.assignment": "fas fa-tasks",
        "profiles.student": "fas fa-user-graduate",
        "profiles.teacherprofile": "fas fa-chalkboard-teacher",
    },
}
