.. doctest docs/dev/site.rst
.. _dev.site:

===================================
Introducing the :class:`Site` class
===================================

.. contents::
    :depth: 1
    :local:


.. currentmodule:: lino.core.site

Your application is defined by its :class:`Site` class
======================================================

As explained in :doc:`settings` and :doc:`/dev/polls/index`,  a :term:`Lino
site` is when a :term:`Django settings module` has a variable named
:setting:`SITE`, and this variable must contain an instance of some subclass of
the :class:`lino.core.site.Site` class.

This top-level :class:`Site` class is the ancestor of all Lino applications. It
is designed to be subclassed by the :term:`application developer`, then imported
into a local :xfile:`settings.py`, where a :term:`site maintainer` may possibly
subclass it another time. A :term:`Lino site` starts to "live" when such a
:class:`Site` class gets **instantiated** in a :term:`Django settings module`.

This concept brings an additional level of encapsulation to Django. Django
settings usually contain simple values (strings, integers, or lists or
dictionaries thereof).  But Lino's :setting:`SITE` setting holds a *Python
object*, with methods that can be called by application code at runtime.

To hook this into Django, imagine the :class:`Site` *class* as a kind of a
"project model". Read :doc:`application` if you wonder why we chose that name.

In other words, the central and fundamental definition of a :term:`Lino
application` is formulated by a :class:`Site` class object. This  :class:`Site`
class object is *not* defined in a :term:`Django settings module` but as part of
the Python package that implements your application. For example, the
:class:`Site` class for :ref:`voga` is defined in the module
:mod:`lino_voga.lib.voga.settings`.

Note that this module *defines* a :class:`Site` class object but does *not
instantiate* it.  You can import this module into a :term:`Django settings
module`, but you cannot use it directly as a settings module.  The following
attempt can only fail:

>>> from lino import startup
>>> startup('lino_voga.lib.voga.settings')
>>> from lino.api.rt import *
Traceback (most recent call last):
...
AttributeError: 'Settings' object has no attribute 'SITE'


In your :class:`Site` class you define some general description of your
application.

.. class:: Site
  :noindex:

  .. attribute:: title

    The title to appear in the browser window.  If this is None, Lino will use
    :attr:`verbose_name` as default value.

  .. attribute:: verbose_name

    The name of this application, to be displayed to end users at different
    places.

    Note the difference between :attr:`title` and :attr:`verbose_name`:

    - :attr:`title` may be None, :attr:`verbose_name` not.

    - :attr:`title` is used by the
      :srcref:`index.html <lino/modlib/extjs/config/extjs/index.html>` for
      :mod:`lino.modlib.extjs`.

    - :attr:`title` and :attr:`verbose_name` are used by
      :xfile:`admin_main.html` to generate the fragments "Welcome to the
      **title** site" and "We are running **verbose_name** version
      **x.y**"  (the latter only if :attr:`version` is set).

    - :meth:`site_version` uses :attr:`verbose_name` (not :attr:`title`)

    IOW, the :attr:`title` is rather for usage by a :term:`site maintainer`,
    while the :attr:`verbose_name` is rather for usage by the :term:`application
    developer`.

  .. attribute:: version

    An optional version number.


  .. attribute:: url

    The URL of the website that describes this application.
    Used e.g. in a :menuselection:`Site --> About` dialog box.

  .. method:: site_version(self)

      Used in footnote or header of certain printed documents.

  .. method:: welcome_text(self)

      Returns the text to display in a console window when this
      application starts.

  .. method:: using_text(self)

     Text to display in a console window when Lino starts.


How Lino builds the :setting:`INSTALLED_APPS` setting
=====================================================

A :term:`Lino application` is usually meant to install a given set of Django
"apps" (i.e. what's in the :setting:`INSTALLED_APPS` setting).
An application is a collection of plugins that make up a whole.
To define this collection, the :term:`application developer` usually overrides the
:meth:`Site.get_installed_apps` method.

Lino calls this method once at startup, and it expects it to yield a list of
strings.  Lino then adds some more "system" plugins and stores the resulting
list into your :setting:`INSTALLED_APPS` setting.


Additional local plugins
========================

An optional second positional argument can be specified by the  :term:`site
maintainer` in order to specify additional *local plugins*. These will go into
the :setting:`INSTALLED_APPS` setting, together with any other plugins needed by
them.

>>> from lino_book.projects.min1.settings import Site
>>> pseudoglobals = {}
>>> Site(pseudoglobals, "lino_xl.lib.events")  #doctest: +ELLIPSIS
<lino_book.projects.min1.settings.Site object at ...>
>>> print('\n'.join(pseudoglobals['INSTALLED_APPS']))
... #doctest: +REPORT_UDIFF +NORMALIZE_WHITESPACE
lino
django.contrib.staticfiles
lino.modlib.about
lino.modlib.jinja
lino.modlib.bootstrap3
lino.modlib.extjs
lino.modlib.printing
lino.modlib.system
lino.modlib.users
lino.modlib.office
lino_xl.lib.xl
lino_xl.lib.countries
lino_xl.lib.contacts
lino_xl.lib.events
django.contrib.sessions

As an :term:`application developer` you won't specify this argument, you should
specify your installed plugins by overriding :meth:`get_installed_apps
<lino.core.site.Site.get_installed_apps>`.

.. class:: Site

  :noindex:

  .. method:: get_installed_apps(self)

      Yield the list of apps to be installed on this site.

      Each item must be either a string or a *generator* to be iterated
      recursively (again expecting either strings or generators of strings).

      Lino will call this method exactly once when the :class:`Site`
      instantiates.  The resulting list of names will then possibly
      altered by the :meth:`get_apps_modifiers` method before being
      assigned to the :setting:`INSTALLED_APPS` setting.


  .. method:: get_plugin_configs(self)

      Return a series of plugin configuration settings.

      This is called before plugins are loaded.  :attr:`rt.plugins` is not
      yet populated.

      The method must return an iterator that yields tuples with three items
      each: The name of the plugin, the name of the setting and the
      value to set.

      Example::

        def get_plugin_configs(self):
            yield super(Site, self).get_plugin_configs()
            yield ('countries', 'hide_region', True)
            yield ('countries', 'country_code', 'BE')
            yield ('vat', 'declaration_plugin', 'lino_xl.lib.bevats')
            yield ('ledger', 'use_pcmn', True)
            yield ('ledger', 'start_year', 2014)


  .. method:: get_apps_modifiers(self, **kwargs)

      Override or hide individual plugins of the application.

      Deprecated because this approach increases complexity instead of
      simplifying things.

      For example, if your site inherits from
      :mod:`lino.projects.min2`::

        def get_apps_modifiers(self, **kw):
            kw = super(Site, self).get_apps_modifiers(**kw)
            kw.update(sales=None)
            kw.update(courses='my.modlib.courses')
            return kw

      The default implementation returns an empty dict.

      This method adds an additional level of customization because
      it lets you remove or replace individual plugins from
      :setting:`INSTALLED_APPS` without rewriting your own
      :meth:`get_installed_apps`.

      This will be called during Site instantiation and is expected to
      return a dict of `app_label` to `full_python_path`
      mappings which you want to override in the list of plugins
      returned by :meth:`get_installed_apps`.

      Mapping an `app_label` to `None` will remove that plugin from
      :setting:`INSTALLED_APPS`.

      It is theoretically possible but not recommended to replace an
      existing `app_label` by an app with a different
      `app_label`. For example, the following might work but is not
      recommended::

         kw.update(courses='my.modlib.MyActivities')
