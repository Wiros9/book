.. doctest docs/specs/uploads.rst
.. _specs.uploads:

=====================================
``uploads`` : Managing uploaded files
=====================================

.. currentmodule:: lino.modlib.uploads

The :mod:`lino.modlib.uploads` plugin adds functionality for managing "uploads".
It holds the minimal core functionality.  There is also the
:mod:`lino_xl.lib.uploads` plugin, which extends this plugin and which is
described in :doc:`/specs/avanti/uploads`.

.. contents::
   :depth: 1
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.min9.settings.doctests')
>>> from lino.api.doctest import *


Overview
========

.. glossary::

  upload file

    A database record that represents an independent media file that has been
    uploaded to the :term:`Lino site` either via the web interface or as a
    library file.

We differentiate between **web uploads** and **library uploads**. They look
quite similar to the end user who may even ignore that difference. But they
differ by the way they arrived to the server. Web uploads were uploaded manually
by some user via the web interface, while *library uploads* have been discovered
by Lino in a :term:`library volume`. A third type of upload files are **fileless
uploads**. Yes, you can even have upload files without an actual file. This
represents the fact that some external document exists, but just hasn't been
digitalized. There are people are interested in this kind of fact ;-)

All :term:`upload files <upload file>` are stored in a single database table
called :class:`Upload`.

.. glossary::

  upload controller

    Any database object used as the controller of an :term:`upload file`.

Every :term:`upload file` is usually linked to its :term:`controller <upload
controller>`, i.e. some database object that inherits from
:class:`UploadController`. Upload files without a controller are considered
**useless**, and the :term:`site manager` should decide what to do with them.


.. glossary::

  library volume

    A folder in the file system where *library uploads* are stored.

The site manager can configure :term:`library volumes <library volume>` via the
menu command :menuselection:`Configure --> Uploads --> Library volumes`.  Lino
watches the files in the folder tree of a library volume and can automatically
create an :term:`upload file` for every new file.


Concepts
========

.. glossary::

  upload type

    The type of an upload file.

  upload area

    A group of upload types that are being displayed in a given upload panel.


Upload files
============

.. class:: Upload

    Django model representing an :term:`upload file`.

    .. attribute:: file

        Pointer to the uploaded file itself (a `Django FileField
        <https://docs.djangoproject.com/en/3.2/ref/models/fields/#filefield>`_).

    .. attribute:: file_size

        The size of the file in bytes. Not yet implemented.

    .. attribute:: mimetype

        The `media type <https://en.wikipedia.org/wiki/Media_type>`_ of the
        uploaded file.

        See also `this thread
        <http://stackoverflow.com/questions/643690/maximum-mimetype-length-when-storing-type-in-db>`_
        about length of MIME type field.

    .. attribute:: type

        The type of this upload.

        Pointer to :class:`UploadType`. The choices for this field are usually
        limited to those in the same *upload area*.

    .. attribute:: description

        A short description entered manually by the user.

    .. attribute:: volume

        A pointer to the :term:`library volume` where this file is stored.

    .. attribute:: upload_area

        The :term:`upload area` this file belongs to.

    .. attribute:: library_file

        The path of this file, relative the volume's root.

    .. attribute:: description_link

        Almost the same as :attr:`description`, but if :attr:`file` is
        not empty, the text is clickable, and clicking on it opens the
        uploaded file in a new browser window.


.. class:: AreaUploads

    Mixin for tables of uploads where the *area* is known. Inherited by
    :class:`UploadsByController`.

    The summary displays the uploads related to this controller as a list grouped
    by uploads type.

    Note that this also works on
    :class:`lino_welfare.modlib.uploads.models.UploadsByProject`
    and their subclasses for the different `_upload_area`.


.. class:: MyUploads

    Shows my uploads (i.e. those whose author is the current user).

.. class:: UploadsByController

    Shows the uploads controlled by this database object.


.. class:: UploadBase

    Abstract base class of :class:`Upload`.
    This was named :class:`lino.mixins.uploadable.Uploadable` until 20210217.
    It encapsulates some really basic
    functionality. Its usage is deprecated. If you were inheriting from
    :class:`lino.mixins.Uploadable`, you should convert that model to point to
    an :class:`Upload` instead.




Upload areas
============

The application developer can define **upload areas**.  Every upload area has
its list of upload types.  The default has only one upload area.

>>> rt.show(uploads.UploadAreas)
======= ========= =========
 value   name      text
------- --------- ---------
 90      general   Uploads
======= ========= =========
<BLANKLINE>

For example :ref:`welfare` extends this list.


Upload types
============

.. class:: UploadType

    Django model representing an :term:`upload type`.

    .. attribute:: shortcut

        Optional pointer to a virtual **upload shortcut** field.  If
        this is not empty, then the given shortcut field will manage
        uploads of this type.  See also :class:`Shortcuts`.

.. class:: UploadTypes

    The table with all existing upload types.

    This usually is accessible via the `Configure` menu.

Upload controllers
==================


.. class:: UploadController

    Model mixin that turns a model into an :term:`upload controller`.

    .. method:: show_uploads(self, obj, ar=None)

        Show uploads in a grid table.



Upload shortcuts
================

The application developer can define **upload shortcuts**.  Every upload
shortcut will create an **upload shortcut field**, a virtual field with a set
of actions for quickly uploading or viewing uploads of a particular type for a
given database object.

Usage:

- Declare your Site's upload shortcuts from within your
  :attr:`workflows_module
  <lino.core.site.Site.workflows_module>`. For example::

      from lino.modlib.uploads.choicelists import add_shortcut as add
      add('contacts.Person', 'uploaded_foos', _("Foos"))

- Make the ``uploaded_foos`` field visible in some detail layout.

- Using the web interface, select :menuselection:`Configure --> Office
  --> Upload types`, create an upload type named "Foo" and set its
  `shortcut` field to "Foos".

- Upload a file from your PC to the server.
- Open the uploaded file in a new browser window


.. class:: Shortcuts

    The list of available upload shortcut fields in this application.

>>> rt.show(uploads.Shortcuts)
No data to display


.. function:: add_shortcut(*args, **kw)

    Declare an upload shortcut field. This is designed to be called from within
    your :attr:`workflows_module <lino.core.site.Site.workflows_module>`.
