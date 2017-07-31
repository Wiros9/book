=============
What is Lino?
=============

Lino is a high-level framework for writing :doc:`desktop-like
<desktop>` :doc:`customized <customized>` database applications, based
on `Django <https://www.djangoproject.com/>`_ and `Sencha ExtJS
<http://www.sencha.com/products/extjs/>`_.

From the hoster's and system manager's point of view, Lino
applications are just Django projects.  The difference with plain
Django projects is that Lino applications have an **out-of-the box
user interface**.  More about this in :doc:`lino_and_django`.

Advantages: everything gets much easier: writing a prototype, changing
database structures and business logic, long-term maintenance,
documentation.  More in :doc:`why`.

Disadvantage: you are limited to applications that fit into this
out-of-the box user interface.  More in :doc:`limitations`.

Lino is written mainly in the `Python <https://www.python.org/>`_
programming language, but also contains Javascript code and
ocasionally uses Java.


Target users
============

Primary target users of Lino applications are agencies and companies
who need a customized database application "more than MS-Access for
cheaper than SAP".

Lino is designed to be used by professional developers who write and
maintain a customized database application, either for internal use by
themselves or their employer, or for internal use by their customer,
or for public use as a service to their customers.

The growing collection of :ref:`lino.projects` is meant to be used by
service providers who offer professional hosting of one of these
applications.


Target applications
===================

Typical Lino applications have a rather **complex database
structure**.  For example Lino Welfare has 155 models in 65 plugins.
Even Lino Noi (the smallest Lino application which is being used on a
production site) has 44 models in 32 plugins.

