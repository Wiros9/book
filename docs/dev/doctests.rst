.. _tested_docs:
.. _dev.doctest:

================
Doctests in Lino
================

**Tested documents** are pages that contain blocks of Python code marked by a
``>>>`` in the beginning of each line.
They are part of the Lino test suite and have been tested using Python's
`doctest <https://docs.python.org/3/library/doctest.html>`__ command.

When your :doc:`developer environment is installed </dev/install/index>`, you
can re-play the instructions on such pages in the demo project, either
interactively in a Django :manage:`shell` session or by writing a script and run
it using :manage:`run`.

They run on a :term:`demo project` which has been populated by :cmd:`inv prep`,
not on a temporary test database as the Django test runner creates it.

The advantage of this method (compared to Django tests) is that they access the existing demo database and
thus don't need to populate it (load the demo fixtures) for each test run. A
limitation of this method is of course that they may not modify the database.
That's why we sometimes call them static or passive. They just observe whether
everything looks as expected.

They are tested using the :cmd:`doctest` command, which extracts code snippets
from any text file, runs them in a subprocess and then checks whether their
output is the same as the one displayed in the document.

.. xfile:: test_docs.py

The test suite of a repository with tested documents has a file
:xfile:`test_docs.py` in its :file:`tests` directory, which calls
:func:`atelier.test.make_docs_suite` to automatically create a unit test for
every document in the doctree. A simple :xfile:`test_docs.py` file looks like
this::

  from atelier.test import make_docs_suite

  def load_tests(loader, standard_tests, pattern):
      suite = make_docs_suite(
          "docs", addenv=dict(LINO_LOGLEVEL="INFO"))
      return suite


The initialization code usually imports and calls :func:`lino.startup`, then
imports everything (``*``) from  the :mod:`lino.api.doctest` module (which
contains a selection of the most frequently used commands used in doctests).

See also:

- :mod:`atelier.test`
- :mod:`lino.utils.pythontest` and :mod:`lino.utils.djangotest`
- :mod:`lino.utils.test`
