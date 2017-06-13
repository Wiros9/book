.. _dev.choicelists:

===========================
Introduction to choicelists
===========================

.. To run only this test:

   $ python setup.py test -s tests.DocsTests.test_choicelists

A :class:`ChoiceList <lino.core.choicelists.ChoiceList>` is a
"constant"[#constant]_ ordered list of translatable values.

Wherever in a *plain Django* application you use a `choices` attribute
on a database field, in a *Lino* application you should consider using
a :class:`ChoiceList <lino.core.choicelists.ChoiceList>` instead.

..
    >>> from lino import startup
    >>> startup('lino_book.projects.docs.settings.doctests')
    >>> from lino.api.doctest import *
    

ChoiceLists are **actors**.  They are globally accessible in
:data:`rt.modules` using their *app label* and their name.

For example the :class:`Genders <lino.modlib.system.choicelists.Genders>`
choicelist is part of the :mod:`lino.modlib.system` plugin, so its
*app label* is ``system``:

>>> rt.modules.system.Genders
lino.modlib.system.choicelists.Genders

Like every Actor, ChoiceLists are **never instantiated**. They are
just the class object itself:

>>> from lino.modlib.system.choicelists import Genders
>>> Genders is rt.modules.system.Genders
True


ChoiceLists are tables
======================

ChoiceLists are tables. You can display them using :meth:`show
<lino.core.requests.BaseRequest.show>`:

>>> rt.show(rt.modules.system.Genders)
======= ======== ========
 value   name     text
------- -------- --------
 M       male     Male
 F       female   Female
======= ======== ========
<BLANKLINE>

The text of a choice is a **translatable** string, while *value* and
*name* remain **unchanged**:

>>> with translation.override('de'):
...     rt.show(rt.modules.system.Genders)
====== ======== ==========
 Wert   name     Text
------ -------- ----------
 M      male     Männlich
 F      female   Weiblich
====== ======== ==========
<BLANKLINE>



Accessing individual choices
============================

Each row of a choicelist is a choice. Individual choices can have a
**name**, which makes them accessible as **class attributes** on the
**choicelist** which own them:

>>> Genders.male
<Genders.male:M>

>>> Genders.female
<Genders.female:F>

Here is how to select all men:

>>> list(rt.modules.contacts.Person.objects.filter(gender=Genders.male))
... # doctest: +ELLIPSIS
[Person #114 ('Mr Hans Altenberg'), Person #112 ('Mr Andreas Arens'), ...]


A ChoiceList has an `objects` method (not attribute) which returns an
iterator over its choices:

>>> print(Genders.objects())
[<Genders.male:M>, <Genders.female:F>]

Each Choice has a "value", a "name" and a "text". 

The **value** is what gets stored when this choice is assigned to a
database field.

>>> [g.value for g in Genders.objects()]
[u'M', u'F']

The **name** is how Python code can refer to this choice.

>>> [g.name for g in Genders.objects()]
[u'male', u'female']

>>> print(repr(Genders.male))
<Genders.male:M>

The **text** is what the user sees.  It is a translatable string,
implemented using Django's i18n machine:

>>> Genders.male.text.__class__
<class 'django.utils.functional.__proxy__'>

Calling `unicode` of a choice is (usually) the same as calling unicode
on its `text` attribute:

>>> rmu([str(g) for g in Genders.objects()])
['Male', 'Female']

The text of a choice depends on the current user language.

>>> from django.utils import translation
>>> with translation.override('fr'):
...     rmu([unicode(g) for g in Genders.objects()])
['Masculin', 'F\xe9minin']

>>> with translation.override('de'):
...     [unicode(g) for g in Genders.objects()]
['M\xe4nnlich', 'Weiblich']

>>> with translation.override('et'):
...     [unicode(g) for g in Genders.objects()]
['Mees', 'Naine']


Comparing Choices uses their *value* (not the *name* nor *text*):

>>> UserTypes = rt.modules.auth.UserTypes

>>> UserTypes.admin > UserTypes.user
True
>>> UserTypes.admin == '900'
True
>>> UserTypes.admin == 'manager'
False
>>> UserTypes.admin == ''
False





.. rubric:: Footnotes

.. [#constant] We put "constant" between quotation marks because of course it may
  vary. But if it does so, then only once at server startup.



