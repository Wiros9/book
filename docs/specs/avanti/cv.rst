.. doctest docs/specs/avanti/cv.rst
.. _avanti.specs.cv:

=================================
CV functions in Lino Avanti
=================================

This document describes how standard CV functionality is being extended by
:ref:`avanti`.


.. contents::
  :local:


.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_book.projects.avanti1.settings.doctests')
>>> from lino.api.doctest import *


Lino Avanti defines a plugin :mod:`lino_avanti.lib.cv`  which inherits from
:mod:`lino_xl.lib.cv`.


.. currentmodule:: lino_avanti.lib.cv

.. class:: Study

    .. attribute::

        Why the pupil was absent.  Choices for this field are defined
        in :class:`AbsenceReasons`.

Calendar workflow
=================

It's almost like :mod:`lino_xl.lib.cal.workflows.voga`, except that we removed
the transition (...).

In existing data (until June 2018) we differentiate between "excused" and
"absent".  In August 2018 we decided to no longer do this differentiation.

>>> rt.show(cal.GuestStates)
======= ========= ============ ========= =============
 value   name      Afterwards   text      Button text
------- --------- ------------ --------- -------------
 10      invited   No           Invited   ?
 40      present   Yes          Present   ☑
 50      missing   Yes          Missing   ☉
 60      excused   No           Excused   ⚕
======= ========= ============ ========= =============
<BLANKLINE>

In Avanti there is a presence state "excused", but there is no workflow
transition for it, so it is rather invisible for the end users.

>>> show_workflow(cal.GuestStates.workflow_actions)
============= ============== =========== ============== =========================
 Action name   Verbose name   Help text   Target state   Required states
------------- -------------- ----------- -------------- -------------------------
 wf1           ☑              Present     Present        invited
 wf2           ☉              Missing     Missing        invited
 wf3           ?              Invited     Invited        missing present excused
============= ============== =========== ============== =========================


>>> rt.show(cal.EntryStates)
======= ============ ============ ============= ============= ======== ============= =========
 value   name         text         Button text   Fill guests   Stable   Transparent   No auto
------- ------------ ------------ ------------- ------------- -------- ------------- ---------
 10      suggested    Suggested    ?             Yes           No       No            No
 20      draft        Draft        ☐             Yes           No       No            No
 50      took_place   Took place   ☑             No            Yes      No            No
 70      cancelled    Cancelled    ☒             No            Yes      Yes           Yes
======= ============ ============ ============= ============= ======== ============= =========
<BLANKLINE>


>>> show_workflow(cal.EntryStates.workflow_actions)
============= ============== ============ ============== ================================
 Action name   Verbose name   Help text    Target state   Required states
------------- -------------- ------------ -------------- --------------------------------
 reset_event   Reset          Suggested    Suggested      suggested took_place cancelled
 wf2           ☐              Draft        Draft          suggested cancelled took_place
 wf3           Took place     Took place   Took place     suggested draft cancelled
 wf4           ☒              Cancelled    Cancelled      suggested draft took_place
============= ============== ============ ============== ================================


>>> base = '/choices/cal/Guests/partner'
>>> show_choices("rolf", base + '?query=') #doctest: +ELLIPSIS
<br/>
ABAD Aábdeen (114/nathalie)
ABBASI Aáishá (118/romain)
ABDALLA Aádil (120/rolf)
ABDALLAH Aáish (127/robin)
ABDELLA Aákif (128/nathalie)
ABDI Aátifá (136/rolf)
ABDO Aásim (138/robin)
ABDUL Abbáád (171/romain)
ABDULLA Abbáás (152/rolf)
ABID Abdul Báásid (162/romain)
ABOOD Abdul Fáttááh (163/rolf)
ALEKSANDROV Akim (116/nathalie)
ARNOLD Alexei (129/nathalie)
ARSHAN Afimiá (132/nelly)
ASTAFUROV Agáfiiá (175/robin)
BA Abá (113/nathalie)
BARDZECKI Agáfiyá (144/rolf)
BASKOV Anstice (156/nelly)
BEK-MURZIN Agápiiá (160/romain)
BERNDT Armán (167/nathalie)
CONGO Chiámáká (126/rolf)
CONTEE Chike (131/robin)
DEMEULENAERE Dorothée (121/nelly)
DIALLO Deiondre (140/rolf)
DIOP Ashánti (142/robin)
DOBBELSTEIN-DEMEULENAERE Dorothée (122/nathalie)
GUEYE Dewáyne (154/rolf)
JALLOH Diállo (158/robin)
MAALOUF Cátává (168/romain)


>>> show_choices("audrey", base + '?query=') #doctest: +ELLIPSIS
<br/>
(114) from Eupen
(118) from Eupen
(120) from Eupen
(127) from Eupen
(128) from Eupen
(136) from Eupen
...



:class:`GuestsByPartner` shows all presences except those in more than
one week and sorts them chronologically:

>>> obj = avanti.Client.objects.get(pk=115)
>>> rt.show(cal.GuestsByPartner, obj) #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
January 2017: *Mon 16.*☑ *Tue 17.*☑ *Thu 19.*☑ *Fri 20.*☑ *Mon 23.*☑ *Tue 24.*☑ *Thu 26.*☒ *Fri 27.*☑ *Mon 30.*☑ *Tue 31.*☑
February 2017: *Thu 02.*☑ *Fri 03.*☑ *Mon 06.*☑ *Tue 07.*☑ *Thu 09.*? *Fri 10.*? *Mon 13.*? *Tue 14.*? *Thu 16.*? *Fri 17.*? *Mon 20.*? *Tue 21.*?
Suggested : 8 ,  Draft : 0 ,  Took place : 13 ,  Cancelled : 1


Absence reasons
===============

In :ref:`avanti` we record and analyze why pupils have been missing.

.. class:: AbsenceReasons

    The table of possible absence reasons.

    Accessible via :menuselection:`Configure --> Calendar --> Absence
    reasons`.

    >>> show_menu_path(cal.AbsenceReasons)
    Configure --> Calendar --> Absence reasons

    >>> rt.show(cal.AbsenceReasons)
    ==== ==================== ========================== ====================
     ID   Designation          Designation (de)           Designation (fr)
    ---- -------------------- -------------------------- --------------------
     1    Sickness             Krankheit                  Sickness
     2    Other valid reason   Sonstiger gültiger Grund   Other valid reason
     3    Unknown              Unbekannt                  Inconnu
     4    Unjustified          Unberechtigt               Unjustified
    ==== ==================== ========================== ====================
    <BLANKLINE>


.. class:: AbsenceReason

   .. attribute:: name
