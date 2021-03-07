.. _dev.translate:

============================
Instructions for translators
============================

Here is how your can help translating Lino into your own language.

Before starting to translate, you must have :doc:`installed a contributor
environment </team/install/index>` of Lino.

Overview
--------

You are going to edit a series of :xfile:`.po` files which are part of the Lino
source code.  Each Lino repository has its own series of :xfile:`.po` files.
Their place is given by the :attr:`locale_dir` setting (see
:ref:`atelier.prjconf`). Here are some examples:

- :mod:`lino` : lino/locale
- :mod:`lino_xl` : lino_xl/lib/xl/locale
- :mod:`lino_noi` : lino_noi/lib/noi/locale
- :mod:`lino_cosi` : lino_cosi/lib/cosi/locale
- etc.

To edit these :xfile:`.po` files you can use either your preferred :doc:`text
editor </dev/newbies/editor>` or a tool like Poedit_.  We recommend the latter.
On Debian you install it with :cmd:`apt-get install poedit`.

.. _Poedit: http://www.poedit.net


Adding support for a new language to translate
----------------------------------------------

Before you can start translating to a language, you must check whether the
repository already has translation files for your language.

If you want to translate to a language for which Lino does not yet have any
translations,

Every repository has a list of languages for which it provides translations.
This list is in the :envvar:`languages` parameter in the repository's
:xfile:`tasks.py` file. You can add your language there.

Lino uses the same language codes as Django.
You can see the list of available languages in
`django/conf/global_settings.py
<https://github.com/django/django/blob/master/django/conf/global_settings.py>`__.

After adding a language, you must run :cmd:`inv mm`, which will ask your
configuration before creating the new catalog files.


Set up a site
-------------

Let's say for example that you want to translate to *Spanish*.

Don't simply translate all the messages in the :xfile:`django.po` files because

- some translations depend on the context. It's better that you
  see where a message is being used before you decide how to translate it.

- you won't need to translate *all* the messages. It's more efficient to focus
  on the most important ones.

That's why we recommend that you use a demo project to see your work while you are
evolving.

Go to some local project directory (e.g. the one you created in
:ref:`dev.install`)::

  $ go first

Change your project's :xfile:`settings.py` file once more so that it
looks as follows:

.. literalinclude:: settings.py

That is, you specify your own language distribution (in the
:attr:`lino.core.site.Site.languages` setting) consisting of English as first
language and Spanish (your language) as second. The first language cannot
currently be your language because some demo fixtures would fail
(:srcref:`docs/tickets/108`).

If your language is not yet covered for Lino, then you must `Create a demo user
for your language`_ before going on.

Initialize the demo database::

  $ python manage.py prep

Run the development server::

  $ python manage.py runserver

Point your browser to view the application. Log in as the Spanish user.

.. image:: translate_1.png
  :scale: 80

Find the strings that you want to translate
-------------------------------------------

The translatable strings on this page (`gettext` and Poedit_ call them
"messages") are for example the menu labels ("Contacts", "Products" etc), but
also content texts like "Welcome", "Hi, Rodrigo!" or "This is a Lino demo site."

Now you must find out which :xfile:`django.po` file contains these strings. Open
another terminal window and use :command:`grep` to find the file::

  $ grep -H Contacts ~/repositories/lino/lino/locale/es/LC_MESSAGES/*.po
  /home/repositories/work/lino/lino/locale/es/LC_MESSAGES/django.po:#~ msgid "Contacts"
  $ grep -H Contacts ~/repositories/xl/lino_xl/lib/xl/locale/es/LC_MESSAGES/*.po
  /home/luc/repositories/xl/lino_xl/lib/xl/locale/es/LC_MESSAGES/django.po:msgid "Contacts"
  /home/luc/repositories/xl/lino_xl/lib/xl/locale/es/LC_MESSAGES/django.po:msgid "Client Contacts"
  /home/luc/repositories/xl/lino_xl/lib/xl/locale/es/LC_MESSAGES/django.po:#~ msgid "Contacts"


Translate
---------

Launch Poedit_ on the :xfile:`django.po` file for the Spanish translation::

  $ poedit lino/locale/es/LC_MESSAGES/django.po

It looks similar to this screenshot:

.. image:: poedit_es_1.png
  :scale: 60

Translate one or a few messages. In our example we translated the following
message::

  Hi, %(first_name)s!

into::

  ¡Hola, %(first_name)s!

Save your work in Poedit_.  Poedit will automatically compile the
:xfile:`django.po` file into a corresponding :file:`django.mo` file.

Now you should first `touch` your `settings.py` file in order to tell runserver
that something has changed. Open a third terminal window and type::

  $ go first
  $ touch settings.py

This will cause the server process (which is running in the first terminal
window) to reload and to rewrite any cache files.

Refresh your browser page:

.. image:: cosi_es_hola.png
  :scale: 80

Submit your work
---------------------

When you are satisfied with your work, you must make a pull request to ask us to
integrate your changes into the public Lino repositories.

More about pull requests in :doc:`/dev/git`.


Create a demo user for your language
------------------------------------

If Lino does not yet have a default site administrator user for your language
(:mod:`lino.modlib.users.fixtures.demo`), then :cmd:`pm prep` will say a
warning::

  No demo user for language 'bn'.

This means that you should create a local fixture that creates it.  It's easy::

  $ mkdir fixtures
  $ touch fixtures/__init__.py
  $ nano fixtures/demo.py

The :file:`demo.py` file should look as follows:

.. literalinclude:: fixtures/demo.py



Trucs et astuces
----------------

Voici un pitfall: la traduction du string suivant::

  msgid "%(person)s has been unregistered from %(course)s"

ne doit pas être::

  msgstr "%(personne)s a été désinscrit du %(cours)"

mais bien::

  msgstr "%(person)s a été désinscrit du %(course)s"

C.-à-d. les mots-clés entre parenthèses sont des variables,
et il *ne faut pas* les modifier.

À noter également que le ``s`` derrière la parenthèse ne sera pas
imprimé mais est obligatoire
(il indique à Python qu'il s'agit d'un remplacement de type `string`).
