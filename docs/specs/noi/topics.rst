.. _noi.specs.topics:

=============================
Topics in Lino Noi
=============================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_topics
    
    doctest init:

    >>> import lino
    >>> lino.startup('lino_book.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document specifies the ticket management functions of Lino Noi,
implemented in :mod:`lino_xl.lib.tickets`.


.. contents::
  :local:



Topics
========

The :attr:`topic <lino_xl.lib.tickets.models.Ticket.topic>` of a
ticket is what Trac calls "component". Topics are a "customer-side"
classification of the different components which are being developed
by the team that uses a given Lino Noi site.

There are 4 topics in the demo database.

>>> show_menu_path(topics.AllTopics)
Configure --> Topics --> Topics



>>> rt.show(topics.AllTopics)
=========== ============== ================== ================== =============
 Reference   Designation    Designation (de)   Designation (fr)   Topic group
----------- -------------- ------------------ ------------------ -------------
 linõ        Lino Core
 welfäre     Lino Welfare
 così        Lino Cosi
 faggio      Lino Voga
=========== ============== ================== ================== =============
<BLANKLINE>


Choosing a topic
================

When choosing a topic, the search text looks in both the
:guilabel:`Reference` and the :guilabel:`Designation` field:

>>> base = '/choices/tickets/Tickets/topic'
>>> show_choices("robin", base + '?query=')
<br/>
Lino Core
Lino Welfare
Lino Cosi
Lino Voga

Note that we have a topic whose `ref` is different from `name`, and
that the search works in both fields:

>>> obj = topics.Topic.get_by_ref('faggio')
>>> print(obj.ref)
faggio
>>> print(obj.name)
Lino Voga

>>> show_choices("robin", base + '?query=fag')
Lino Voga

>>> show_choices("robin", base + '?query=voga')
Lino Voga


Interests
=========

Every partner can have its list of "interests". They will get notified
about changes in these topics even when they did not report the
ticket.


>>> obj = contacts.Company.objects.get(name="welket")
>>> rt.show(topics.InterestsByController, obj)
... #doctest: +REPORT_UDIFF
Lino Core, Lino Welfare, Lino Cosi

>>> obj = topics.Topic.objects.get(ref="welfäre")
>>> rt.show(topics.InterestsByTopic, obj)
... #doctest: +REPORT_UDIFF
======================
 Controlled by
----------------------
 *welket*
 *welsch*
 *2015-05-21 by Jean*
======================
<BLANKLINE>


Filtering tickets by topic
==========================

>>> pv = dict(topic=rt.models.topics.Topic.get_by_ref("così"))
>>> rt.show(tickets.Tickets, param_values=pv)
... #doctest: -REPORT_UDIFF
===== =========================================== ========= =========== =========== ====== ==========
 ID    Summary                                     Author    Topic       Actions     Site   Mission
----- ------------------------------------------- --------- ----------- ----------- ------ ----------
 114   Ticket 114                                  Jean      Lino Cosi   **Talk**           téam
 110   Ticket 110                                  Mathieu   Lino Cosi   **Ready**          docs
 106   Ticket 106                                  Luc       Lino Cosi   **Talk**           research
 102   Ticket 102                                  Jean      Lino Cosi   **Ready**          shop
 98    Ticket 98                                   Mathieu   Lino Cosi   **Talk**           linö
 94    Ticket 94                                   Luc       Lino Cosi   **Ready**          téam
 90    Ticket 90                                   Jean      Lino Cosi   **Talk**           docs
 86    Ticket 86                                   Mathieu   Lino Cosi   **Ready**          research
 82    Ticket 82                                   Luc       Lino Cosi   **Talk**           shop
 78    Ticket 78                                   Jean      Lino Cosi   **Ready**          linö
 74    Ticket 74                                   Mathieu   Lino Cosi   **Talk**           téam
 70    Ticket 70                                   Luc       Lino Cosi   **Ready**          docs
 66    Ticket 66                                   Jean      Lino Cosi   **Talk**           research
 62    Ticket 62                                   Mathieu   Lino Cosi   **Ready**          shop
 58    Ticket 58                                   Luc       Lino Cosi   **Talk**           linö
 54    Ticket 54                                   Jean      Lino Cosi   **Ready**          téam
 50    Ticket 50                                   Mathieu   Lino Cosi   **Talk**           docs
 46    Ticket 46                                   Luc       Lino Cosi   **Ready**          research
 42    Ticket 42                                   Jean      Lino Cosi   **Talk**           shop
 38    Ticket 38                                   Mathieu   Lino Cosi   **Ready**          linö
 34    Ticket 34                                   Luc       Lino Cosi   **Talk**           téam
 30    Ticket 30                                   Jean      Lino Cosi   **Ready**          docs
 26    Ticket 26                                   Mathieu   Lino Cosi   **Talk**           research
 22    Ticket 22                                   Luc       Lino Cosi   **Ready**          shop
 18    Ticket 18                                   Jean      Lino Cosi   **Talk**           linö
 14    Bar cannot baz                              Mathieu   Lino Cosi   **Ready**          téam
 10    Where can I find a Foo when bazing Bazes?   Luc       Lino Cosi   **Talk**           docs
 6     Sell bar in baz                             Jean      Lino Cosi   **Ready**          research
 2     Bar is not always baz                       Mathieu   Lino Cosi   **Talk**           téam
===== =========================================== ========= =========== =========== ====== ==========
<BLANKLINE>

 


Topic groups
============

>>> rt.show(topics.TopicGroups)
No data to display

>>> show_menu_path(topics.TopicGroups)
Configure --> Topics --> Topic groups
