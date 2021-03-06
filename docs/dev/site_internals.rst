.. doctest docs/dev/site_internals.rst

===================================
More about the :class:`Site` class
===================================

.. contents::
    :depth: 1
    :local:


.. currentmodule:: lino.core.site


Here are the Django settings that :class:`Lino` puts into the global context of
a settings module:

>>> from lino_book.projects.min9.settings import Site
>>> pseudoglobals = {}
>>> SITE = Site(pseudoglobals)
>>> sorted(pseudoglobals.keys())
... #doctest: +ELLIPSIS +REPORT_UDIFF +NORMALIZE_WHITESPACE
['AUTHENTICATION_BACKENDS', 'AUTH_USER_MODEL', 'DATABASES', 'FIXTURE_DIRS', 'INSTALLED_APPS', 'LANGUAGES', 'LANGUAGE_CODE', 'LOCALE_PATHS', 'LOGIN_REDIRECT_URL', 'LOGIN_URL', 'LOGOUT_REDIRECT_URL', 'MEDIA_ROOT', 'MEDIA_URL', 'MIDDLEWARE', 'ROOT_URLCONF', 'SERIALIZATION_MODULES', 'STATIC_ROOT', 'STATIC_URL', 'TEMPLATES', 'USE_L10N']

Note that Lino writes to your settings module's global namespace only
while the Site class gets *instantiated*.  So if for some reason you
want to modify one of the settings, do it *after* your
``SITE=Site(globals())`` line.




Additional local apps
=====================

An optional second positional argument can be specified by the  :term:`site
maintainer` in order to specify additional *local plugins*. These will go into
the :setting:`INSTALLED_APPS` setting, together with any other plugins needed by
them.

>>> from lino_book.projects.min9.settings import Site
>>> pseudoglobals = {}
>>> Site(pseudoglobals, "lino_xl.lib.events")  #doctest: +ELLIPSIS
<lino_book.projects.min9.settings.Site object at ...>
>>> print('\n'.join(pseudoglobals['INSTALLED_APPS']))
... #doctest: +REPORT_UDIFF +NORMALIZE_WHITESPACE
lino
django.contrib.staticfiles
lino.modlib.about
lino.modlib.jinja
lino.modlib.bootstrap3
lino.modlib.extjs
lino.modlib.office
lino_xl.lib.xl
lino_xl.lib.countries
lino.modlib.printing
lino.modlib.system
lino_book.projects.min9.modlib.contacts
django.contrib.contenttypes
lino.modlib.gfks
lino_xl.lib.excerpts
lino.modlib.users
lino.modlib.checkdata
lino_xl.lib.addresses
lino_xl.lib.phones
lino_xl.lib.cal
lino_xl.lib.reception
lino_xl.lib.courses
lino.modlib.weasyprint
lino.modlib.uploads
lino_xl.lib.ledger
lino_xl.lib.sepa
lino.modlib.memo
lino_xl.lib.notes
lino_xl.lib.humanlinks
lino_xl.lib.households
lino_xl.lib.calview
lino_xl.lib.pages
lino.modlib.export_excel
lino_xl.lib.dupable_partners
lino.modlib.tinymce
lino_xl.lib.appypod
lino.modlib.notify
lino.modlib.changes
lino.modlib.comments
lino_xl.lib.properties
lino.modlib.languages
lino_xl.lib.cv
lino_cosi.lib.cosi
lino_xl.lib.b2c
lino_xl.lib.products
lino_xl.lib.vat
lino_xl.lib.sales
lino_xl.lib.finan
lino_xl.lib.events
django.contrib.sessions

As an :term:`application developer` you won't specify this argument, you should
specify your installed plugins by overriding :meth:`get_installed_apps
<lino.core.site.Site.get_installed_apps>`.

Besides this you can override any class argument using a keyword
argment of same name:

- :attr:`lino.core.site.Site.title`
- :attr:`lino.core.site.Site.verbose_name`

You've maybe heard that it is not allowed to modify Django's settings
once it has started.  But there's nothing illegal with this here
because this happens before Django has seen your :xfile:`settings.py`.

Lino does more than this. It will for example read the `__file__
<http://docs.python.org/2/reference/datamodel.html#index-49>`__
attribute of this, to know where your :file:`settings.py` is in the
file system.



Technical details
=================

Here are the Django settings that Lino will override:

>>> from lino.core.site import TestSite as Site
>>> SITE = Site()
>>> print([k for k in SITE.django_settings.keys() if k.isupper()])
... #doctest: +NORMALIZE_WHITESPACE
['SECRET_KEY', 'DATABASES', 'SERIALIZATION_MODULES', 'LANGUAGES',
'INSTALLED_APPS', 'MEDIA_ROOT', 'ROOT_URLCONF', 'MEDIA_URL', 'STATIC_ROOT',
'STATIC_URL', 'TEMPLATES', 'MIDDLEWARE', 'AUTHENTICATION_BACKENDS', 'LOGIN_URL',
'LOGIN_REDIRECT_URL', 'LOGOUT_REDIRECT_URL', 'FIXTURE_DIRS', 'LOCALE_PATHS']

>>> from pprint import pprint
>>> from atelier.utils import rmu
>>> pprint(rmu(SITE.django_settings))
... #doctest: +ELLIPSIS +REPORT_UDIFF +NORMALIZE_WHITESPACE
{'AUTHENTICATION_BACKENDS': ['lino.core.auth.backends.ModelBackend'],
 'DATABASES': {'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': '.../core/default.db'}},
 'FIXTURE_DIRS': (),
 'INSTALLED_APPS': ('lino',
                    'django.contrib.staticfiles',
                    'lino.modlib.about',
                    'lino.modlib.jinja',
                    'lino.modlib.bootstrap3',
                    'lino.modlib.extjs'),
 'LANGUAGES': [('en', 'English')],
 'LOCALE_PATHS': (),
 'LOGIN_REDIRECT_URL': '/',
 'LOGIN_URL': '/accounts/login/',
 'LOGOUT_REDIRECT_URL': None,
 'MEDIA_ROOT': '.../core/media',
 'MEDIA_URL': '/media/',
 'MIDDLEWARE': ('django.middleware.common.CommonMiddleware',
                'lino.core.auth.middleware.NoUserMiddleware',
                'lino.utils.ajax.AjaxExceptionResponse'),
 'ROOT_URLCONF': 'lino.core.urls',
 'SECRET_KEY': '20227',
 'SERIALIZATION_MODULES': {'py': 'lino.utils.dpy'},
 'STATIC_ROOT': '...static_root',
 'STATIC_URL': '/static/',
 'TEMPLATES': [{'APP_DIRS': True,
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                                   'django.template.context_processors.i18n',
                                                   'django.template.context_processors.media',
                                                   'django.template.context_processors.static',
                                                   'django.template.context_processors.tz',
                                                   'django.contrib.messages.context_processors.messages']}},
               {'BACKEND': 'django.template.backends.jinja2.Jinja2',
                'DIRS': [],
                'OPTIONS': {'environment': 'lino.modlib.jinja.get_environment'}}],
 '__file__': '.../lino/core/site.py...'}


Here are the Django settings which Lino does not modify:

>>> import lino_book.projects.lydia.settings.demo as settings
>>> print([s for s in dir(settings)
...     if not s in SITE.django_settings and s[0].isupper()])
... #doctest: +NORMALIZE_WHITESPACE
['ADMINS', 'ALLOWED_HOSTS', 'AUTH_USER_MODEL', 'DEBUG',
'DEBUG_PROPAGATE_EXCEPTIONS', 'EMAIL_HOST', 'LANGUAGE_CODE', 'MANAGERS',
'SETUP_INFO', 'SITE', 'Site', 'TEMPLATE_DEBUG', 'TEST_RUNNER', 'TIM2LINO_LOCAL',
'TIM2LINO_USERNAME', 'TIME_ZONE', 'USE_I18N', 'USE_L10N', 'USE_TZ']
