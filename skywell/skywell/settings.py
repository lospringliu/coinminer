"""
Django settings for skywell project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o#+pkrk+r4u@3$iyqjv11gnqs@5zj$-zi8p8i-f@@vmmg22#1t'

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = False


TEMPLATE_DEBUG = True

ALLOWED_HOSTS = [ '*', ]


# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.sites',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'south',
	'mptt',
	'common',
	'userprofiles',
	'reports',
	'issues',
	'qq_open',
	'social.apps.django_app.default',
	'authextension',
)
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.debug",
	"django.core.context_processors.i18n",
	"django.core.context_processors.media",
	"django.core.context_processors.static",
	"django.core.context_processors.tz",
	"django.contrib.messages.context_processors.messages",
	'social.apps.django_app.context_processors.backends',
	'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'skywell.urls'

WSGI_APPLICATION = 'skywell.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
	'default': {
#		'ENGINE': 'django.db.backends.sqlite3',
#		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'skywell',					# Or path to database file if using sqlite3.
		'HOST': 'skywell.cp6tehgcsvuh.us-west-2.rds.amazonaws.com',				   # Set to empty string for localhost. Not used with sqlite3.
		'USER': 'skywell',				   # Not used with sqlite3.
		'PASSWORD': '',			   # Not used with sqlite3.
		'PORT': '',  
	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
SITE_ID = 1
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	)

MEDIA_ROOT = os.path.join(BASE_DIR,'media/')
MEDIA_RUL = '/media/'
MPTT_ADMIN_LEVEL_INDENT = 20
#SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.User'
AUTHENTICATION_BACKENDS=('social.backends.google.GoogleOAuth2','social.backends.qq.QQOAuth2','authextension.backendsflex.FlexBackend','django.contrib.auth.backends.ModelBackend')
AUTH_PROFILE_MODULE='userprofiles.UserProfile'
TEMPLATE_DIRS = (
	os.path.join(BASE_DIR,'templates'),
)
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
		)
#EMAIL_HOST = '127.0.0.1'
DEFAULT_FROM_EMAIL = 'SkywellPasswordReset<lospringliu@qq.com>'
EMAIL_FROM = 'SkywellPasswordReset<lospringliu@qq.com>'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = '9818674'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_SSL = True
EMAIL_USE_TLS = True
LOGIN_URL = "/django/accounts/login/"
LOGIN_REDIRECT_URL = "/django/"
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
#SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
SOCIAL_LOGIN_URL = "/django/socialhome/"
SOCIAL_LOGIN_REDIRECT_URL = "/django/socialhome/"
SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/django/socialhome/"
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/django/qqlogin"
LOGOUT_URL="/django/sociallogout/"
SOCIAL_AUTH_QQ_KEY = '101055994'
SOCIAL_AUTH_QQ_SECRET = ''
#SOCIAL_AUTH_QQ_KEY = '37642912'
#SOCIAL_AUTH_QQ_SECRET = '686f312f464fef4611fe736ede5c31cd'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "ikVEtbDODUhLzZhRFd_M3XgN"
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'email']
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email','first_name','last_name']
SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_EMAIL_FORM_URL = '/django/signup-email'
SOCIAL_AUTH_EMAIL_FORM_HTML = 'email_signup.html'
SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'authextension.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/django/email-sent/'
SOCIAL_AUTH_USERNAME_FORM_URL = '/django/signup-username'
SOCIAL_AUTH_USERNAME_FORM_HTML = 'username_signup.html'
SOCIAL_AUTH_PIPELINE = (
	'social.pipeline.social_auth.social_details',
	'social.pipeline.social_auth.social_uid',
	'social.pipeline.social_auth.auth_allowed',
	'social.pipeline.social_auth.social_user',
	'social.pipeline.user.get_username',
	'authextension.pipeline.require_info',
	'social.pipeline.mail.mail_validation',
	'authextension.pipeline.user_by_email',
	'social.pipeline.user.create_user',
	'social.pipeline.social_auth.associate_user',
	'social.pipeline.social_auth.load_extra_data',
	'social.pipeline.user.user_details',
	'social.pipeline.debug.debug'
)
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/django/socialhome/'
FORCE_EMAIL_VALIDATION = True
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '/tmp/django.log',
		},
	},	
	'loggers': {
		'django.request': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}

