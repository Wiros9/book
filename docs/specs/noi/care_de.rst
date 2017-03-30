.. _noi.specs.care_de:

====================================
Lino Care - Technische Spezifikation
====================================

.. How to test only this document:

    $ python setup.py test -s tests.SpecsTests.test_care_de
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_book.projects.care_de.settings')
    >>> from lino.api.doctest import *

Dieses Dokument ist eine technische Beschreibung der Funktionalitäten
von Lino Care. Es ist auch Teil der Test-Suite.

Die englische Version dieses Dokuments (:doc:`/specs/noi/care`) ist
umfangreicher.

.. contents::
  :local:



Das Hauptmenü
=============

**Systemverwalter** haben ei nkomplettes Menü:

>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Stimmabgaben : Meine Aufgaben, Meine Interessen, Meine Kandidaturen, Meine Stimmabgaben
- Büro : Meine Auszüge, Meine Kommentare, Meine Benachrichtigungen, Meine Uploads
- Projekte : Meine Projekte, Meine Anfragen, Wo ich helfen kann, Aktive Tickets, Alle Tickets, Nicht zugewiesene Tickets
- Berichte :
  - System : Broken GFKs
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Kontakte : Themen, Themengruppen, Organisationsarten, Funktionen
  - Büro : Auszugsarten, Kommentar-Arten, Upload-Arten
  - Projekte : Projekte, Projekte (Hierarchie), Project Types, Ticket types, Umfelder
  - Fähigkeiten : Fähigkeiten (Hierarchie), Fähigkeiten (Alle), Fähigkeitsarten
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerarten, Änderungen, Benachrichtigungen, All dashboard widgets
  - Kontakte : Interessen, Kontaktpersonen
  - Stimmabgaben : Alle Stimmabgaben, Stimmabgabezustände
  - Büro : Auszüge, Kommentare, Uploads, Upload-Bereiche
  - Projekte : Verknüpfungen, Ticketzustände, Zuständigkeiten
  - Fähigkeiten : Fähigkeitsangebote, Anfragen
- Site : Info


**Einfache** Benutzer haben ein eingeschränktes Menü:

>>> rt.login('berta').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Stimmabgaben : Meine Aufgaben, Meine Interessen, Meine Kandidaturen, Meine Stimmabgaben
- Büro : Meine Kommentare, Meine Benachrichtigungen, Meine Uploads
- Projekte : Meine Projekte, Meine Anfragen, Wo ich helfen kann
- Site : Info

Bewertungen
===========


>>> base = '/choices/votes/Votes/rating'
>>> show_choices("rolf", base + '?query=')
<br/>
Sehr gut
Gut
Ausreichend
Mangelhaft
Ungenügend
Nicht bewertbar


