.. doctest docs/dev/settings.rst

=============================
Lino and your Django settings
=============================

Content moved to :doc:`/admin/settings` and :doc:`/dev/site`.

Remaining content is obsolete.


.. _lino.site_module:


The LINO_SITE_MODULE
====================

Lino applications (unlike Django projects) have a hook for specifying
site-wide default values for their Django settings.
This concept is mostly useful on servers where many Lino sites are
running (as described in :ref:`lino.admin.site_module`).
Actually they are not system-wide but environment-wide.

.. envvar:: LINO_SITE_MODULE

Each time a Lino process starts (when a :class:`lino.core.site.Site`
gets instantiated), it checks whether an environment variable
:envvar:`LINO_SITE_MODULE` is exists.  And if it does, Lino expects it
to be the name of a Python module, will import that module and, if it
contains a function named ``setup_site``, will call that function,
passing it the `Site` instance as one and only positional parameter.

For example you can do::

  $ export LINO_SITE_MODULE=my_site_options

And then create a file named :xfile:`my_site_options.py` somewhere on
your :envvar:`PYTHONPATH` with the following content::

    def setup_site(self):
        self.update_settings(ADMINS=[("John", "john.doe@example.com")])
        self.update_settings(EMAIL_HOST="mail.provider.com")
        self.update_settings(DEBUG=True)
        self.update_settings(ALLOWED_HOSTS=['127.0.0.1'])
        self.use_java = False

By convention we recommend to name that file :xfile:`lino_local.py`
and to set :envvar:`LINO_SITE_MODULE` to ``lino_local``.


.. rubric:: Keep in mind

.. xfile:: lino_local.py

:xfile:`lino_local.py` is a file containing site-wide local settings,
i.e. local settings to be applied to all projects.

The file just defines *default* values, individual projects can still
decide to override them.

This file is usually in a directory :file:`/usr/local/src/lino/`.

Lino will use these settings only if that directory is in
:envvar:`PYTHON_PATH` and if the project defines an environment
variable :envvar:`LINO_SITE_MODULE` containing the string
``lino_local``.



.. rubric:: Historic note

.. xfile:: djangosite_local.py

The :xfile:`djangosite_local.py` file was used until 20160109 as a
hard-coded :envvar:`LINO_SITE_MODULE`. Which had the disadvantage that
it was not easy to disable it quickly.

On servers where this was used, when upgrading to a Lino version after
20160109, you should set :envvar:`LINO_SITE_MODULE` to the string
``djangosite_local`` in order to maintain the old behaviour::

  export LINO_SITE_MODULE=djangosite_local
