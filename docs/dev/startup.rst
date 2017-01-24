.. _startup:

=================================
When a Lino application starts up
=================================

This chapter describes what happens during the startup of a Lino
process.

There are three major phases in the startup of a Lino process:

- **Application definition** (:mod:`lino.api.ad`) while Django
  **settings** are being loaded
  
- **Database definition** (:mod:`lino.api.dd`) while Django **models** are
  being loaded
  
- **Runtime** (:mod:`lino.api.rt`) when startup has finished.


A more detailed description follows.
  
- The `manage.py` script causes the module specified by
  :envvar:`DJANGO_SETTINGS_MODULE` (your :xfile:`settings.py` module) to be
  imported. This might happen twice (e.g. with :manage:`runserver`).
  Everything in :mod:`lino.api.ad` is usable.  

- Importing the :xfile:`settings.py` module will instantiate your
  :setting:`SITE`.

- When settings are ready, Django will load the :xfile:`models.py`
  modules.  Everything in :mod:`lino.api.dd` is usable during this
  step.

- When all models are loaded, the Site will "start up" and instantiate
  the **kernel**. Only now everything in :mod:`lino.api.rt` is usable.
  
  
**The remaining part of this section is obsolete.** It was for Django
before 1.7.


  


A server startup signal for Django
==================================

Lino provides a solution for Django's old problem of not having an
"application server startup signal", a signal to be emitted when the
models cache has been populated.

About the problem
-----------------

The problem is old:

- In March 2010, wojteks suggested to call it "server_initialized"
  in his :djangoticket:`13024` ("Signal sent on application startup").
  This ticket has been closed because it was 
  "fixed in a branch which needs review. See #3591."

- :djangoticket:`3591` ("add support for custom app_label and verbose_name") 
  seems truly very interesting and truly very complex,
  but didn't get into 1.5.
  Obviously it's not easy to find a good solution.

Note that this is *not* the same problem as
in `Entry point hook for Django projects
<http://eldarion.com/blog/2013/02/14/entry-point-hook-django-projects/>`__
(2013-02-14) where 
Brian Rosner 
describes a method for "running code when Django starts".
We don't want to run code *when* Django starts, 
but *after* Django has finished to start.
The difference is important e.g. if you want to analyze all installed models.


How Lino solves it
------------------

The basic trick is to simply send the signal "at the end of your last
app's models.py file" as described by `Ross McFarland on Sun 24 June
2012 <http://www.xormedia.com/django-startup-signal/>`_.

That's why :mod:`lino`  must be the *last* item of your
:setting:`INSTALLED_APPS`.

.. currentmodule:: lino.core.site

Although :mod:`lino` doesn't have any model of its own, it
does have a `models` module which invokes
the :meth:`startup <Site.startup>` method.
The :meth:`startup <Site.startup>` method
then emits a :attr:`startup <djangosite.signals.startup>`
signal.

Result is that you can now write code like the following in any
`models` or `admin` module of your existing project::

  from djangosite.signals import startup, receiver
  
  @receiver(startup)
  def my_handler(sender,**kw):
      # code to run exactly once per process at startup
      print sender.welcome_text()
        
