.. _lino.tested.cv:

==================================
Career module (tested)
==================================


.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_cv
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_book.projects.max.settings.demo')
    >>> from lino.api.doctest import *

.. contents:: 
   :local:
   :depth: 2


>>> UserTypes = rt.modules.users.UserTypes
>>> AllLanguageKnowledges = rt.modules.cv.AllLanguageKnowledges

>>> rt.show(UserTypes)
======= =========== ===============
 value   name        text
------- ----------- ---------------
 000     anonymous   Anonymous
 100     user        User
 900     admin       Administrator
======= =========== ===============
<BLANKLINE>

>>> a = UserTypes.admin
>>> a
users.UserTypes.admin:900

>>> u = UserTypes.user
>>> u
users.UserTypes.user:100

>>> AllLanguageKnowledges.required_roles
set([<class 'lino_xl.lib.cv.roles.CareerStaff'>])

>>> AllLanguageKnowledges.default_action.get_view_permission(u)
False

>>> AllLanguageKnowledges.default_action.get_view_permission(a)
False
