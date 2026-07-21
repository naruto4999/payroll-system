from .settings import *  # noqa: F401,F403


DEBUG = False
SECRET_KEY = SECRET_KEY or "test-secret-key"
ALLOWED_HOSTS = ["testserver", "localhost"]
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

DATABASES["default"]["TEST"] = {
    "NAME": os.environ.get("DB_TEST_NAME", "payroll_system_test"),
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
