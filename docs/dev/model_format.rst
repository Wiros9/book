.. doctest docs/dev/model_format.rst

=================================
Customizing how data is formatted
=================================


.. currentmodule:: lino.core.model

.. class:: Model
  :noindex:

  .. method::


.. class:: lino.core.actors.Actor
  :noindex:

  .. attribute:: label

    The text to appear e.g. on a button that will call the default
    action of an actor.  This attribute is *not* inherited to
    subclasses.  For :class:`Actor` subclasses that don't have a
    label, Lino will call :meth:`get_actor_label`.

  .. classmethod:: get_row_classes(self, ar)

    If a method of this name is defined on an actor, then it must
    be a class method which takes an :class:`ar
    <lino.core.requests.BaseRequest>` as single argument and
    returns either None or a string "red", "green" or "blue"
    (todo: add more colors and styles). Example::

        @classmethod
        def get_row_classes(cls,obj,ar):
            if obj.client_state == ClientStates.newcomer:
                return 'green'

    Defining this method will cause an additional special
    `RowClassStoreField` field in the :class:`lino.core.Store`
    objects of this actor.

  .. attribute:: details_of_master_template = _("%(details)s of %(master)s")

    Used to build the title of a request on this table when it is a
    slave table (i.e. :attr:`master` is not None). The default value
    is defined as follows::

        details_of_master_template = _("%(details)s of %(master)s")
