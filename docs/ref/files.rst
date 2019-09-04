Files
=====

.. xfile:: media/cache/wsdl

  See :blogref:`20120508`.
  
.. xfile:: models.py

Every Django app usually has a file `models.py`.  See `How to write
reusable apps
<https://docs.djangoproject.com/en/2.2/intro/reusable-apps/>`_


.. xfile:: urls.py

See http://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-a-project

.. xfile:: manage.py

See http://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-a-project

.. xfile:: __init__.py

The Python language requires a file :xfile:`__init__.py` in each
directory that is to be considered as a package.  Read the `Packages
<https://docs.python.org/2/tutorial/modules.html#packages>`_ chapter
of the Python Tutorial for more.

The :xfile:`__init__.py` files of a Django app are often empty, but
with Lino these files can contain :class:`lino.core.plugin.Plugin` class
definitions.

.. xfile:: media

This is the directory where Lino expects certain subdirs.

.. xfile:: config

Lino has a concept of configuration directories that are a bit like 
Django's `templates` directories.
See :mod:`lino.utils.config`.

.. xfile:: .po

:xfile:`.po` files are gettext catalogs. 
They contain chunks of English text as they appear in Lino, 
together with their translation into a given language.
See :doc:`/dev/translate/index`.

.. xfile:: linolib.js
.. xfile:: lino.js

These are obsolete synonyms for :xfile:`linoweb.js`.


.. xfile:: .weasy.html

An input template used by :mod:`lino.modlib.weasyprint`. 

