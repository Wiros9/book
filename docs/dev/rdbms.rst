====================
Relational databases
====================

Let's make sure whether you know the following concepts.

.. glossary::

  database

    A named set of one or more :term:`database tables <database table>`, stored
    in one place together with user access rights and other information.

  database table

    A set of :term:`rows <database row>` that can be represented using a same
    set of :term:`database columns <database column>`.

    Each table is made up of rows and columns.  If you imagine a table as a grid,
    the columns go from left to right across the grid and each entry of data is
    listed down as a row.

  database row

    A row in a :term:`database table`.

  database column

    A column in a :term:`database table`.

    A database column is defined by its *name* and its *data type*.   Typical
    data types are for example "text", "date", "timestamp", "number"... The
    *name* of a column is used when selecting and ordering data, and the *type*
    is used to validate information stored.

  primary key

    A text or --more often-- a number used to *identify* a given row in a given
    table.

    Each row in a table is uniquely identified by its :term:`primary key`.  In
    SQL this can be one or more sets of column values, but Django supports only
    *atomic* primary keys, i.e. a single column that is used to store its value.
    No two rows can have the same primary key value.  You can *select* every
    single row by just knowing its primary key.

  database server

    A background process on a :term:`Lino server` that nothing but wait for
    incoming *requests* (formulated in :term:`SQL`), *execute* them and return a
    *response*.

  ORM

    (`Object-relational mapping
    <https://en.wikipedia.org/wiki/Object%E2%80%93relational_mapping>`__) is the
    technology that connects between your application program and a
    :term:`database server`.

  SQL

    (`Structured Query Language <https://en.wikipedia.org/wiki/SQL>`__) is the
    language used by two computers when they talk about operations in a
    :term:`database`.
