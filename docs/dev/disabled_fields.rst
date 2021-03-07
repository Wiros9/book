.. doctest docs/dev/disabled_fields.rst
.. _disabled_fields:

====================================
Controlling whether data is editable
====================================

Disabling individual fields
===========================

.. currentmodule:: lino.core.model

Sometimes you want to disable (make non-editable) individual fields of a form
based on certain conditions.  The conditions for disabling individual fields can
be application specific and based e.g. on user roles or the values of certain
other fields of the object being displayed.

For example, in :ref:`cosi` an invoice disables most fields when it has been
registered.  Here are two screenshots of a same invoice, once when the invoice's
state is "draft" and once when it is "registered":

.. image:: /specs/cosi/sales.Invoice.detail.draft.png
    :scale: 20

.. image:: /specs/cosi/sales.Invoice.detail.registered.png
    :scale: 20

In Lino you define this behaviour by overriding the :meth:`disabled_fields
<lino.core.model.Model.disabled_fields>` instance method on your model.

.. class:: Model
  :noindex:

  .. method:: disabled_fields(self, ar)

    Return a set of field names that should be *disabled* (i.e. not editable)
    for this :term:`database object`.

Here is a fictive example::

    class MyModel(dd.Model):
        ...
        def disabled_fields(self, ar):
            s = super(MyModel, self).disabled_fields(ar)
            ...
            return set()

The :class:`Invoice` model used in above screenshots does something
like this::

    class Invoice(dd.Model):
      ...
      def disabled_fields(self, ar):
          df = super(Invoice, self).disabled_fields(ar)
          if self.state == InvoiceStates.registered:
              df.add('subject')
              df.add('payment_term')
              ...
          return df

The decision which fields to disable may depend an the current user. Here is a
fictive example of a model :class:`Case` where only the author may change first
and last name::

    class Case(dd.Model):
      ...
      def disabled_fields(self, ar):
          df = super(Case, self).disabled_fields(ar)
          if self.author == ar.user:
              return df
          df.add('first_name')
          df.add('last_name')
          return df


You may also disable *actions* simply by adding their name to the set of
disabled fields. (The method name :meth:`disabled_fields` is actually
misleading, one day we might rename it to :meth:`disabled_elements`).

You may want to override this method on the actor instead of per model. In that
case it must be a `classmethod` with two arguments `obj` and `ar`::

  @classmethod
  def disabled_fields(cls, obj, ar):
      s = super(MyActor, cls).disabled_fields(obj, ar)
      ...
      return set()

Note that Lino calls the :meth:`disabled_fields <Model.disabled_fields>` method
only once per :term:`database row` and request.  The returned set is cached in
memory.


Disable editing of a whole table
================================

.. class:: lino.core.actors.Actor
  :noindex:

  .. attribute:: editable

    Set this explicitly to `True` or `False` to make the whole table
    editable or not.  Otherwise Lino will guess what you want during
    startup and set it to `False` if the actor is a Table and has a
    `get_data_rows` method (which usually means that it is a virtual
    table), otherwise to `True`.

    Non-editable actors won't even call :meth:`get_view_permission`
    for actions whose :attr:`readonly
    <lino.core.actions.Action.readonly>` is `False`.

The :class:`changes.Changes <lino.modlib.changes.Changes>` table is an example
where this is being used: nobody should ever edit something in the table of
Changes.  The user interface uses this to generate optimized JS code for this
case.
