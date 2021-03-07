.. doctest docs/dev/actors.rst
.. _dev.actors:

======================
Introduction to actors
======================

*Tables* and *choicelists* have certain things in common.  When we
refer to them in general, then we call them :term:`actors <actor>`.

.. contents::
   :depth: 1
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.noi1e.settings.demo')
>>> from lino.api.doctest import *

Actor types
===========

The most common type of actors :term:`table actors <table actor>`.

But not all actors are tables. Another type of actors are *frames*, display some
data in some other form.   One such frame actor is the calendar panel, another
one is :class:`lino.utils.report.EmptyTable`, used to display reports.


.. glossary::

  table actor

    An actor that operates on a list of "rows".

    We happen to simply refer to a table actor as "table", but of course we
    must not mix them up with :term:`database table`.

  database actor

    A :term:`table actor` that is connected to a :term:`database table`.


Identifying actors
==================

Actors are identified by their `app_label.ClassName`. Similar to Django's models
they are globally known unique class objects.

Lino collects actors during :term:`site startup` in a way similar to how Django
collects models.  Every subclass of :class:`lino.core.actors.Actor` that is
defined somewhere in your code, will be "registered" into the global models
namespace :data:`rt.models`.

It makes no difference wheter you import them or access them via
:data:`rt.models`.

>>> from lino_xl.lib.working.ui import WorkedHours
>>> rt.models.working.WorkedHours is WorkedHours
True

The advantage of accessing them via :data:`rt.models` is that your code is open
to extensions.

Actors are never instantiated, we use only the class objects.

>>> str(WorkedHours)
'working.WorkedHours'

>>> repr(WorkedHours)
'lino_xl.lib.working.ui.WorkedHours'


Getting a list of all actors
============================

When Lino starts up, it automatically discovers the installed plugins
and registers each subclass of :class:`Actor` as an actor.

>>> len(actors.actors_list)
350

Some of the actors are abstract, i.e. they are used as base classes for other
actors:

>>> len([a for a in actors.actors_list if a.abstract])
32

The actors aren't collected only in this global list but also at different
places depending on their type.

The most common actors are **database tables**. HEre we differentiate between
"master tables", "slave tables" and "generic slave tables":

>>> from lino.core import kernel
>>> len(kernel.master_tables)
153
>>> kernel.master_tables[0]
lino.modlib.system.models.SiteConfigs

>>> len(kernel.slave_tables)
77
>>> kernel.slave_tables[0]
lino_xl.lib.countries.models.PlacesByPlace

>>> list(sorted(kernel.generic_slaves.values(), key=str))
[lino_xl.lib.cal.ui.EntriesByController, lino_xl.lib.cal.ui.TasksByController, lino.modlib.changes.models.ChangesByMaster, lino.modlib.changes.models.ChangesByObject, lino.modlib.checkdata.models.ProblemsByOwner, lino.modlib.comments.ui.CommentsByRFC, lino.modlib.comments.ui.MentionsByOwner, lino_xl.lib.excerpts.models.ExcerptsByOwner, lino.modlib.gfks.models.HelpTextsByModel, lino_xl.lib.invoicing.models.InvoicingsByGenerator, lino.modlib.uploads.models.UploadsByController]

>>> for a in kernel.generic_slaves.values():
...    assert a not in kernel.slave_tables
...    assert a in actors.actors_list


Another category are :term:`virtual tables <virtual table>`.
For example
:class:`lino.modlib.users.UserRoles`
:class:`lino_xl.lib.working.WorkedHours`
:class:`lino.modlib.gfks.BrokenGFKs`
:class:`lino.modlib.gfks.BrokenGFKs`

>>> kernel.virtual_tables  #doctest: +NORMALIZE_WHITESPACE
[lino.modlib.about.models.SiteSearch, lino.modlib.gfks.models.BrokenGFKs,
lino.modlib.gfks.models.BrokenGFKsByModel, lino_xl.lib.calview.ui.MonthlySlave,
lino_xl.lib.calview.ui.DailyView, lino_xl.lib.calview.ui.WeeklyView,
lino_xl.lib.calview.ui.MonthlyView, lino_xl.lib.working.ui.WorkedHours,
lino_xl.lib.ledger.ui.ExpectedMovements, lino_xl.lib.ledger.ui.DebtsByAccount,
lino_xl.lib.ledger.ui.DebtsByPartner, lino_xl.lib.ledger.ui.Debtors,
lino_xl.lib.ledger.ui.Creditors, lino.modlib.users.desktop.UserRoles,
lino_xl.lib.vat.desktop.VouchersByPartner]




Another category are choicelists

>>> len(kernel.CHOICELISTS)
54
>>> list(sorted(kernel.CHOICELISTS.items()))[6]
('cal.GuestStates', lino_xl.lib.cal.choicelists.GuestStates)

>>> for a in kernel.CHOICELISTS.values():
...    if a not in actors.actors_list:
...        print(a)


And a last category are what we call "frames":

>>> kernel.frames_list
[lino.modlib.about.models.About, lino_xl.lib.ledger.ui.Situation]
