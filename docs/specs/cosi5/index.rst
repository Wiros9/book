.. doctest docs/specs/cosi5/index.rst

===============
Lino in Bengali
===============

Here is a screenshot of the :mod:`lino_book.projects.cosi5` demo project.

.. image:: /images/screenshots/0307_cosi5_bn.png


.. include:: /../docs/shared/include/tested.rst

>>> import lino
>>> lino.startup('lino_book.projects.cosi5.settings')
>>> from lino.api.doctest import *

>>> show_menu('roby')
- যোগাযোগ : Persons, Organizations
- অফিস : My Excerpts, My Upload files
- Sales : Sales invoices (SLS)
- Reports :
  - Sales : Due invoices, Sales invoice journal
  - Accounting : Accounting Report, Debtors, Creditors
- Configure :
  - System : Help Texts, Users, Site Parameters
  - Places : Countries, Places
  - যোগাযোগ : Organization types, Functions
  - অফিস : Excerpt Types, Library volumes, Upload types, My Text Field Templates
  - Sales : Products, Product Categories, Price rules, Paper types
  - Accounting : Sheet items, Accounts, Journals, Fiscal years, Accounting periods, Payment terms
- Explorer :
  - System : কনটেন্ট টাইপ সমূহ, Authorities, User types, User roles, Data checkers, Data problems
  - যোগাযোগ : Contact persons, Partners
  - অফিস : Excerpts, Upload files, Upload areas, Text Field Templates
  - SEPA : Bank accounts
  - Sales : Price factors, Sales invoices, Sales invoice items
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - Accounting : Accounting Reports, Common sheet items, General account balances, Analytic accounts balances, Partner balances, Sheet item entries, Common accounts, Match rules, Vouchers, Voucher types, Movements, Trade types, Journal groups
  - VAT : VAT areas, VAT regimes, VAT classes, VAT columns, Invoices, VAT rules
- Site : About, User sessions


>>> rt.show(products.Products)
==== ================================================================ ================== ================= =============
 ID   Designation                                                      Designation (bn)   Category          Sales price
---- ---------------------------------------------------------------- ------------------ ----------------- -------------
 10   Book                                                             Book               Other             29,90
 6    IT consultation & maintenance                                                       Website Hosting   30,00
 9    Image processing and website content maintenance                                    Website Hosting   25,00
 4    Metal chair                                                                         Furniture         79,99
 3    Metal table                                                                         Furniture         129,99
 8    Programming                                                                         Website Hosting   40,00
 7    Server software installation, configuration and administration                      Website Hosting   35,00
 11   Stamp                                                            Stamp              Other             1,40
 5    Website hosting 1MB/month                                                           Website Hosting   3,99
 2    Wooden chair                                                                        Furniture         99,99
 1    Wooden table                                                                        Furniture         199,99
                                                                                                            **675,25**
==== ================================================================ ================== ================= =============
<BLANKLINE>
