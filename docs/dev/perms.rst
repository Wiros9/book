.. doctest docs/dev/perms.rst
.. _dev.permissions:
.. _permissions:

===========================
Introduction to permissions
===========================

As soon as a database application is used by more than one user, we usually need
to speak about **permissions**.  For example, a :term:`site administrator` can
see certain resources that a simple :term:`end user` should not get to see.  The
application must check whether a given user has permission to see a given
resource or to execute a given action.  An application framework must provide a
system for managing these permissions. Lino replaces Django's user management
and permission system (see :doc:`/dev/about/auth` if you wonder why).

.. contents::
    :depth: 1
    :local:

.. include:: /../docs/shared/include/tested.rst

>>> from lino import startup
>>> startup('lino_book.projects.min9.settings')
>>> from lino.api.doctest import *




User roles
==========

A **user role** is a role of a user in our application. It is used as
the basic unit for defining permissions.

- Every user has a set of roles.
- Every resource (table or action) has a set of *required* roles.

User roles are class objects that represent conditions for getting permission to
access the functionalities of the application.  Lino comes with a few built-in
user roles that are defined in :mod:`lino.core.roles`.  Every plugin may define
its own user roles which must be subclasses of these builtin roles.  A role can
inherit from one or several other roles.

A real-world application can define *many* user roles. For example
here is an inheritance diagram of the roles used by :ref:`noi`:

.. inheritance-diagram:: lino_noi.lib.noi.user_types

And if you think this diagram is complex, then don't look at the
following one (that of :ref:`welfare`)...

.. inheritance-diagram:: lino_welfare.modlib.welfare.user_types

As the application developer you must specify for each resource the
role(s) that are *required* to use it.


User types
==========

When creating a new user, the site administrator needs to assign these
roles to every user.

But imagine they would get, for each user group, a multiple-choice
combobox with all available roles from above examples! They would get
crazy.

That's why we have **user types**.  The application developer defines
a meaningful *subset of all available roles* for their application.
This is done by populating the :class:`UserTypes
<lino.modlib.users.choicelists.UserTypes>` choicelist.

User types are a way to classify end users in order to grant them different sets
of permissions.

Each user type is basically not much more than a user-friendly *name*
and a storable *value* given to a selected user role.  Here is the
default list of user types, defined in :mod:`lino.core.user_types`:

>>> rt.show(users.UserTypes)
======= =========== ===============
 value   name        text
------- ----------- ---------------
 000     anonymous   Anonymous
 100     user        User
 900     admin       Administrator
======= =========== ===============
<BLANKLINE>


Actually a user *type* contains a bit more information than a user
role.  It has the following fields:

- :attr:`role`, the role given to users of this type
- :attr:`text`, a translatable name
- :attr:`value`, a value for storing it in the database

- :attr:`readonly
  <lino.modlib.users.choicelists.UserType.readonly>` defines a user
  type which shows everything that a given user role can see, but
  unlike the original user role it cannot change any data.

- :attr:`hidden_languages
  <lino.modlib.users.choicelists.UserType.hidden_languages>`
  (experimental), a set of languages to *not* show to users of this
  type. This is used on sites with more than three or four
  :attr:`languages <lino.core.site.Site.languages>`.


The **user type** of a user is stored in a field whose internal name
is :attr:`user_type <lino.modlib.users.models.User.user_type>`. This is
because at the beginnings of Lino we called them "user profiles".  Now
we prefer to call them **user types**. The web interface already calls
them "types", but it will take some time to change all internal names
from "profile" to "type".

>>> rt.show('users.AllUsers', column_names="username user_type")
========== =====================
 Username   User type
---------- ---------------------
 robin      900 (Administrator)
 rolf       900 (Administrator)
 romain     900 (Administrator)
========== =====================
<BLANKLINE>


Relation between user roles and user types
==========================================

There is a built-in virtual table that shows an overview of which roles are
contained for each user type.  This table can be helpful for documenting the
permissions granted to each user type.

>>> rt.show(users.UserRoles)
======================== ===== ===== =====
 Name                     000   100   900
------------------------ ----- ----- -----
 cal.GuestOperator              ☑     ☑
 comments.CommentsStaff               ☑
 comments.CommentsUser          ☑     ☑
 contacts.ContactsStaff               ☑
 contacts.ContactsUser          ☑     ☑
 excerpts.ExcerptsStaff               ☑
 excerpts.ExcerptsUser          ☑     ☑
 notes.NotesStaff                     ☑
 notes.NotesUser                ☑     ☑
 office.OfficeStaff                   ☑
 office.OfficeUser              ☑     ☑
 polls.PollsAdmin                     ☑
 polls.PollsUser                ☑     ☑
 xl.SiteAdmin                         ☑
 xl.SiteUser                    ☑
======================== ===== ===== =====
<BLANKLINE>

Accessing permissions from within your code
===========================================

Just some examples...


>>> UserTypes = rt.models.users.UserTypes

>>> UserTypes.admin
<users.UserTypes.admin:900>

>>> UserTypes.admin.role  #doctest: +ELLIPSIS
<lino_xl.lib.xl.user_types.SiteAdmin object at ...>

>>> UserTypes.admin.readonly
False

>>> UserTypes.admin.hidden_languages


>>> robin = users.User.objects.get(username='robin')
>>> robin.user_type  #doctest: +ELLIPSIS
<users.UserTypes.admin:900>

>>> robin.user_type.role  #doctest: +ELLIPSIS
<lino_xl.lib.xl.user_types.SiteAdmin object at ...>




Defining required roles
=======================

The :term:`application developer` specifies which roles are required for a
given resource.

Where "resource" is one of the following:

- an actor (a subclass of :class:`lino.core.actors.Actor`)
- an action (an instance of :class:`lino.core.actions.Action` or a
  subclass thereof)
- a panel (an instance of :class:`lino.core.layouts.Panel`)

These objects have a :attr:`required_roles
<lino.core.permissions.Permittable.required_roles>` attribute which
must be a :func:`set` of the user roles required for getting
permission to access this resource.

This set of user roles can be specified using the
:func:`login_required <lino.core.roles.login_required>` utility
function.  You can also specify it manually. But it must stisfy some
conditions described in :func:`check_required_roles
<lino.core.roles.check_required_roles>`.


See :meth:`lino.modlib.users.UserType.has_required_role`


For example, the list of all users (the :class:`users.AllUsers
<lino.modlib.users.desktop.AllUsers>` table) is visible only for users
who have the :class:`SiteAdmin <lino.core.roles.SiteAdmin>` role:

>>> sixprint(rt.models.users.AllUsers.required_roles)
{<class 'lino.core.roles.SiteAdmin'>}

>>> from lino.core.roles import SiteUser, SiteAdmin
>>> user = SiteUser()
>>> admin = SiteAdmin()
>>> user.has_required_roles(rt.models.users.AllUsers.required_roles)
False
>>> admin.has_required_roles(rt.models.users.AllUsers.required_roles)
True



Local customizations
====================

You may have noted that :class:`UserTypes
<lino.modlib.users.choicelists.UserTypes>` is a choicelist, not a
database table.  This is because it depends on the application and is
usually not locally modified.

Local site administrators may nevertheless decide to change the set of
available user types.


The user types module
========================

The :attr:`roles_required
<lino.core.permissions.Permittable.roles_required>` attribute is being
ignored when :attr:`user_types_module
<lino.core.site.Site.user_types_module>` is empty.


.. xfile:: roles.py

.. xfile:: user_types.py

The :xfile:`roles.py` is used for both defining roles

A :xfile:`user_types.py` module is used for defining the user roles
that we want to make available in a given application.  Every user
type is assigned to one and only one user role. But not every user
role is made available for selection in that list.



.. _debug_permissions:

Permission debug messages
=========================

Sometimes you want to know why a given action is available (or not
available) on an actor where you would not (or would) have expected it
to be.

In this situation you can temporarily set the `debug_permissions`
attributes on both the :attr:`Actor <lino.core.actors.Actor.debug_permissions>` and
the :attr:`Action <lino.core.actions.Action.debug_permissions>` to True.

This will cause Lino to log an info message for each invocation of a
handler on this action.

Since you probably don't want to have this feature accidentally
activated on a production server, Lino will raise an Exception if this
happens when :setting:`DEBUG` is False.
