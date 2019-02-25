============
Introduction
============

Lino applications are basically normal Django applications, but
instead of writing `Admin` classes for your Django models, you write
Tables.

A Table describes a set of tabular data independently of *user
interface* and *medium* (paper, screen, interactive or not), but with
all the meta-data information necessary for any front end to
produce a satisfying result on any medium.  This is the theory.

Your tables are subclasses of :class:`dd.Table`, and they must be
defined in your application's 'models' module because Lino 'discovers'
and instantiates them automatically at startup.

A Layout describes an entry form in a GUI-independent way.
Users see them as Tabs of a Detail window (whose main component is a 
`FormPanel <http://www.extjs.com/deploy/dev/examples/form/xml-form.html>`_)

Instead of having each application register its models to the admin site, 
you write a main menu for your site that uses your Reports. 
This is is currently done in a file :xfile:`lino_settings.py`, 
usually in the same directory as Django's :xfile:`settings.py`.
This approach is less pluggable than Admin-based applications, 
but enterprise solutions don't need to be plug and play.

