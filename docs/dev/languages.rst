.. doctest docs/dev/languages.rst

============================
The languages of a Lino site
============================

The :attr:`languages <lino.core.site.Site.languages>` attribute in the
:xfile:`settings.py` file of a :term:`Lino site` specifies what we call the
:term:`language distribution`.

The :term:`language distribution` controls two things: (1) the :term:`front end`
languages available on this site and (2) how multilingual database content is
stored in your database.

Every site user may chose one of these languages in their preferences.

The :term:`site maintainer` can change the language distribution with the
:attr:`Site.language` attribute in the :xfile:`settings.py` file.


.. glossary::

  language distribution

    The list of languages that are activated on a given :term:`Lino site`.

  language code

    A code that identifies a language for which screen messages have been
    translated.

    Lino uses the same language codes as Django. You can see the list of
    available languages in `django/conf/global_settings.py
    <https://github.com/django/django/blob/master/django/conf/global_settings.py>`__.

    You may use any of these languages, but Lino-specific messages are currently
    translated only into German, French, Estonian and Dutch.  You are welcome to
    contribute translations to your language of choice. See
    :doc:`/dev/translate/index`.

Having more than one language in your :term:`language distribution` will make
your Lino site **multilingual**. Changing this setting may change your database
structure and thus might require a :ref:`data migration <datamig>`. This is
because this setting also controls how multilingual database content is stored
in your database. See :ref:`mldbc`.


>>> import lino
>>> lino.startup('lino.projects.std.settings_test')


Developer reference
===================

.. currentmodule:: lino.core.site

.. class:: Site
  :noindex:

  .. attribute:: languages = None

    The :term:`language distribution` to be used on this site.

    This must be either `None`, or an iterable of :term:`language codes
    <language code>`, or a string containing a space-separated series of
    language codes.

    Examples::

      languages = "en de fr nl et"
      languages = ['en', 'fr']
      languages = 'en'

    The first language in this list is the site's default language,
    returned by :meth:`get_default_language`.

  .. attribute:: hidden_languages = None

    A string with a space-separated list of :term:`language codes <language
    code>` that should be hidden. This is useful when you have multilingual
    database content and a :term:`language distribution` of more than three
    languages.


>>> from django.utils import translation
>>> from lino.core.site import TestSite as Site
>>> import json
>>> from pprint import pprint


Application code usually specifies :attr:`Site.languages` as a single
string with a space-separated list of language codes.  The
:class:`Site` will analyze this string during instantiation and
convert it into a tuple of :data:`LanguageInfo` objects.

The following examples use the :class:`TestSite` class just to show certain
things that apply also to "real" Sites.

>>> SITE = Site(languages="en fr de")
>>> print(SITE.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='en', name='en', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de', name='de', index=2, suffix='_de'))

>>> SITE = Site(languages="de-ch de-be")
>>> print(SITE.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='de-ch', name='de_CH', index=0, suffix=''), LanguageInfo(django_code='de-be', name='de_BE', index=1, suffix='_de_BE'))

If we have more than one locale of a same language *on a same Site*
(e.g. 'en-us' and 'en-gb') then it is not allowed to specify just
'en'.  But otherwise it is allowed to just say "en", which will mean
"the English variant used on this Site".

>>> site = Site(languages="en-us fr de-be de")
>>> print(site.languages)  #doctest: +NORMALIZE_WHITESPACE
(LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
 LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr'),
 LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE'),
 LanguageInfo(django_code='de', name='de', index=3, suffix='_de'))

>>> pprint(site.language_dict)
{'de': LanguageInfo(django_code='de', name='de', index=3, suffix='_de'),
 'de_BE': LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE'),
 'en': LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
 'en_US': LanguageInfo(django_code='en-us', name='en_US', index=0, suffix=''),
 'fr': LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')}

>>> site.language_dict['de']
LanguageInfo(django_code='de', name='de', index=3, suffix='_de')

>>> site.language_dict['de_BE']
LanguageInfo(django_code='de-be', name='de_BE', index=2, suffix='_de_BE')

>>> site.language_dict['de'] == site.language_dict['de_BE']
False

>>> site.language_dict['en'] == site.language_dict['en_US']
True

>>> site.language_dict['en']
LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')
>>> site.language_dict['en']
LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')

>>> site.language_dict['fr']
LanguageInfo(django_code='fr', name='fr', index=1, suffix='_fr')

>>> pprint(site.django_settings['LANGUAGES'])  #doctest: +ELLIPSIS
[('de', 'German'), ('fr', 'French')]

Note that Lino automatically sets :setting:`USE_L10N` to `True` when you specify
:attr:`languages <lino.core.site.Site.languages>`.

>>> site.django_settings['USE_L10N']
True
>>> pprint(site.django_settings['LANGUAGE_CODE'])
'en-us'

When you leave :attr:`languages <lino.core.site.Site.languages>` at its default
value `None`, Lino will set the default language "en" at startup. But there is a
difference between `None` and "en": `None` will cause :setting:`USE_L10N` to be
False because this is what we want when we don't worry about languages.

Lino's default language is "en" and not "en-us" because Django has no entry in
:setting:`LANGUAGES` for this language code, and because we also reduce the
:setting:`LANGUAGES` setting to the languages that are needed. Django 3.0.3
system check complained with "(translation.E004) You have provided a value for
the LANGUAGE_CODE setting that is not in the LANGUAGES setting."

>>> site = Site()
>>> print(site.languages)
(LanguageInfo(django_code='en', name='en', index=0, suffix=''),)
>>> pprint(site.django_settings['LANGUAGES'])
[('en', 'English')]

>>> 'USE_L10N' in site.django_settings
False

>>> 'LANGUAGE_CODE' in site.django_settings
False



API documentation
=================

The :setting:`SITE` object contains other information about the language
distribution.

.. class:: Site
  :noindex:

  .. method:: get_default_language(self)

      The django code of the default language to use in every
      :class:`lino.utils.mldbc.fields.LanguageField`.


  .. attribute:: LANGUAGE_CHOICES

    A tuple in the format expected by Django's :attr:`Field.choices
    <django.models.fields.Field.choices>` attribute, used e.g. by
    :class:`LanguageField <lino.utils.mldbc.fields.LanguageField>`. Its
    content is automatically populated from :attr:`languages` and
    application code should not change its value.

  .. method:: get_language_info(self, code)

    Use this in Python fixtures or tests to test whether a Site
    instance supports a given language.  `code` must be a
    Django-style language code.

    On a site with only one locale of a language (and optionally
    some other languages), you can use only the language code to
    get a tuple of :data:`LanguageInfo` objects.

    >>> from lino.core.site import TestSite as Site
    >>> Site(languages="en-us fr de-be de").get_language_info('en')
    LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')

    On a site with two locales of a same language (e.g. 'en-us'
    and 'en-gb'), the simple code 'en' yields that first variant:

    >>> site = Site(languages="en-us en-gb")
    >>> print(site.get_language_info('en'))
    LanguageInfo(django_code='en-us', name='en_US', index=0, suffix='')


  .. method:: resolve_languages(self, languages)

    This is used by `UserType`.

    Examples:

    >>> from lino.core.site import TestSite as Site
    >>> lst = Site(languages="en fr de nl et pt").resolve_languages('en fr')
    >>> [i.name for i in lst]
    ['en', 'fr']

    You may not specify languages that don't exist on this site:

    >>> Site(languages="en fr de").resolve_languages('en nl')
    Traceback (most recent call last):
    ...
    Exception: Unknown language code 'nl' (must be one of ['en', 'fr', 'de'])


  .. method:: str2kw(self, name, txt,  **kw)

    Return a dictionary that maps the internal field names for
    babelfield `name` to their respective translation of the given
    lazy translatable string `txt`.

    >>> from django.utils.translation import gettext_lazy as _
    >>> from lino.core.site import TestSite as Site
    >>> site = Site(languages='de fr es')
    >>> site.str2kw('name', _("January")) == {'name_fr': 'janvier', 'name': 'Januar', 'name_es': 'Enero'}
    True
    >>> site = Site(languages='fr de es')
    >>> site.str2kw('name', _("January")) == {'name_de': 'Januar', 'name': 'janvier', 'name_es': 'Enero'}
    True

  .. method:: babelkw(self, name, **kw)

    Return a dict with appropriate resolved field names for a
    BabelField `name` and a set of hard-coded values.

    This function is no longer recommended to use for application code. When
    some application code uses::

      babelkw("fieldname", en="foo", de="Foo", fr="Phou", ...)

    this code should be replaced by::

      str2kw(_("foo"))

    and after this change you must run :cmd:`inv mm`, which will add `"foo"` as
    a translatable string to the :xfile:`.po` files. And then you must use
    poedit to add the formerly hard-coded translations ("Foo" for `de` and
    "Phou" for `fr`) in the the :xfile:`.po` files.

    But this function is still being used in Python fixtures (where it makes
    sense).

    You have some hard-coded multilingual content in a fixture:
    >>> from lino.core.site import TestSite as Site
    >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

    The field names where this info gets stored depends on the
    Site's `languages` distribution.

    >>> Site(languages="de-be en").babelkw('name',**kw) == {'name_en': 'Hello', 'name': 'Hallo'}
    True

    >>> Site(languages="en de-be").babelkw('name',**kw) == {'name_de_BE': 'Hallo', 'name': 'Hello'}
    True

    >>> Site(languages="en-gb de").babelkw('name',**kw) == {'name_de': 'Hallo', 'name': 'Hello'}
    True

    >>> Site(languages="en").babelkw('name',**kw) == {'name': 'Hello'}
    True

    >>> Site(languages="de-be en").babelkw('name',de="Hallo",en="Hello") == {'name_en': 'Hello', 'name': 'Hallo'}
    True

    In the following example `babelkw` attributes the
    keyword `de` to the *first* language variant:

    >>> Site(languages="de-ch de-be").babelkw('name',**kw) == {'name': 'Hallo'}
    True


  .. method:: args2kw(self, name, *args)

    Takes the basename of a BabelField and the values for each language.
    Returns a `dict` mapping the actual fieldnames to their values.

  .. method:: field2kw(self, obj, name, **known_values)

    Return a `dict` with all values of the BabelField `name` in the
    given object `obj`. The dict will have one key for each
    :attr:`languages`.

    Examples:

    >>> from lino.core.site import TestSite as Site
    >>> from lino.utils import AttrDict
    >>> def testit(site_languages):
    ...     site = Site(languages=site_languages)
    ...     obj = AttrDict(site.babelkw(
    ...         'name', de="Hallo", en="Hello", fr="Salut"))
    ...     return site,obj


    >>> site, obj = testit('de en')
    >>> site.field2kw(obj, 'name') == {'de': 'Hallo', 'en': 'Hello'}
    True

    >>> site, obj = testit('fr et')
    >>> site.field2kw(obj, 'name') == {'fr': 'Salut'}
    True

  .. method:: field2args(self, obj, name)

    Return a list of the babel values of this field in the order of
    this Site's :attr:`Site.languages` attribute.

  .. method:: babelitem(self, *args, **values)

    Given a dictionary with babel values, return the
    value corresponding to the current language.

    This is available in templates as a function `tr`.

    >>> kw = dict(de="Hallo", en="Hello", fr="Salut")

    >>> from lino.core.site import TestSite as Site
    >>> from django.utils import translation

    A Site with default language "de":

    >>> site = Site(languages="de en")
    >>> tr = site.babelitem
    >>> with translation.override('de'):
    ...    print(tr(**kw))
    Hallo

    >>> with translation.override('en'):
    ...    print(tr(**kw))
    Hello

    If the current language is not found in the specified `values`,
    then it returns the site's default language:

    >>> with translation.override('jp'):
    ...    print(tr(en="Hello", de="Hallo", fr="Salut"))
    Hallo

    Testing detail: default language should be "de" in our example, but
    we are playing here with more than one Site instance while Django
    knows only one "default language" which is the one specified in
    `lino.projects.docs.settings`.

    Another way is to specify an explicit default value using a
    positional argument. In that case the language's default language
    doesn'n matter:

    >>> with translation.override('jp'):
    ...    print(tr("Tere", de="Hallo", fr="Salut"))
    Tere

    >>> with translation.override('de'):
    ...     print(tr("Tere", de="Hallo", fr="Salut"))
    Hallo

    You may not specify more than one default value:

    >>> tr("Hello", "Hallo")
    Traceback (most recent call last):
    ...
    ValueError: ('Hello', 'Hallo') is more than 1 default value.


  .. method:: babelattr(self, obj, attrname, default=NOT_PROVIDED, language=None)

    Return the value of the specified babel field `attrname` of `obj` in the
    current language.

    This is to be used in multilingual document templates.  For example in a
    document template of a contract you may use the following expression::

      babelattr(self.type, 'name')

    This will return the correct value for the current language.

    Examples:

    >>> from __future__ import unicode_literals
    >>> from django.utils import translation
    >>> from lino.core.site import TestSite as Site
    >>> from lino.utils import AttrDict
    >>> def testit(site_languages):
    ...     site = Site(languages=site_languages)
    ...     obj = AttrDict(site.babelkw(
    ...         'name', de="Hallo", en="Hello", fr="Salut"))
    ...     return site, obj


    >>> site,obj = testit('de en')
    >>> with translation.override('de'):
    ...     print(site.babelattr(obj,'name'))
    Hallo

    >>> with translation.override('en'):
    ...     print(site.babelattr(obj,'name'))
    Hello

    If the object has no translation for a given language, return
    the site's default language.  Two possible cases:

    The language exists on the site, but the object has no
    translation for it:

    >>> site,obj = testit('en es')
    >>> with translation.override('es'):
    ...     print(site.babelattr(obj, 'name'))
    Hello

    Or a language has been activated which doesn't exist on the site:

    >>> with translation.override('fr'):
    ...     print(site.babelattr(obj, 'name'))
    Hello




.. class:: LanguageInfo

  A named tuple with four fields:

  .. attribute:: django_code

    How Django calls this language

  .. attribute:: name

    How Lino calls it

  .. attribute:: index

    The position in the :attr:`Site.languages` tuple

  .. attribute:: suffix

    The suffix to append to babel fields for this language
