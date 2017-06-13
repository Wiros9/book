.. _noi.specs.as_pdf:

=================
Printing tables
=================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_as_pdf
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_book.projects.team.settings.demo')
    >>> from lino.api.doctest import *


This document describes and tests the print to pdf function.


.. contents::
  :local:

>>> settings.SITE.appy_params.update(raiseOnError=True)
>>> test_client.force_login(rt.login('robin').user)
>>> def mytest(k):
...     url = 'http://127.0.0.1:8000/api/{0}?an=as_pdf'.format(k)
...     res = test_client.get(url, REMOTE_USER='robin')
...     assert res.status_code == 200, "Request to {} got status code {}".format(url, res.status_code)
...     result = json.loads(res.content)
...     assert result['success']
...     print(result['open_url'])

>>> mytest("tickets/TicketsToDo")  #doctest: +SKIP
/media/cache/appypdf/127.0.0.1/tickets.TicketsToDo.pdf

>>> mytest("tickets/AllTickets")  #doctest: +SKIP
/media/cache/appypdf/127.0.0.1/tickets.AllTickets.pdf
