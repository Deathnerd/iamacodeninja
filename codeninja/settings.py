__author__ = 'Deathnerd'
import os


class Base():
	"""Base Config"""
	# General App
	ENV = os.environ['CODENINJA_SERVER_ENV']
	SECRET_KEY = os.environ['CODENINJA_SECRET_KEY']
	APP_DIR = os.path.abspath(os.path.dirname(__file__))
	PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

	# SQLAlchemy
	SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}/{}?charset=utf8".format(os.environ['CODENINJA_DATABASE_USER'],
																		os.environ['CODENINJA_DATABASE_PASS'],
																	   	os.environ['CODENINJA_DATABASE_HOST'],
																	   	os.environ['CODENINJA_DATABASE_NAME'])

	# Bcrypt
	BCRYPT_LOG_ROUNDS = 13

	# Debug Toolbar
	DEBUG_TB_ENABLED = False
	DEBUG_TB_INTERCEPT_REDIRECTS = False

	# Flask-Assets
	ASSETS_DEBUG = False

	# WTForms
	WTF_CSRF_ENABLED = True
	WTF_CSRF_SECRET_KEY = os.environ['CODENINJA_WTF_CSRF_SECRET_KEY']
	RECAPTCHA_PUBLIC_KEY = os.environ['CODENINJA_RECAPTCHA_PUBLIC_KEY']
	RECAPTCHA_PRIVATE_KEY = os.environ['CODENINJA_RECAPTCHA_PRIVATE_KEY']


class Production(Base):
	"""Production Config"""
	DEBUG = False
	DEBUG_TB_ENABLED = False


class Development(Base):
	"""Development Config"""
	# General App
	DEBUG = True

	# SQLAlchemy

	# Debug Toolbar
	DEBUG_TB_ENABLED = True
	DEBUG_TB_PROFILER_ENABLED = True
	# DEBUG_TB_INTERCEPT_REDIRECTS = True
	DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True

	# Flask-Assets
	ASSETS_DEBUG = True

	# WTF-Forms


class Staging(Base):
	"""Staging Config"""
	# General App
	TESTING = True
	DEBUG = True

	# Bcrypt
	BCRYPT_LOG_ROUNDS = 1

	# WTForms