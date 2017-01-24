.. _book.specs.checkdata:

==========================
Checking for data problems
==========================

.. to test just this doc:

    $ python setup.py test -s tests.SpecsTests.test_checkdata

    >>> from lino import startup
    >>> startup('lino_book.projects.min2.settings.doctests')
    >>> from lino.api.doctest import *
    >>> from django.core.management import call_command


Data checkers
=============

In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility checkers` to see a table of all available
checkers.

.. 
    >>> show_menu_path(plausibility.Checkers)
    Explorer --> System --> Plausibility checkers
    
>>> rt.show(plausibility.Checkers)
================================= ==================================================
 value                             text
--------------------------------- --------------------------------------------------
 printing.CachedPrintableChecker   Check for missing target files
 countries.PlaceChecker            Check plausibility of geographical places.
 addresses.AddressOwnerChecker     Check for missing or non-primary address records
 mixins.DupableChecker             Check for missing phonetic words
 cal.EventGuestChecker             Events without participants
 cal.ConflictingEventsChecker      Check for conflicting events
 cal.ObsoleteEventTypeChecker      Obsolete event type of generated events
 cal.LongEventChecker              Too long-lasting events
================================= ==================================================
<BLANKLINE>


Showing all problems
====================

The demo database deliberately contains some data problems.
In the web interface you can select :menuselection:`Explorer -->
System --> Plausibility problems` to see them.

..
    >>> show_menu_path(plausibility.AllProblems)
    Explorer --> System --> Plausibility problems


>>> rt.show(plausibility.AllProblems)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================= ========================================================= ====================================================================== ==============================
 Responsible       Controlled by                                             Message                                                                Plausibility checker
----------------- --------------------------------------------------------- ---------------------------------------------------------------------- ------------------------------
 Robin Rood        *Calendar entry #30 All Souls' Day (31.10.2014)*          Event conflicts with 2 other events.                                   Check for conflicting events
 Romain Raffault   *Calendar entry #113 Petit-déjeuner (31.10.2014 09:40)*   Event conflicts with Calendar entry #30 All Souls' Day (31.10.2014).   Check for conflicting events
 Rando Roosi       *Calendar entry #137 Breakfast (31.10.2014 08:30)*        Event conflicts with Calendar entry #30 All Souls' Day (31.10.2014).   Check for conflicting events
================= ========================================================= ====================================================================== ==============================
<BLANKLINE>



Filtering data problems
=======================

The user can set the table parameters e.g. to see only problems of a
given type ("checker"). The following snippet simulates the situation
of selecting the :class:`ConflictingEventsChecker
<lino_xl.lib.cal.models.ConflictingEventsChecker>`.

>>> chk = plausibility.Checkers.get_by_value('cal.ConflictingEventsChecker')
>>> rt.show(plausibility.ProblemsByChecker, chk)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
================= ========================================================= ======================================================================
 Responsible       Controlled by                                             Message
----------------- --------------------------------------------------------- ----------------------------------------------------------------------
 Robin Rood        *Calendar entry #30 All Souls' Day (31.10.2014)*          Event conflicts with 2 other events.
 Romain Raffault   *Calendar entry #113 Petit-déjeuner (31.10.2014 09:40)*   Event conflicts with Calendar entry #30 All Souls' Day (31.10.2014).
 Rando Roosi       *Calendar entry #137 Breakfast (31.10.2014 08:30)*        Event conflicts with Calendar entry #30 All Souls' Day (31.10.2014).
================= ========================================================= ======================================================================
<BLANKLINE>



Running the :command:`checkdata` command
========================================


>>> call_command('checkdata')
Found 3 and fixed 0 data problems in Calendar entries.
Done 5 checkers, found 3 and fixed 0 problems.

You can see the list of all available checkers also from the command
line using::

    $ python manage.py checkdata --list

>>> call_command('checkdata', list=True)
================================= ==================================================
 value                             text
--------------------------------- --------------------------------------------------
 printing.CachedPrintableChecker   Check for missing target files
 countries.PlaceChecker            Check plausibility of geographical places.
 addresses.AddressOwnerChecker     Check for missing or non-primary address records
 mixins.DupableChecker             Check for missing phonetic words
 cal.EventGuestChecker             Events without participants
 cal.ConflictingEventsChecker      Check for conflicting events
 cal.ObsoleteEventTypeChecker      Obsolete event type of generated events
 cal.LongEventChecker              Too long-lasting events
================================= ==================================================
<BLANKLINE>


>>> call_command('checkdata', 'cal.')
Found 3 and fixed 0 data problems in Calendar entries.
Done 1 checkers, found 3 and fixed 0 problems.

>>> call_command('checkdata', 'foo')
Traceback (most recent call last):
...
Exception: No checker matches ('foo',)



