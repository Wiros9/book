.. doctest docs/dev/create.rst

=================================
Customizing how data is created
=================================

There are many ways to customize how to insert rows into the database.

.. currentmodule:: lino.core.model

.. class:: Model
  :noindex:

  .. method:: on_create(self)

    Override this to set default values that depend on the request.

    The difference with Django's `pre_init
    <https://docs.djangoproject.com/en/1.11/ref/signals/#pre-init>`__
    and `post_init
    <https://docs.djangoproject.com/en/1.11/ref/signals/#post-init>`__
    signals is that (1) you override the method instead of binding
    a signal and (2) you get the action request as argument.

    Used e.g. by :class:`lino_xl.lib.notes.Note`.

  .. method:: after_ui_create(self, ar)

    Hook to define custom behaviour to run when a user has created a new instance
    of this model.


  .. attribute:: submit_insert

    The :class:`SubmitInsert <lino.core.actions.SubmitInsert>` action to be
    executed when the when the users submits an insert window.

    See :mod:`lino.mixins.dupable` for an example of how to override it.

  .. method:: create_from_choice(cls, text)

    Called when a learning combo has been submitted.
    Create a persistent database object if the given text contains enough information.

  .. method:: choice_text_to_dict(cls, text)

    Return a dict of the fields to fill when the given text contains enough
    information for creating a new database object.


.. class:: lino.core.actors.Actor
  :noindex:


  .. attribute:: allow_create = True

    If this is False, the table won't have any insert_action.


  .. method:: get_create_permission(self, ar)

    Dynamic test per request.  

    This is being called only when :attr:`allow_create` is True.
