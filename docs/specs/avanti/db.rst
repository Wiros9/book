.. doctest docs/specs/avanti/db.rst
.. _avanti.specs.db:

=================================
Database structure of Lino Avanti
=================================

.. doctest init:

    >>> import lino
    >>> lino.startup('lino_book.projects.avanti1.settings')
    >>> from lino.api.doctest import *

This document describes the database structure.

.. contents::
  :local:


Complexity factors
==================


>>> print(analyzer.show_complexity_factors())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF -SKIP
- 40 plugins
- 81 models
- 8 user types
- 304 views
- 18 dialog actions
<BLANKLINE>

The database models
===================


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF +SKIP
