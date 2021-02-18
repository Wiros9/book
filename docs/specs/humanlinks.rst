.. doctest docs/specs/humanlinks.rst
.. _lino.specs.humanlinks:

==============================================
``humanlinks`` : managing family relationships
==============================================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_book.projects.min9.settings')
    >>> from lino.api.doctest import *

The :mod:`lino_xl.lib.humanlinks` module adds functionality for
managing human links (i.e. relationships).

.. contents::
   :local:
   :depth: 2


Lars
====

Lars Braun is the natural son of Bruno Braun and Eveline Evrard.
Here is what Lars would say about them:

>>> Person = rt.models.contacts.Person
>>> Link = rt.models.humanlinks.Link
>>> lars = Person.objects.get(first_name="Lars", last_name="Braun")
>>> for lnk in Link.objects.filter(child=lars):
...    print(u"{} is my {}".format(lnk.parent,
...         lnk.type.as_parent(lnk.parent)))
Mr Bruno Braun is my Father
Mrs Eveline Evrard is my Mother
Mr Albert Adam is my Foster father
Mrs Françoise Freisen is my Foster mother
Mrs Daniela Radermacher is my Foster mother

Both parents married another partner. These new households
automatically did not create automatic foster parent links between
Lars and the new partners of his natural parents.
