.. _tested.core_utils:

Lino core utilities
===================

This document tests some functionality of :mod:`lino.core.utils`.

.. How to test only this document:

    $ python setup.py test -s tests.DocsTests.test_core_utils

    doctest init:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = \
    ...    'lino_book.projects.docs.settings.doctests'
    >>> from lino.api.doctest import *

Get installed models which are subclass of a something
======================================================

The :func:`lino.core.utils.models_by_base` function returns a list of
models which are subclass of a given class.

>>> from lino.mixins.duplicable import Duplicable
>>> rt.models_by_base(Duplicable)
[<class 'lino_xl.lib.countries.models.Place'>, <class 'lino_xl.lib.polls.models.Choice'>, <class 'lino_xl.lib.polls.models.Question'>]

>>> rt.models_by_base(rt.models.contacts.Partner)
[<class 'lino_xl.lib.contacts.models.Company'>, <class 'lino_xl.lib.contacts.models.Partner'>, <class 'lino_xl.lib.contacts.models.Person'>]

>>> rt.models_by_base(rt.models.contacts.Person)
[<class 'lino_xl.lib.contacts.models.Person'>]

.. rubric:: Getting only top-level models

The `toplevel_only` option is used by
:mod:`lino.modlib.checkdata`. For example the
:class:`AddressOwnerChecker
<lino.modlib.addresses.mixins.AddressOwnerChecker>` needs to run only on
Partner, not also on Person, Company and Household...

>>> rt.models_by_base(rt.models.contacts.Partner, toplevel_only=True)
[<class 'lino_xl.lib.contacts.models.Partner'>]

>>> rt.models_by_base(rt.models.contacts.Person, toplevel_only=True)
[<class 'lino_xl.lib.contacts.models.Person'>]

