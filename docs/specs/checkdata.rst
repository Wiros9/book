.. doctest docs/specs/checkdata.rst
.. _book.specs.checkdata:

==========================================
``checkdata`` : High-level integrity tests
==========================================

.. currentmodule:: lino.modlib.checkdata

The :mod:`lino.modlib.checkdata` plugin adds support for defining
application-level data integrity tests.
For the :term:`application developer` it provides a method to define :term:`data
checkers <data checker>` for their models.
For the :term:`site maintainer` it
adds the :manage:`checkdata` :term:`django-admin command`.
For the :term:`end user` it adds a set of `automatic actions`_.

.. contents::
   :depth: 1
   :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.roger.settings.demo')
>>> from lino.api.doctest import *
>>> from django.core.management import call_command
>>> from atelier.sheller import Sheller
>>> shell = Sheller(settings.SITE.project_dir.parent)

Overview
========

This plugin provides a framework for managing and handling :term:`data problems
<data problem>`.

.. glossary::

  data problem

    A problem in the database that cannot be detected by the DBMS because
    finding it requires business intelligence.

    Some data problems can be fixed automatically, others need human interaction.

The application developer defines the rules for detecting data problems by
writing :term:`data checkers <data checker>`.

.. glossary::

  data checker

    A piece of code that tests for :term:`data problems <data problem>`.

  unbound data checker

    Data checkers are usually attached to a given database model. If they are
    not attached to a model, they are called **unbound**.  :term:`Data problems
    <data problem>` reported by an unbound data checker have an empty
    :attr:`owner <Problem.owner>` field.

Lino has different ways to run these checkers.  When a data checker finds a
problem, Lino creates a :term:`problem message`.

.. glossary::

  problem message

    A message that describes one or several :term:`data problems <data problem>`
    detected in a given database object.

Problem messages are themselves database objects, but considered temporary
data and may be updated automatically without user confirmation.

Each :term:`problem message` is assigned to a *responsible user*. This user can
see their problems in the :class:`MyProblems` table, which generates a welcome
message if it contains data.

The application developer can decide to add a :class:`ProblemsByOwner` table to
the :term:`detail layout` of any model.  This enables the end users to focus on
the data problems related to a given database object.


Data checkers
=============

In the web interface you can select :menuselection:`Explorer --> System --> Data
checkers` to see a table of all available checkers.

..
    >>> show_menu_path(checkdata.Checkers, language="en")
    Explorer --> System --> Data checkers

>>> rt.show(checkdata.Checkers, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=================================== ========================================================
 value                               text
----------------------------------- --------------------------------------------------------
 beid.SSINChecker                    Check for invalid SSINs
 cal.ConflictingEventsChecker        Check for conflicting calendar entries
 cal.EventGuestChecker               Entries without participants
 cal.LongEntryChecker                Too long-lasting calendar entries
 cal.ObsoleteEventTypeChecker        Obsolete generated calendar entries
 countries.PlaceChecker              Check data of geographical places.
 courses.MemberChecker               Check membership payments
 finan.FinancialVoucherItemChecker   Check for invalid account/partner combination
 ledger.VoucherChecker               Check integrity of ledger vouchers
 memo.PreviewableChecker             Check for previewables needing update
 phones.ContactDetailsOwnerChecker   Check for mismatches between contact details and owner
 printing.CachedPrintableChecker     Check for missing target files
 sepa.BankAccountChecker             Check for partner mismatches in bank accounts
 system.BleachChecker                Find unbleached html content
 uploads.UploadChecker               Check metadata of upload files
 uploads.UploadsFolderChecker        Find orphaned files in uploads folder
 vat.VatColumnsChecker               Check VAT columns configuration.
=================================== ========================================================
<BLANKLINE>


The :class:`lino_xl.lib.countries.PlaceChecker` class is a simple example of how
to write a data checker::

  from lino.api import _
  from lino.modlib.checkdata.choicelists import Checker

  class PlaceChecker(Checker):
      model = 'countries.Place'
      verbose_name = _("Check data of geographical places.")

      def get_checkdata_problems(self, obj, fix=False):
          if obj.name.isdigit():
              yield (False, _("Name contains only digits."))

  PlaceChecker.activate()

..
  >>> print(rt.models.countries.PlaceChecker.verbose_name)
  Check data of geographical places.


More examples of data checkers we recommend to explore:

- :class:`lino_xl.lib.countries.PlaceChecker`
- :class:`lino_xl.lib.beid.mixins.BeIdCardHolderChecker`
- :class:`lino_xl.lib.addresses.AddressOwnerChecker`
- :class:`lino.mixins.dupable.DupableChecker`
- :class:`lino.modlib.uploads.UploadChecker`
- :class:`lino.modlib.uploads.UploadsFolderChecker`
- :class:`lino_welfare.modlib.pcsw.models.SSINChecker`
- :class:`lino_welfare.modlib.pcsw.models.ClientCoachingsChecker`
- :class:`lino_welfare.modlib.isip.mixins.OverlappingContractsChecker`
- :class:`lino_welfare.modlib.dupable_clients.models.SimilarClientsChecker`



Showing all data problems
=========================

In the web interface you can select :menuselection:`Explorer -->
System --> Data problems` to see all problems.

..
    >>> show_menu_path(checkdata.AllProblems, language="en")
    Explorer --> System --> Data problems

The demo database deliberately contains some data problems.

>>> rt.show(checkdata.AllProblems, language="en")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============= =========================================== ============================================================== ========================================
 Responsible   Database object                             Message                                                        Checker
------------- ------------------------------------------- -------------------------------------------------------------- ----------------------------------------
 Robin Rood                                                File uploads/2015/05/foo.pdf has no upload entry.              Find orphaned files in uploads folder
 Robin Rood    *Recurring event #4 Assumption of Mary*     Event conflicts with Activity #1 001  1.                       Check for conflicting calendar entries
 Robin Rood    *Recurring event #11 Ascension of Jesus*    Event conflicts with Mittagessen (14.05.2015 11:10).           Check for conflicting calendar entries
 Robin Rood    *Recurring event #12 Pentecost*             Event conflicts with 4 other events.                           Check for conflicting calendar entries
 Rolf Rompen   *Mittagessen (14.05.2015 11:10)*            Event conflicts with Recurring event #11 Ascension of Jesus.   Check for conflicting calendar entries
 Robin Rood    *First meeting (25.05.2015 13:30)*          Event conflicts with Recurring event #12 Pentecost.            Check for conflicting calendar entries
 Robin Rood    *Absent for private reasons (25.05.2015)*   Event conflicts with Recurring event #12 Pentecost.            Check for conflicting calendar entries
 Robin Rood    *Karl Kaivers (ME)*                         Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Laura Laschet (ME)*                        Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Josefine Leffin (MEL)*                     Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Marie-Louise Meier (ME)*                   Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Alfons Radermacher (ME)*                   Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Christian Radermacher (MEL)*               Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Edgard Radermacher (ME)*                   Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Guido Radermacher (ME)*                    Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Hedi Radermacher (ME)*                     Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Jean Radermacher (ME)*                     Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Erna Ärgerlich (ME)*                       Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Jean Dupont (ME)*                          Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Marie-Louise Vandenmeulenbos (MEC)*        Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Bernd Brecht (ME)*                         Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Jérôme Jeanémart (ME)*                     Member until 2015-12-31, but no payment.                       Check membership payments
 Robin Rood    *Source document PRC_29_2015.pdf*           Upload entry uploads/2015/05/PRC_29_2015.pdf has no file       Check metadata of upload files
============= =========================================== ============================================================== ========================================
<BLANKLINE>


Filtering data problem messages
===============================

The user can set the table parameters e.g. to see only messages of a given type
("checker"). The following snippet simulates the situation of selecting the
:class:`ConflictingEventsChecker <lino_xl.lib.cal.ConflictingEventsChecker>`.

>>> chk = checkdata.Checkers.get_by_value('cal.ConflictingEventsChecker')
>>> rt.show(checkdata.ProblemsByChecker, chk)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============= =========================================== ==============================================================
 Responsible   Database object                             Message
------------- ------------------------------------------- --------------------------------------------------------------
 Robin Rood    *Recurring event #4 Assumption of Mary*     Event conflicts with Activity #1 001  1.
 Robin Rood    *Recurring event #11 Ascension of Jesus*    Event conflicts with Mittagessen (14.05.2015 11:10).
 Robin Rood    *Recurring event #12 Pentecost*             Event conflicts with 4 other events.
 Rolf Rompen   *Mittagessen (14.05.2015 11:10)*            Event conflicts with Recurring event #11 Ascension of Jesus.
 Robin Rood    *First meeting (25.05.2015 13:30)*          Event conflicts with Recurring event #12 Pentecost.
 Robin Rood    *Absent for private reasons (25.05.2015)*   Event conflicts with Recurring event #12 Pentecost.
============= =========================================== ==============================================================
<BLANKLINE>


See also :doc:`cal` and :doc:`holidays`.

Running the :command:`checkdata` command
========================================


>>> call_command('checkdata')
Found 6 and fixed 0 data problems in Calendar entries.
Found 15 and fixed 0 data problems in Participants.
Found 1 and fixed 0 data problems in Upload files.
Found 1 and fixed 0 data problems in unbound data.
Done 33 checks, found 23 and fixed 0 problems.


You can see the list of all available checkers also from the command
line using::

    $ python manage.py checkdata --list

>>> call_command('checkdata', list=True)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=================================== ========================================================
 value                               text
----------------------------------- --------------------------------------------------------
 beid.SSINChecker                    Check for invalid SSINs
 cal.ConflictingEventsChecker        Check for conflicting calendar entries
 cal.EventGuestChecker               Entries without participants
 cal.LongEntryChecker                Too long-lasting calendar entries
 cal.ObsoleteEventTypeChecker        Obsolete generated calendar entries
 countries.PlaceChecker              Check data of geographical places.
 courses.MemberChecker               Check membership payments
 finan.FinancialVoucherItemChecker   Check for invalid account/partner combination
 ledger.VoucherChecker               Check integrity of ledger vouchers
 memo.PreviewableChecker             Check for previewables needing update
 phones.ContactDetailsOwnerChecker   Check for mismatches between contact details and owner
 printing.CachedPrintableChecker     Check for missing target files
 sepa.BankAccountChecker             Check for partner mismatches in bank accounts
 system.BleachChecker                Find unbleached html content
 uploads.UploadChecker               Check metadata of upload files
 uploads.UploadsFolderChecker        Find orphaned files in uploads folder
 vat.VatColumnsChecker               Check VAT columns configuration.
=================================== ========================================================
<BLANKLINE>


>>> call_command('checkdata', 'cal.')
Found 6 and fixed 0 data problems in Calendar entries.
Done 1 check, found 6 and fixed 0 problems.

>>> call_command('checkdata', 'foo')
Traceback (most recent call last):
...
Exception: No checker matches ('foo',)

The ``--prune`` option instructs checkdata to remove all existing error messages
before running the tests.  This makes the operation quicker on sites with many
existing data problem messages. Don't use this in combination with a filter
because `--prune` removes *all* messages, not only those that you ask to
rebuild.

>>> shell("python manage.py checkdata --prune")
Prune 23 existing messages...
Found 6 and fixed 0 data problems in Calendar entries.
Found 15 and fixed 0 data problems in Participants.
Found 1 and fixed 0 data problems in Upload files.
Found 1 and fixed 0 data problems in unbound data.
Done 33 checks, found 23 and fixed 0 problems.

NB the above example uses :mod:`atelier.sheller` instead of :mod:`call_command
<django.core.management.call_command>`.  Both methods are functionally
equivalent.


Language of checkdata messages
==============================

Every detected checkdata problem is stored in the database in the language of
the responsible user. A possible pitfall with this is the following example.

The checkdata message "Similar clients" appeared in English and not in the
language of the responsible user. That was because the checker did this::

  msg = _("Similar clients: {clients}").format(
      clients=', '.join([str(i) for i in lst]))
  yield (False, msg)

The correct way is like this::

  msg = format_lazy(_("Similar clients: {clients}"),
      clients=', '.join([str(i) for i in lst]))
  yield (False, msg)

See :doc:`/dev/i18n` for details.

Database models
===============

.. class:: Problem

  Django model used to store a :term:`problem message`.

  .. attribute:: checker

     The :class:`Checker <lino.modlib.checkdata.Checker>` that reported this
     problem.

  .. attribute:: message

     The message text. This is a concatenation of all messages that
     were yielded by the :attr:`checker`.

  .. attribute:: user

     The :class:`user <lino.modlib.users.User>` responsible for fixing this
     problem.

     This field is being filled by the :meth:`get_responsible_user
     <lino.modlib.checkdata.Checker.get_responsible_user>`
     method of the :attr:`checker`.


.. class:: Problems

    The base table for :term:`problem messages <problem message>`.

.. class:: MyProblems

    Shows the :term:`problem messages <problem message>` assigned to me.


.. class:: Checkers

    The list of data checkers known by this application.

    This was the first use case of a :class:`ChoiceList
    <lino.core.choicelists.ChoiceList>` with a :attr:`detail_layout
    <lino.core.actors.Actor.detail_layout>`.


.. class:: Checker

  Base class for all :term:`data checkers <data checker>`.

  .. attribute:: model

    The model to be checked.  If this is a string, Lino will resolve it at startup.

    If this is an abstract model, :meth:`get_checkable_models` will
    yield all models that inherit from it.

    If this is `None`, the checker is unbound, i.e. the problem messages will
    not be bound to a particular database object.  This is used to detect
    *missing* database objects.   For example :class:`vat.VatColumnsChecker
    <lino_xl.lib.vat.VatColumnsChecker>` is unbound.

    Instead of setting :attr:`model` you might want to define your own
    :meth:`get_checkable_models` method. For example,
    :class:`ledger.VoucherChecker <lino_xl.lib.ledger.VoucherChecker>` does this
    because it wants to get all MTI children (not only top-level models).
    See :ref:`tested.core_utils` for more explanations.


  .. classmethod:: check_instance(cls, *args, **kwargs)

    Run :meth:`get_checkdata_problems` on this checker for the given database
    object.

  .. method:: get_checkable_models(self)

    Return a list of the models to check.

    The default implementation returns all top-level models that inherit from
    :attr:`model` (or `[None]` when :attr:`model` is `None`).

  .. classmethod:: activate(cls)

    Creates an instance of this class and adds it as a choice to the
    :class:`Checkers` choicelist.

    The :term:`application developer` must call this on their subclass in order
    to "register" or "activate" the checker.

  .. method:: update_problems(self, obj=None, delete=True, fix=False)

    Update the :term:`problem messages <problem message>` of this checker for
    the specified object.

    ``obj`` is `None` on unbound checkers.

    When `delete` is False, the caller is responsible for deleting any existing
    objects.

  .. method:: get_checkdata_problems(self, obj, fix=False)

    Return or yield a series of `(fixable, message)` tuples, each describing a
    data problem. `fixable` is a boolean saying whether this problem can be
    automatically fixed. And if `fix` is `True`, this method is also responsible
    for fixing it.

  .. method:: get_responsible_user(self, obj)

    The site user to be considered responsible for problems detected by this
    checker on the given database object `obj`. This will be stored in
    :attr:`user <lino.modlib.checkdata.Problem.user>`.

    The given `obj` is an instance of :attr:`model`, unless for unbound
    checkers (i.e. whose :attr:`model` is `None`).

    The default implementation returns the *main checkdata
    responsible* defined for this site (see
    :attr:`responsible_user
    <lino.modlib.checkdata.Plugin.responsible_user>`).



Automatic actions
=================

This plugin automatically installs two actions on every model for which there is
at least one active :term:`data checker`:

.. currentmodule:: lino.core.model


.. class:: Model
  :noindex:

  .. attribute:: fix_problems

    Update data problem messages and repair those which are automatically fixable.

    Implementing class: :class:`lino.modlib.checkdata.FixProblemsByController`.

  .. attribute:: check_data

    Update data problem messages for this database object,
    also removing messages that no longer exist.
    This action does not change anything else in the database.

    Implementing class: :class:`lino.modlib.checkdata.UpdateProblemsByController`.

.. currentmodule:: lino.modlib.checkdata

Internal utilities
==================

.. function:: get_checkable_models(*args)

    Return an `OrderedDict` mapping each model which has at least one
    checker to a list of these checkers.

    The dict is ordered to avoid that checkers run in a random order.
