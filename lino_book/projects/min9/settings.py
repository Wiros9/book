# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *
from lino.utils import i2d


class Site(Site):
    title = "Lino Mini 9"
    project_model = 'contacts.Person'
    languages = 'en de fr'
    user_types_module = 'lino_xl.lib.xl.user_types'
    demo_fixtures = """std demo demo2 checkdata""".split()
    default_build_method = 'weasy2pdf'

    the_demo_date = i2d(20141023)
    webdav_protocol = 'davlink'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.users'
        yield 'lino_book.projects.min9.modlib.contacts'
        yield 'lino_xl.lib.excerpts'
        yield 'lino_xl.lib.addresses'
        yield 'lino_xl.lib.phones'
        yield 'lino_xl.lib.reception'
        yield 'lino_xl.lib.courses'
        yield 'lino_xl.lib.sepa'
        yield 'lino_xl.lib.notes'
        # yield 'lino_xl.lib.projects'
        yield 'lino_xl.lib.humanlinks'
        yield 'lino_xl.lib.households'
        yield 'lino_xl.lib.calview'
        # yield 'lino_xl.lib.extensible'
        yield 'lino_xl.lib.pages'
        yield 'lino.modlib.export_excel'
        yield 'lino_xl.lib.dupable_partners'
        yield 'lino.modlib.checkdata'
        yield 'lino.modlib.tinymce'
        # yield 'lino.modlib.wkhtmltopdf'
        yield 'lino.modlib.weasyprint'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.notify'
        yield 'lino.modlib.changes'
        yield 'lino.modlib.comments'
        yield 'lino.modlib.uploads'
        yield 'lino_xl.lib.properties'
        yield 'lino_xl.lib.cv'
        yield 'lino_xl.lib.b2c'
        yield 'lino_xl.lib.sales'
        yield 'lino_xl.lib.finan'

    def get_plugin_configs(self):
        """
        Change the default value of certain plugin settings.
        """
        yield super(Site, self).get_plugin_configs()
        yield ('countries', 'country_code', 'BE')
        yield ('b2c', 'import_statements_path', self.project_dir.child('sepa_in'))

    def do_site_startup(self):
        # lino_xl.lib.reception requires some workflow to be imported
        from lino_xl.lib.cal.workflows import feedback
        super(Site, self).do_site_startup()

SITE = Site(globals())

# ALLOWED_HOSTS = ['*']
DEBUG = True
# SECRET_KEY = "20227"  # see :djangoticket:`20227`
