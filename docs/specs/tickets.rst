.. _noi.specs.tickets:

=============================
Ticket management in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_tickets
    
    doctest init:
    >>> import lino
    >>> lino.startup('lino_noi.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_xl.lib.tickets`.

.. contents::
  :local:


What is a ticket?
=================


.. currentmodule:: lino_xl.lib.tickets

.. class:: Ticket

    A **Ticket** is a concrete question or problem formulated by a
    user.

    The user may be a system user or an end user represented by a
    system user.

    A Ticket is always related to one and only one Project.  It may be
    related to other tickets which may belong to other projects.


    .. attribute:: user

        The user who entered this ticket and is responsible for
        managing it.

    .. attribute:: end_user

        The end user who is asking for help.

    .. attribute:: assigned_to

        No longer used. The user who is working on this ticket.

        If this field is empty and :attr:`project` is not empty, then
        default value is taken from :attr:`Project.assign_to`.

    .. attribute:: state

        The state of this ticket. See :class:`TicketStates
        <lino_xl.lib.tickets.choicelists.TicketStates>`

    .. attribute:: waiting_for

        What to do next. An unformatted one-line text which describes
        what this ticket is waiting for.

    .. attribute:: upgrade_notes

        A formatted text field meant for writing instructions for the
        hoster's site administrator when doing an upgrade where this
        ticket is being deployed.

    .. attribute:: description

        A complete and concise description of the ticket. This should
        describe in more detail what this ticket is about. If the
        ticket has evolved during time, it should reflect the latest
        version.

        The description can contain *memo commands* defined by the
        application.

    .. attribute:: duplicate_of

        A pointer to the ticket which is the cause of this ticket.

        A ticket with a non-empty :attr:`duplicate_of` field can be
        called a "duplicate".  The number of a duplicate is
        theoretically higher than the number of the ticket it
        duplicates.

        The :attr:`state` of a duplicate does not automatically become
        that of the duplicated ticket.  Each ticket continues to have
        its own state. Example: Some long time ago, with Mathieu, we
        agreed that ticket #100 can go to *Sleeping*. Now Aurélie
        reported the same problem again as #904. This means that we
        should talk about it. And even before talking with her, I'd
        like to have a look at the code in order to estimate whether
        it is difficult or not, so I set the state of #904 to ToDo.

        Wouldn't it be preferrable to replace the :attr:`duplicate_of
        field by a :class:`LinkType
        <lino_xl.lib.tickets.choicelists.LinkTypes>` called
        "Duplicated/Duplicated by"?  No. We had this before and
        preferred the field, because a field is at least one click
        less, and because we *want* users to define a clear hiearchy
        with a clear root ticket. You can have a group of tickets
        which are all direct or indirect duplicates of this "root of
        all other problems".

    .. attribute:: deadline

        Specify that the ticket must be done for a given date.

        TODO: Triagers should have a table of tickets having this
        field non-empty and are still in an active state.

    .. attribute:: priority

        How urgent this ticket is. This should be a value between 0
        and 100.

    .. attribute:: rating

        How the author rates this ticket.

    .. attribute:: reporting_type

        An indication about who is going to pay for work on this
        project.  See :class:`ReportingTypes`.



Lifecycle of a ticket
=====================

The :attr:`state <lino_xl.lib.tickets.models.Ticket.state>` of a
ticket has one of the following values:

>>> rt.show(tickets.TicketStates)
======= =========== =========== ======== ========
 value   name        text        Symbol   Active
------- ----------- ----------- -------- --------
 10      new         New         ⛶        Yes
 15      talk        Talk        ☎        Yes
 20      opened      Open        ☉        Yes
 22      started     Started     ⚒        Yes
 30      sleeping    Sleeping    ☾        No
 40      ready       Ready       ☐        Yes
 50      closed      Closed      ☑        No
 60      cancelled   Cancelled   ☒        No
======= =========== =========== ======== ========
<BLANKLINE>

There is also a "modern" series of symbols, which can be enabled
site-wide in :attr:`lino.core.site.Site.use_new_unicode_symbols`.

You can see this table in your web interface using
:menuselection:`Explorer --> Tickets --> States`.

.. >>> show_menu_path(tickets.TicketStates)
   Explorer --> Tickets --> States

See :class:`lino_xl.lib.tickets.choicelists.TicketStates` for more
information about every state.

Above table in German:

>>> rt.show(tickets.TicketStates, language="de")
====== =========== =============== ======== =======
 Wert   name        Text            Symbol   Aktiv
------ ----------- --------------- -------- -------
 10     new         Neu             ⛶        Ja
 15     talk        Besprechen      ☎        Ja
 20     opened      Offen           ☉        Ja
 22     started     Gestartet       ⚒        Ja
 30     sleeping    Schläft         ☾        Nein
 40     ready       Bereit          ☐        Ja
 50     closed      Abgeschlossen   ☑        Nein
 60     cancelled   Storniert       ☒        Nein
====== =========== =============== ======== =======
<BLANKLINE>

And in French (not yet fully translated):

>>> rt.show(tickets.TicketStates, language="fr")
======= =========== ========== ======== ========
 value   name        text       Symbol   Active
------- ----------- ---------- -------- --------
 10      new         Nouveau    ⛶        Oui
 15      talk        Talk       ☎        Oui
 20      opened      Open       ☉        Oui
 22      started     Started    ⚒        Oui
 30      sleeping    Sleeping   ☾        Non
 40      ready       Ready      ☐        Oui
 50      closed      Closed     ☑        Non
 60      cancelled   Annulé     ☒        Non
======= =========== ========== ======== ========
<BLANKLINE>


Note that a ticket also has a checkbox for marking it as :attr:`closed
<lino_xl.lib.tickets.models.Ticket.closed>`.  This means that a ticket
can be marked as "closed" in any of above states.  We don't use this for the moment and are not sure
whether this is a cool feature (:ticket:`372`).

- :attr:`standby <lino_xl.lib.tickets.models.Ticket.standby>`



Projects
========

The :attr:`project <lino_xl.lib.tickets.models.Ticket.project>` of a
ticket is used to specify "who is going to pay" for it. Lino Noi does
not issue invoices, so it uses this information only for reporting
about it and helping with the decision about whether and how worktime
is being invoiced to the customer.  But the invoicing itself is not
currently a goal of Lino Noi.

So a **project** is something for which somebody is possibly willing
to pay money.

>>> rt.show(tickets.Projects)
=========== =============== ======== ========= =========
 Reference   Name            Parent   Company   Private
----------- --------------- -------- --------- ---------
 linö        Framewörk                welket    No
 téam        Téam            linö     welsch    Yes
 docs        Documentatión   linö     pypi      No
 research    Research        docs     welket    No
 shop        Shop                     welsch    No
=========== =============== ======== ========= =========
<BLANKLINE>


>>> rt.show(tickets.TopLevelProjects)
=========== =========== ======== ================
 Reference   Name        Parent   Children
----------- ----------- -------- ----------------
 linö        Framewörk            *téam*, *docs*
 shop        Shop
=========== =========== ======== ================
<BLANKLINE>


Developers can start working on tickets without specifying a project
(i.e. without knowing who is going to pay for their work).  

But after some time every ticket should get assigned to some
project. You can see a list of tickets which have not yet been
assigned to a project:

>>> pv = dict(has_project=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: +REPORT_UDIFF
==== =================== ========= ============== ============== =========
 ID   Summary             Author    Topic          Actions        Project
---- ------------------- --------- -------------- -------------- ---------
 5    Cannot create Foo   Mathieu   Lino Welfare   **Sleeping**
 3    Baz sucks           Luc       Lino Voga      **Open**
==== =================== ========= ============== ============== =========
<BLANKLINE>


Distribution of tickets per project
===================================

In our demo database, tickets are distributed over the different
projects as follows (not a realistic distribution):

>>> for p in tickets.Project.objects.all():
...         print p.ref, p.tickets_by_project.count()
linö 23
téam 22
docs 23
research 23
shop 23



Private tickets
===============

Tickets are private by default. But when they are assigned to a public
project, then their privacy is removed.

So the private tickets are (1) those in project "téam" and (2) those
without project:

>>> pv = dict(show_private=dd.YesNo.yes)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary project")
... #doctest: -REPORT_UDIFF
===== =========================== =========
 ID    Summary                     Project
----- --------------------------- ---------
 112   Ticket 112                  téam
 107   Ticket 107                  téam
 102   Ticket 102                  téam
 97    Ticket 97                   téam
 92    Ticket 92                   téam
 87    Ticket 87                   téam
 82    Ticket 82                   téam
 77    Ticket 77                   téam
 72    Ticket 72                   téam
 67    Ticket 67                   téam
 62    Ticket 62                   téam
 57    Ticket 57                   téam
 52    Ticket 52                   téam
 47    Ticket 47                   téam
 42    Ticket 42                   téam
 37    Ticket 37                   téam
 32    Ticket 32                   téam
 27    Ticket 27                   téam
 22    Ticket 22                   téam
 17    Ticket 17                   téam
 12    Foo cannot bar              téam
 7     No Foo after deleting Bar   téam
 5     Cannot create Foo
 3     Baz sucks
===== =========================== =========
<BLANKLINE>



And these are the public tickets:

>>> pv = dict(show_private=dd.YesNo.no)
>>> rt.show(tickets.Tickets, param_values=pv,
...     column_names="id summary project")
... #doctest: -REPORT_UDIFF
===== =========================================== ==========
 ID    Summary                                     Project
----- ------------------------------------------- ----------
 116   Ticket 116                                  linö
 115   Ticket 115                                  shop
 114   Ticket 114                                  research
 113   Ticket 113                                  docs
 111   Ticket 111                                  linö
 110   Ticket 110                                  shop
 109   Ticket 109                                  research
 108   Ticket 108                                  docs
 106   Ticket 106                                  linö
 105   Ticket 105                                  shop
 104   Ticket 104                                  research
 103   Ticket 103                                  docs
 101   Ticket 101                                  linö
 100   Ticket 100                                  shop
 99    Ticket 99                                   research
 98    Ticket 98                                   docs
 96    Ticket 96                                   linö
 95    Ticket 95                                   shop
 94    Ticket 94                                   research
 93    Ticket 93                                   docs
 91    Ticket 91                                   linö
 90    Ticket 90                                   shop
 89    Ticket 89                                   research
 88    Ticket 88                                   docs
 86    Ticket 86                                   linö
 85    Ticket 85                                   shop
 84    Ticket 84                                   research
 83    Ticket 83                                   docs
 81    Ticket 81                                   linö
 80    Ticket 80                                   shop
 79    Ticket 79                                   research
 78    Ticket 78                                   docs
 76    Ticket 76                                   linö
 75    Ticket 75                                   shop
 74    Ticket 74                                   research
 73    Ticket 73                                   docs
 71    Ticket 71                                   linö
 70    Ticket 70                                   shop
 69    Ticket 69                                   research
 68    Ticket 68                                   docs
 66    Ticket 66                                   linö
 65    Ticket 65                                   shop
 64    Ticket 64                                   research
 63    Ticket 63                                   docs
 61    Ticket 61                                   linö
 60    Ticket 60                                   shop
 59    Ticket 59                                   research
 58    Ticket 58                                   docs
 56    Ticket 56                                   linö
 55    Ticket 55                                   shop
 54    Ticket 54                                   research
 53    Ticket 53                                   docs
 51    Ticket 51                                   linö
 50    Ticket 50                                   shop
 49    Ticket 49                                   research
 48    Ticket 48                                   docs
 46    Ticket 46                                   linö
 45    Ticket 45                                   shop
 44    Ticket 44                                   research
 43    Ticket 43                                   docs
 41    Ticket 41                                   linö
 40    Ticket 40                                   shop
 39    Ticket 39                                   research
 38    Ticket 38                                   docs
 36    Ticket 36                                   linö
 35    Ticket 35                                   shop
 34    Ticket 34                                   research
 33    Ticket 33                                   docs
 31    Ticket 31                                   linö
 30    Ticket 30                                   shop
 29    Ticket 29                                   research
 28    Ticket 28                                   docs
 26    Ticket 26                                   linö
 25    Ticket 25                                   shop
 24    Ticket 24                                   research
 23    Ticket 23                                   docs
 21    Ticket 21                                   linö
 20    Ticket 20                                   shop
 19    Ticket 19                                   research
 18    Ticket 18                                   docs
 16    How to get bar from foo                     linö
 15    Bars have no foo                            shop
 14    Bar cannot baz                              research
 13    Bar cannot foo                              docs
 11    Class-based Foos and Bars?                  linö
 10    Where can I find a Foo when bazing Bazes?   shop
 9     Foo never matches Bar                       research
 8     Is there any Bar in Foo?                    docs
 6     Sell bar in baz                             linö
 4     Foo and bar don't baz                       shop
 2     Bar is not always baz                       research
 1     Föö fails to bar when baz                   docs
===== =========================================== ==========
<BLANKLINE>



There are 18 private and 98 public tickets in the demo database.

>>> tickets.Ticket.objects.filter(private=True).count()
18
>>> tickets.Ticket.objects.filter(private=False).count()
98

My tickets
==========

>>> rt.login('jean').show(tickets.MyTickets)
... #doctest: +REPORT_UDIFF
============================================================== ========================================
 Description                                                    Actions
-------------------------------------------------------------- ----------------------------------------
 `#115 (Ticket 115) <Detail>`__                                 [▶] [★] **Open** → [☾] [☎] [⚒] [☐] [☑]
 `#106 (Ticket 106) <Detail>`__                                 [▶] [★] **Talk** → [☾] [☉] [⚒] [☐] [☑]
 `#102 (Ticket 102) <Detail>`__                                 [▶] [★] **Ready** → [☎] [☑]
 `#100 (Ticket 100) <Detail>`__                                 [▶] [★] **Started** → [☾] [☎] [☐] [☑]
 `#97 (Ticket 97) <Detail>`__                                   [▶] [★] **New** → [☾] [☎] [☉] [⚒] [☐]
 `#91 (Ticket 91) <Detail>`__                                   [▶] [★] **Open** → [☾] [☎] [⚒] [☐] [☑]
 `#82 (Ticket 82) <Detail>`__                                   [▶] [★] **Talk** → [☾] [☉] [⚒] [☐] [☑]
 `#78 (Ticket 78) <Detail>`__                                   [▶] [★] **Ready** → [☎] [☑]
 `#76 (Ticket 76) <Detail>`__                                   [▶] [★] **Started** → [☾] [☎] [☐] [☑]
 `#73 (Ticket 73) <Detail>`__                                   [▶] [★] **New** → [☾] [☎] [☉] [⚒] [☐]
 `#67 (Ticket 67) <Detail>`__                                   [▶] [★] **Open** → [☾] [☎] [⚒] [☐] [☑]
 `#58 (Ticket 58) <Detail>`__                                   [▶] [★] **Talk** → [☾] [☉] [⚒] [☐] [☑]
 `#54 (Ticket 54) <Detail>`__                                   [▶] [★] **Ready** → [☎] [☑]
 `#52 (Ticket 52) <Detail>`__                                   [▶] [★] **Started** → [☾] [☎] [☐] [☑]
 `#49 (Ticket 49) <Detail>`__                                   [▶] [★] **New** → [☾] [☎] [☉] [⚒] [☐]
 `#43 (Ticket 43) <Detail>`__                                   [▶] [★] **Open** → [☾] [☎] [⚒] [☐] [☑]
 `#34 (Ticket 34) <Detail>`__                                   [▶] [★] **Talk** → [☾] [☉] [⚒] [☐] [☑]
 `#30 (Ticket 30) <Detail>`__                                   [▶] [★] **Ready** → [☎] [☑]
 `#28 (Ticket 28) <Detail>`__                                   [▶] [★] **Started** → [☾] [☎] [☐] [☑]
 `#25 (Ticket 25) <Detail>`__                                   [▶] [★] **New** → [☾] [☎] [☉] [⚒] [☐]
 `#19 (Ticket 19) <Detail>`__                                   [▶] [★] **Open** → [☾] [☎] [⚒] [☐] [☑]
 `#10 (Where can I find a Foo when bazing Bazes?) <Detail>`__   [▶] [★] **Talk** → [☾] [☉] [⚒] [☐] [☑]
 `#6 (Sell bar in baz) <Detail>`__                              [▶] [★] **Ready** → [☎] [☑]
 `#4 (Foo and bar don't baz) <Detail>`__                        [▶] [★] **Started** → [☾] [☎] [☐] [☑]
 `#1 (Föö fails to bar when baz) <Detail>`__                    [▶] [★] **New** → [☾] [☎] [☉] [⚒] [☐]
============================================================== ========================================
<BLANKLINE>


Sites
=====

Lino Noi has a list of all sites for which we do support:

>>> rt.show(tickets.Sites)
============= ========= ======== ====
 Designation   Partner   Remark   ID
------------- --------- -------- ----
 pypi          pypi               3
 welket        welket             1
 welsch        welsch             2
============= ========= ======== ====
<BLANKLINE>

A ticket may or may not be "local", i.e. specific to a given site.
When a ticket is site-specific, we simply assign the `site` field.  We
can see all local tickets for a given site object:

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(tickets.TicketsBySite, welket)
... #doctest: -REPORT_UDIFF -SKIP
===== ============ ========= ============== ============== ==========
 ID    Summary      Author    Topic          Actions        Project
----- ------------ --------- -------------- -------------- ----------
 109   Ticket 109   Jean      Lino Welfare   **Sleeping**   research
 91    Ticket 91    Jean      Lino Voga      **Open**       linö
 79    Ticket 79    Mathieu   Lino Voga      **Closed**     research
 61    Ticket 61    Jean      Lino Welfare   **Sleeping**   linö
 49    Ticket 49    Jean      Lino Welfare   **New**        research
 31    Ticket 31    Mathieu   Lino Voga      **Closed**     linö
 19    Ticket 19    Jean      Lino Voga      **Open**       research
===== ============ ========= ============== ============== ==========
<BLANKLINE>


Note that the above table shows no state change actions in the
Actions column because it is being requested by anonymous. For an
authenticated developer it looks like this:

>>> rt.login('luc').show(tickets.TicketsBySite, welket)
... #doctest: -REPORT_UDIFF -SKIP
===== ============ ========= ============== ================== ==========
 ID    Summary      Author    Topic          Actions            Project
----- ------------ --------- -------------- ------------------ ----------
 109   Ticket 109   Jean      Lino Welfare   [☆] **Sleeping**   research
 91    Ticket 91    Jean      Lino Voga      [▶] [★] **Open**   linö
 79    Ticket 79    Mathieu   Lino Voga      [☆] **Closed**     research
 61    Ticket 61    Jean      Lino Welfare   [☆] **Sleeping**   linö
 49    Ticket 49    Jean      Lino Welfare   [▶] [★] **New**    research
 31    Ticket 31    Mathieu   Lino Voga      [☆] **Closed**     linö
 19    Ticket 19    Jean      Lino Voga      [▶] [★] **Open**   research
===== ============ ========= ============== ================== ==========
<BLANKLINE>






Milestones
==========

Every site can have its list of "milestones" or "releases". A
milestone is when a site gets an upgrade of the software which is
running there. 

A milestone is not necessary an *official* release of a new
version. It just means that you release some changed software to the
users of that site.

>>> welket = tickets.Site.objects.get(name="welket")
>>> rt.show(rt.actors.deploy.MilestonesBySite, welket)
... #doctest: -REPORT_UDIFF
======= ============== ============ ======== ====
 Label   Expected for   Reached      Closed   ID
------- -------------- ------------ -------- ----
         15/05/2015     15/05/2015   No       7
         11/05/2015     11/05/2015   No       5
         07/05/2015     07/05/2015   No       3
         03/05/2015     03/05/2015   No       1
======= ============== ============ ======== ====
<BLANKLINE>


Deployments
===========

Every milestone has its list of "deployments", i.e. the tickets that
are being fixed when this milestone is reached.

The demo database currently does not have any deployments:

>>> rt.show(rt.actors.deploy.Deployments)
No data to display


Release notes
=============

Lino Noi has an excerpt type for printing a milestone.  This was used
to produce *release notes*.

>>> obj = deploy.Milestone.objects.get(pk=7)
>>> rt.show(rt.actors.deploy.DeploymentsByMilestone, obj)
No data to display

>>> rt.show(clocking.OtherTicketsByMilestone, obj) #doctest: +SKIP
No data to display



Dependencies between tickets
============================


.. class:: LinkTypes

    The possible values of a :class:`lino_xl.lib.tickets.Link`.

    .. attribute:: requires

        The parent ticket requires the child ticket.
    
    .. attribute:: triggers

        The parent ticket triggers the child ticket.
    
    .. attribute:: deploys

        The parent ticket is a deployment which deploys the child ticket.

        Release notes are a printout of a deployment ticket which
        lists the deployed tickets.


>>> rt.show(tickets.LinkTypes)
... #doctest: +REPORT_UDIFF
======= =========== ===========
 value   name        text
------- ----------- -----------
 10      requires    Requires
 20      triggers    Triggers
 30      suggests    Suggests
 40      obsoletes   Obsoletes
======= =========== ===========
<BLANKLINE>




>>> rt.show(tickets.Links)
... #doctest: +REPORT_UDIFF
==== ================= ================================ ============================
 ID   Dependency type   Parent                           Child
---- ----------------- -------------------------------- ----------------------------
 1    Requires          #1 (Föö fails to bar when baz)   #2 (Bar is not always baz)
==== ================= ================================ ============================
<BLANKLINE>


Comments
========

Comments on private tickets are not shown to anonymous users:

>>> rt.show(comments.Comments, column_names="id user short_text")
+----+-----------------+--------------------------------------------------------------------------------+
| ID | Author          | Short text                                                                     |
+====+=================+================================================================================+
| 1  | Jean            | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
| 2  | Luc             | Who| What| Done?                                                               |
|    |                 | ---|---|---                                                                    |
|    |                 | Him| Bar|                                                                      |
|    |                 | Her| Foo the Bar| **x**                                                        |
|    |                 | Them| Floop the pig                                                            |
|    |                 | | x                                                                            |
+----+-----------------+--------------------------------------------------------------------------------+
| 4  | Romain Raffault | Lorem ipsum** dolor sit amet**, consectetur adipiscing elit. Nunc cursus felis |
|    |                 | nisi, eu pellentesque lorem lobortis non. Aenean non sodales neque, vitae      |
|    |                 | venenatis lectus. In eros dui, gravida et dolor at, pellentesque hendrerit     |
|    |                 | magna. Quisque vel lectus dictum, rhoncus massa feugiat, condimentum sem.      |
|    |                 | Donec elit nisl, placerat vitae imperdiet eget, hendrerit nec quam. Ut         |
|    |                 | elementum ligula vitae odio efficitur rhoncus. Duis in blandit neque. Sed      |
|    |                 | dictum mollis volutpat. Morbi at est et nisi euismod viverra. Nulla quis lacus |
|    |                 | vitae ante sollicitudin tincidunt. Donec nec enim in leo vulputate ultrices.   |
|    |                 | Suspendisse potenti. Ut elit nibh, porta ut enim ac, convallis molestie risus. |
|    |                 | Praesent consectetur lacus lacus, in faucibus justo fringilla vel.             |
|    |                 |                                                                                |
|    |                 | Donec fermentum enim et maximus vestibulum. Sed mollis lacus quis dictum       |
|    |                 | fermentum. Maecenas libero tellus, hendrerit cursus pretium et, hendrerit quis |
|    |                 | lectus. Nunc bibendum nunc nunc, ac commodo sem interdum ut. Quisque vitae     |
|    |                 | turpis lectus. Nullam efficitur scelerisque hendrerit. Fusce feugiat           |
|    |                 | ullamcorper nulla. Suspendisse quis placerat ligula. Etiam ullamcorper         |
|    |                 | elementum consectetur. Aenean et diam ullamcorper, posuere turpis eget,        |
|    |                 | egestas nibh. Quisque condimentum arcu ac metus sodales placerat. Quisque      |
|    |                 | placerat, quam nec tincidunt pharetra, urna justo scelerisque urna, et         |
|    |                 | vulputate ipsum lacus at ligula.                                               |
+----+-----------------+--------------------------------------------------------------------------------+
| 6  | Robin Rood      | Lorem ipsum ** dolor sit amet**, consectetur adipiscing elit. Donec interdum   |
|    |                 | dictum erat. Fusce condimentum erat a pulvinar ultricies.                      |
|    |                 |                                                                                |
|    |                 | Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.      |
|    |                 |                                                                                |
|    |                 | Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel |
|    |                 | enim vel eros venenatis congue.                                                |
+----+-----------------+--------------------------------------------------------------------------------+
| 8  | Luc             | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
| 9  | Mathieu         | Who| What| Done?                                                               |
|    |                 | ---|---|---                                                                    |
|    |                 | Him| Bar|                                                                      |
|    |                 | Her| Foo the Bar| **x**                                                        |
|    |                 | Them| Floop the pig                                                            |
|    |                 | | x                                                                            |
+----+-----------------+--------------------------------------------------------------------------------+
| 10 | Romain Raffault | Lorem ipsum** dolor sit amet**, consectetur adipiscing elit. Nunc cursus felis |
|    |                 | nisi, eu pellentesque lorem lobortis non. Aenean non sodales neque, vitae      |
|    |                 | venenatis lectus. In eros dui, gravida et dolor at, pellentesque hendrerit     |
|    |                 | magna. Quisque vel lectus dictum, rhoncus massa feugiat, condimentum sem.      |
|    |                 | Donec elit nisl, placerat vitae imperdiet eget, hendrerit nec quam. Ut         |
|    |                 | elementum ligula vitae odio efficitur rhoncus. Duis in blandit neque. Sed      |
|    |                 | dictum mollis volutpat. Morbi at est et nisi euismod viverra. Nulla quis lacus |
|    |                 | vitae ante sollicitudin tincidunt. Donec nec enim in leo vulputate ultrices.   |
|    |                 | Suspendisse potenti. Ut elit nibh, porta ut enim ac, convallis molestie risus. |
|    |                 | Praesent consectetur lacus lacus, in faucibus justo fringilla vel.             |
|    |                 |                                                                                |
|    |                 | Donec fermentum enim et maximus vestibulum. Sed mollis lacus quis dictum       |
|    |                 | fermentum. Maecenas libero tellus, hendrerit cursus pretium et, hendrerit quis |
|    |                 | lectus. Nunc bibendum nunc nunc, ac commodo sem interdum ut. Quisque vitae     |
|    |                 | turpis lectus. Nullam efficitur scelerisque hendrerit. Fusce feugiat           |
|    |                 | ullamcorper nulla. Suspendisse quis placerat ligula. Etiam ullamcorper         |
|    |                 | elementum consectetur. Aenean et diam ullamcorper, posuere turpis eget,        |
|    |                 | egestas nibh. Quisque condimentum arcu ac metus sodales placerat. Quisque      |
|    |                 | placerat, quam nec tincidunt pharetra, urna justo scelerisque urna, et         |
|    |                 | vulputate ipsum lacus at ligula.                                               |
+----+-----------------+--------------------------------------------------------------------------------+
| 11 | Rolf Rompen     | Lorem ipsum ** dolor sit amet**, consectetur adipiscing elit. Donec interdum   |
|    |                 | dictum erat. Fusce condimentum erat a pulvinar ultricies.                      |
|    |                 |                                                                                |
|    |                 | Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.      |
|    |                 |                                                                                |
|    |                 | Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel |
|    |                 | enim vel eros venenatis congue.                                                |
+----+-----------------+--------------------------------------------------------------------------------+
| 12 | Robin Rood      | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
<BLANKLINE>

The same list seen by marc

>>> rt.login('luc').show('comments.Comments', column_names="id user short_text")
+----+-----------------+--------------------------------------------------------------------------------+
| ID | Author          | Short text                                                                     |
+====+=================+================================================================================+
| 1  | Jean            | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
| 2  | Luc             | Who| What| Done?                                                               |
|    |                 | ---|---|---                                                                    |
|    |                 | Him| Bar|                                                                      |
|    |                 | Her| Foo the Bar| **x**                                                        |
|    |                 | Them| Floop the pig                                                            |
|    |                 | | x                                                                            |
+----+-----------------+--------------------------------------------------------------------------------+
| 3  | Mathieu         | Very confidential comment                                                      |
+----+-----------------+--------------------------------------------------------------------------------+
| 4  | Romain Raffault | Lorem ipsum** dolor sit amet**, consectetur adipiscing elit. Nunc cursus felis |
|    |                 | nisi, eu pellentesque lorem lobortis non. Aenean non sodales neque, vitae      |
|    |                 | venenatis lectus. In eros dui, gravida et dolor at, pellentesque hendrerit     |
|    |                 | magna. Quisque vel lectus dictum, rhoncus massa feugiat, condimentum sem.      |
|    |                 | Donec elit nisl, placerat vitae imperdiet eget, hendrerit nec quam. Ut         |
|    |                 | elementum ligula vitae odio efficitur rhoncus. Duis in blandit neque. Sed      |
|    |                 | dictum mollis volutpat. Morbi at est et nisi euismod viverra. Nulla quis lacus |
|    |                 | vitae ante sollicitudin tincidunt. Donec nec enim in leo vulputate ultrices.   |
|    |                 | Suspendisse potenti. Ut elit nibh, porta ut enim ac, convallis molestie risus. |
|    |                 | Praesent consectetur lacus lacus, in faucibus justo fringilla vel.             |
|    |                 |                                                                                |
|    |                 | Donec fermentum enim et maximus vestibulum. Sed mollis lacus quis dictum       |
|    |                 | fermentum. Maecenas libero tellus, hendrerit cursus pretium et, hendrerit quis |
|    |                 | lectus. Nunc bibendum nunc nunc, ac commodo sem interdum ut. Quisque vitae     |
|    |                 | turpis lectus. Nullam efficitur scelerisque hendrerit. Fusce feugiat           |
|    |                 | ullamcorper nulla. Suspendisse quis placerat ligula. Etiam ullamcorper         |
|    |                 | elementum consectetur. Aenean et diam ullamcorper, posuere turpis eget,        |
|    |                 | egestas nibh. Quisque condimentum arcu ac metus sodales placerat. Quisque      |
|    |                 | placerat, quam nec tincidunt pharetra, urna justo scelerisque urna, et         |
|    |                 | vulputate ipsum lacus at ligula.                                               |
+----+-----------------+--------------------------------------------------------------------------------+
| 5  | Rolf Rompen     | Very confidential comment                                                      |
+----+-----------------+--------------------------------------------------------------------------------+
| 6  | Robin Rood      | Lorem ipsum ** dolor sit amet**, consectetur adipiscing elit. Donec interdum   |
|    |                 | dictum erat. Fusce condimentum erat a pulvinar ultricies.                      |
|    |                 |                                                                                |
|    |                 | Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.      |
|    |                 |                                                                                |
|    |                 | Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel |
|    |                 | enim vel eros venenatis congue.                                                |
+----+-----------------+--------------------------------------------------------------------------------+
| 7  | Jean            | Very confidential comment                                                      |
+----+-----------------+--------------------------------------------------------------------------------+
| 8  | Luc             | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
| 9  | Mathieu         | Who| What| Done?                                                               |
|    |                 | ---|---|---                                                                    |
|    |                 | Him| Bar|                                                                      |
|    |                 | Her| Foo the Bar| **x**                                                        |
|    |                 | Them| Floop the pig                                                            |
|    |                 | | x                                                                            |
+----+-----------------+--------------------------------------------------------------------------------+
| 10 | Romain Raffault | Lorem ipsum** dolor sit amet**, consectetur adipiscing elit. Nunc cursus felis |
|    |                 | nisi, eu pellentesque lorem lobortis non. Aenean non sodales neque, vitae      |
|    |                 | venenatis lectus. In eros dui, gravida et dolor at, pellentesque hendrerit     |
|    |                 | magna. Quisque vel lectus dictum, rhoncus massa feugiat, condimentum sem.      |
|    |                 | Donec elit nisl, placerat vitae imperdiet eget, hendrerit nec quam. Ut         |
|    |                 | elementum ligula vitae odio efficitur rhoncus. Duis in blandit neque. Sed      |
|    |                 | dictum mollis volutpat. Morbi at est et nisi euismod viverra. Nulla quis lacus |
|    |                 | vitae ante sollicitudin tincidunt. Donec nec enim in leo vulputate ultrices.   |
|    |                 | Suspendisse potenti. Ut elit nibh, porta ut enim ac, convallis molestie risus. |
|    |                 | Praesent consectetur lacus lacus, in faucibus justo fringilla vel.             |
|    |                 |                                                                                |
|    |                 | Donec fermentum enim et maximus vestibulum. Sed mollis lacus quis dictum       |
|    |                 | fermentum. Maecenas libero tellus, hendrerit cursus pretium et, hendrerit quis |
|    |                 | lectus. Nunc bibendum nunc nunc, ac commodo sem interdum ut. Quisque vitae     |
|    |                 | turpis lectus. Nullam efficitur scelerisque hendrerit. Fusce feugiat           |
|    |                 | ullamcorper nulla. Suspendisse quis placerat ligula. Etiam ullamcorper         |
|    |                 | elementum consectetur. Aenean et diam ullamcorper, posuere turpis eget,        |
|    |                 | egestas nibh. Quisque condimentum arcu ac metus sodales placerat. Quisque      |
|    |                 | placerat, quam nec tincidunt pharetra, urna justo scelerisque urna, et         |
|    |                 | vulputate ipsum lacus at ligula.                                               |
+----+-----------------+--------------------------------------------------------------------------------+
| 11 | Rolf Rompen     | Lorem ipsum ** dolor sit amet**, consectetur adipiscing elit. Donec interdum   |
|    |                 | dictum erat. Fusce condimentum erat a pulvinar ultricies.                      |
|    |                 |                                                                                |
|    |                 | Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.      |
|    |                 |                                                                                |
|    |                 | Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel |
|    |                 | enim vel eros venenatis congue.                                                |
+----+-----------------+--------------------------------------------------------------------------------+
| 12 | Robin Rood      | # Styled comment pasted from word!                                             |
+----+-----------------+--------------------------------------------------------------------------------+
<BLANKLINE>


>>> obj = tickets.Ticket.objects.get(pk=6)
>>> rt.show(comments.CommentsByRFC, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
<ul><li><a href="Detail" title="Created ...">...</a> by <em>Robin Rood</em> <a href="#" onclick="toggle_visibility('comment-6');" title="Hide">&#8284;</a><div id=comment-6><p>Lorem ipsum <strong> dolor sit amet</strong>, consectetur adipiscing elit. Donec interdum dictum erat. Fusce condimentum erat a pulvinar ultricies.</p>
<p>Phasellus gravida ullamcorper eros, sit amet blandit sapien laoreet quis.</p>
<p>Donec accumsan mauris at risus lobortis, nec pretium tortor aliquam. Nulla vel enim vel eros venenatis congue.</p></div></li></ul>



Filtering tickets
=================


>>> show_fields(tickets.Tickets)
+-----------------+-----------------+---------------------------------------------------------------+
| Internal name   | Verbose name    | Help text                                                     |
+=================+=================+===============================================================+
| user            | Author          |                                                               |
+-----------------+-----------------+---------------------------------------------------------------+
| end_user        | End user        | Only rows concerning this end user.                           |
+-----------------+-----------------+---------------------------------------------------------------+
| assigned_to     | Voted by        | Only tickets having a vote by this user.                      |
+-----------------+-----------------+---------------------------------------------------------------+
| not_assigned_to | Not voted by    | Only tickets having no vote by this user.                     |
+-----------------+-----------------+---------------------------------------------------------------+
| interesting_for | Interesting for | Only tickets interesting for this partner.                    |
+-----------------+-----------------+---------------------------------------------------------------+
| site            | Site            | Select a site if you want to see only tickets for this site.  |
+-----------------+-----------------+---------------------------------------------------------------+
| project         | Project         |                                                               |
+-----------------+-----------------+---------------------------------------------------------------+
| state           | State           | Only rows having this state.                                  |
+-----------------+-----------------+---------------------------------------------------------------+
| has_project     | Has project     | Show only (or hide) tickets which have a project assigned.    |
+-----------------+-----------------+---------------------------------------------------------------+
| show_assigned   | Assigned        | Whether to show assigned tickets                              |
+-----------------+-----------------+---------------------------------------------------------------+
| show_active     | Active          | Whether to show active tickets                                |
+-----------------+-----------------+---------------------------------------------------------------+
| show_todo       | To do           | Show only (or hide) tickets which are todo (i.e. state is New |
|                 |                 | or ToDo).                                                     |
+-----------------+-----------------+---------------------------------------------------------------+
| show_private    | Private         | Show only (or hide) tickets that are marked private.          |
+-----------------+-----------------+---------------------------------------------------------------+
| start_date      | Period from     | Start date of observed period                                 |
+-----------------+-----------------+---------------------------------------------------------------+
| end_date        | until           | End date of observed period                                   |
+-----------------+-----------------+---------------------------------------------------------------+
| observed_event  | Observed event  |                                                               |
+-----------------+-----------------+---------------------------------------------------------------+
| topic           | Topic           |                                                               |
+-----------------+-----------------+---------------------------------------------------------------+
| feasable_by     | Feasable by     | Show only tickets for which the given supplier is competent.  |
+-----------------+-----------------+---------------------------------------------------------------+




The detail layout of a ticket
=============================

Here is a textual description of the fields and their layout used in
the detail window of a ticket.

>>> from lino.utils.diag import py2rst
>>> print(py2rst(tickets.Tickets.detail_layout, True))
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
(main) [visible for all]:
- **General** (general_1):
  - (general1):
    - (general1_1): **Summary** (summary), **ID** (id)
    - (general1_2): **Author** (user), **End user** (end_user), **Deadline** (deadline)
    - (general1_3): **Site** (site), **Topic** (topic), **Project** (project)
    - (general1_4): **Actions** (workflow_buttons), **Private** (private)
    - (bottom_box_1) [visible for user consultant hoster developer senior admin]: **Wanted skills** (DemandsByDemander), **Votes** (VotesByVotable), **Sessions** (SessionsByTicket) [visible for consultant hoster developer senior admin]
  - **Comments** (CommentsByRFC)
- **More** (more):
  - (more_1):
    - (more1):
      - (more1_1): **Created** (created), **Modified** (modified), **Reported for** (reported_for), **Ticket type** (ticket_type)
      - (more1_2): **State** (state), **Duplicate of** (duplicate_of), **Planned time** (planned_time), **Priority** (priority)
    - **Duplicates** (DuplicatesByTicket)
  - (more_2): **Description** (description), **Resolution** (upgrade_notes), **Dependencies** (LinksByTicket) [visible for senior admin]
- **History** (changes.ChangesByMaster) [visible for senior admin]
- **Even more** (more2) [visible for user consultant hoster developer senior admin]:
  - **Deployments** (deploy.DeploymentsByTicket)
  - **Uploads** (UploadsByController)
<BLANKLINE>



Plugin configuration
====================

    
.. class:: Plugin
           
    See also :class:`lino.core.plugin.Plugin`

    .. attribute:: end_user_model


