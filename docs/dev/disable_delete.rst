.. doctest docs/dev/disable_delete.rst
.. _lino.tested.ddh:

=============================
Controlling delete behaviour
=============================

.. currentmodule:: lino.core.model

The ``disable_delete`` method
=============================

When a user has view and write permission to an actor, they usually also have
permission to delete individual :term:`database rows <database row>` using the
|delete| button in the toolbar.  But before actually deleting a row, Lino will
call the :meth:`disable_delete <Model.disable_delete>` method do decide whether
the action will actually run.

.. class:: Model
  :noindex:

  .. method:: disable_delete(self, ar)

    Return `None` when there is no veto against deleting this :term:`database
    row`, otherwise a translatable message that explains to the user why they
    can't delete this row.

As an example, here is how the :meth:`disable_delete <Model.disable_delete>`
method of :class:`lino_xl.lib.cal.GuestsByEvent` table adds a customized veto
message to refuse deleting the presence of a guest in a calendar event for which
Lino manages presences automatically ::

    @classmethod
    def disable_delete(cls, obj, ar):
        msg = super(GuestsByEvent, cls).disable_delete(obj, ar)
        if msg is not None:
            return msg
        mi = ar.master_instance
        assert mi == obj.event
        if mi.can_edit_guests_manually():
            return None
        return _("Cannot edit guests manually.")

When you override this method, be careful to call :func:`super` because Lino
finds a lot of veto reasons automatically for you by checking whether the
database contains related objects. For example. Lino by default forbids to
delete any object that is referenced by other objects. Users will get a message
of type "Cannot delete X because n Ys refer to it". See `About cascaded
deletes`_ below for customizing this behaviour.



About cascaded deletes
======================

Lino changes Django's default behaviour regarding cascaded delete on ForeignKey
fields.  You can set the :attr:`allow_cascaded_copy
<Model.allow_cascaded_delete>` and :attr:`allow_cascaded_copy
<Model.allow_cascaded_copy>` class attributes of a model to customize this
behaviour.

With Lino, unlike plain Django, you control cascaded delete behaviour on the
model whose instances are going to be deleted instead of defining it on the
models that refer to it.
So you usually don't need to care about Django's `on_delete
<https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.ForeignKey.on_delete>`__
attribute, Lino automatically (in :meth:`kernel_startup
<lino.core.kernel.Kernel.kernel_startup>`) sets this to ``PROTECT`` for all FK
fields that are not listed in the :attr:`allow_cascaded_delete` of their model.

.. class:: Model
  :noindex:

  .. attribute:: allow_cascaded_delete

    A set of names of `ForeignKey` or `GenericForeignKey` fields of
    this model that allow for cascaded delete.

    If this is a simple string, Lino expects it to be a space-separated list of
    field names and convert it into a set at startup.

    This is also used by :class:`lino.mixins.duplicable.Duplicate` to decide
    whether slaves of a record being duplicated should be duplicated as well.

Example: Lino should not refuse to delete a Mail just because it has some
Recipient.  When deleting a Mail, Lino should also delete its Recipients. That's
why :class:`lino_xl.lib.outbox.models.Recipient` has ``allow_cascaded_delete =
'mail'``.



.. class:: Model
  :noindex:


  .. method:: on_duplicate(self, ar, master)

    Called after duplicating a row on the new row instance.

    `ar` is the action request that asked to duplicate.

    If `master` is not None, then this is a cascaded duplicate
    initiated by a :meth:`duplicate` on the specified `master`.

    Also called recursively on all related objects.  Where "related
    objects" means those which point to the master using a FK which is
    listed in :attr:`allow_cascaded_delete`.

    Called by the :class:`lino.mixins.duplicable.Duplicate` action.

    Note that this is called *before* saving the object for the
    first time.

    Obsolete: On the master (i.e. when `master` is `None`), this
    is called *after* having saved the new object for a first
    time, and for related objects (`master` is not `None`) it is
    called *before* saving the object.  But even when an
    overridden :meth:`on_duplicate` method modifies a master, you
    don't need to :meth:`save` because Lino checks for
    modifications and saves the master a second time when needed.



  .. method:: after_duplicate(self, ar, master)

    Called by :class:`lino.mixins.duplicable.Duplicate` on
    the new copied row instance, after the row and it's related fields
    have been saved.

    `ar` is the action request that asked to duplicate.

    `ar.selected_rows[0]` contains the original row that is being
    copied, which is the `master` parameter.


  .. method:: delete_veto_message(self, m, n)

    Return the message :message:`Cannot delete X because N Ys refer to it.`

  .. attribute:: allow_cascaded_copy

    A set of names of `ForeignKey` or `GenericForeignKey` fields of
    this model that cause objects to be automatically duplicated when
    their master gets duplicated.

    If this is a simple string, Lino expects it to be a space-separated list of
    field names and convert it into a `set` during startup.


During startup, Lino installs a `disable_delete` handler on each model.
Preventing accidental deletes

>>> from lino import startup
>>> startup('lino_book.projects.min1.settings')
>>> from lino.api.doctest import *

The output of :meth:`lino.utils.diag.analyzer.show_foreign_keys` gives an
overview of the rules that apply for your application.

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())
... #doctest: +REPORT_UDIFF +NORMALIZE_WHITESPACE
- contacts.Company :
  - PROTECT : contacts.Role.company, system.SiteConfig.site_company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Company.partner_ptr, contacts.Person.partner_ptr
  - PROTECT : users.User.partner
- contacts.Person :
  - PROTECT : contacts.Role.person
- contacts.RoleType :
  - PROTECT : contacts.Role.type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, contacts.Partner.region, countries.Place.parent
- users.User :
  - PROTECT : users.Authority.authorized, users.Authority.user
<BLANKLINE>
