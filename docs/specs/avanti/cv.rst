.. doctest docs/specs/avanti/cv.rst
.. _avanti.specs.cv:

=================================
CV functions in Lino Avanti
=================================

This document describes how standard CV functionality is being extended by
:ref:`avanti`.


.. contents::
  :local:


.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_book.projects.avanti1.settings')
>>> from lino.api.doctest import *


Lino Avanti defines a plugin :mod:`lino_avanti.lib.cv`  which inherits from
:mod:`lino_xl.lib.cv`.


.. currentmodule:: lino_avanti.lib.cv

.. class:: Study

    .. attribute:: foreign_education_level



    .. attribute:: recognized

      Whether this study is recognized in Belgium.
