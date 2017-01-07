.. _lino.tested.ddh:

=============================
Preventing accidental deletes
=============================

This document tests this functionality.


.. to run only this test:

    $ python setup.py test -s tests.DocsTests.test_ddh
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_book.projects.docs.settings.doctests'
    >>> from lino.api.doctest import *


>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_foreign_keys())  #doctest: +REPORT_UDIFF
- concepts.Concept :
  - PROTECT : concepts.Link.child, concepts.Link.parent
- contacts.Company :
  - PROTECT : contacts.Role.company, system.SiteConfig.site_company
- contacts.CompanyType :
  - PROTECT : contacts.Company.type
- contacts.Partner :
  - CASCADE : contacts.Company.partner_ptr, contacts.Person.partner_ptr
  - PROTECT : polls.Response.partner, users.User.partner
- contacts.Person :
  - PROTECT : contacts.Role.person
- contacts.RoleType :
  - PROTECT : contacts.Role.type
- contenttypes.ContentType :
  - PROTECT : changes.Change.master_type, changes.Change.object_type, gfks.HelpText.content_type, notify.Message.owner_type, uploads.Upload.owner_type
- countries.Country :
  - PROTECT : contacts.Partner.country, countries.Place.country
- countries.Place :
  - PROTECT : contacts.Partner.city, contacts.Partner.region, countries.Place.parent
- polls.Choice :
  - PROTECT : polls.AnswerChoice.choice
- polls.ChoiceSet :
  - PROTECT : polls.Choice.choiceset, polls.Poll.default_choiceset, polls.Question.choiceset
- polls.Poll :
  - CASCADE : polls.Question.poll
  - PROTECT : polls.Response.poll
- polls.Question :
  - PROTECT : polls.AnswerChoice.question, polls.AnswerRemark.question
- polls.Response :
  - PROTECT : polls.AnswerChoice.response, polls.AnswerRemark.response
- uploads.UploadType :
  - PROTECT : uploads.Upload.type
- users.User :
  - PROTECT : changes.Change.user, notify.Message.user, polls.Poll.user, polls.Response.user, tinymce.TextFieldTemplate.user, uploads.Upload.user, users.Authority.authorized, users.Authority.user
<BLANKLINE>

