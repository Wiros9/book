.. _tested_docs:
.. _dev.doctest:

================
Doctests in Lino
================

.. glossary::

  tested document

    A documentation page that contain blocks of Python code marked by a ``>>>``
    in the beginning of each line, and which is getting tested using Python's
    `doctest <https://docs.python.org/3/library/doctest.html>`__ command as part
    of a test suite.

The :cmd:`doctest` command extracts code snippets from any text file, executes
them checks whether their output is the same as the one displayed in the
document.

When you want to use :cmd:`doctest` for testing Django code, you need to specify
a :term:`Django settings module`. Here is an example of how you do that:

>>> import lino
>>> lino.startup('lino_book.projects.min1.settings')
>>> from lino.api.doctest import *

Yes, this is one of the important reasons why we have :term:`demo projects <demo
project>`.  The :ref:`book` repository contains over 1000 documents, and many of
them (actually about 176) contain doctest snippets.

Most tested documents use the database of some :term:`demo project`. When your
:doc:`developer environment is installed </dev/install/index>`, you can re-play
the instructions on such pages interactively in a Django :manage:`shell` session
on the project they use.

They require of course that the :term:`demo project` has been populated
previously by :cmd:`inv prep`, not on a temporary test database as the Django
test runner creates it.

The advantage of this method (compared to using the Django test runner) is that
they don't need to populate the database (load the demo fixtures) for each test
run. A limitation of this method is of course that they may not modify the
database. That's why we sometimes call them static or passive. They just observe
whether everything looks as expected.  When you want to test something that
modifies the database, you don't write a tested document but a Django test case.


.. xfile:: test_docs.py

The test suite of a repository with tested documents has a file
:xfile:`test_docs.py` in its :file:`tests` directory, which calls
:func:`atelier.test.make_docs_suite` to automatically create a unit test for
every document in the doctree. A simple :xfile:`test_docs.py` file looks like
this::

  from atelier.test import make_docs_suite

  def load_tests(loader, standard_tests, pattern):
      suite = make_docs_suite("docs")
      return suite

The initialization code usually imports and calls :func:`lino.startup`, then
imports everything (``*``) from  the :mod:`lino.api.doctest` module (which
contains a selection of the most frequently used commands used in doctests).

See also:

- :mod:`atelier.test`
- :mod:`lino.utils.pythontest` and :mod:`lino.utils.djangotest`
- :mod:`lino.utils.test`
