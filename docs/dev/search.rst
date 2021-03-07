.. doctest docs/dev/search.rst

=================================
Customizing how data is searched
=================================

There are many ways to customize how users can search for data.

.. currentmodule:: lino.core.model

.. class:: Model
  :noindex:

  .. attribute:: show_in_site_search = True

    Set this to `False` if you don't want this model to occur
    in the site-wide search (:class:`lino.modlib.about.SiteSearch`).

  .. attribute:: quick_search_fields = None

    Explicitly specify the fields to be included in queries with a
    quick search value.

    In your model declarations this should be either `None` or a
    `string` containing a space-separated list of field names.  During
    site startup resolves it into a tuple of data elements.

    If it is `None`, Lino installs a list of all CharFields on the
    model.

    If you want to not inherit this field from a parent using standard
    MRO, then you must set that field explicitly to `None`.

    This is also used when a gridfilter has been set on a foreign key
    column which points to this model.

    **Special quick search strings**

    If the search string starts with "#", then Lino searches for a row
    with that *primary key*.

    If the search string starts with "*", then Lino searches for a row
    with that *reference*.

  .. attribute:: quick_search_fields_digit = None

    Same as :attr:`quick_search_fields`, but this list is used when the
    search text contains only digits (and does not start with '0').
