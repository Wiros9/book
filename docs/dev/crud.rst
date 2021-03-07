=====================
About CRUD operations
=====================

The acronym **CRUD** stands for "create, read, update and delete". These are the
four basic operations to use when you manipulate the content of a
:term:`database`.

- To customize whether certain fields are editable or not, you override the
  :meth:`Model.disabled_fields` method. See :doc:`disabled_fields`.

- To customize whether a :term:`database row` can be deleted or not, you
  override the :meth:`Model.disable_delete` method. See :doc:`disable_delete`.

- There are many ways to customize how data is formatted when presented to the
  end user. See :doc:`model_format`.
