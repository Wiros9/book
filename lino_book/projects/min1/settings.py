# -*- coding: UTF-8 -*-
# Copyright 2012-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *
from lino.utils import i2d


class Site(Site):
    title = "Lino Mini 1"
    demo_fixtures = 'std demo demo2'
    user_types_module = 'lino_xl.lib.xl.user_types'
    use_experimental_features = True
    languages = "en de fr"
    the_demo_date = i2d(20141023)

    def setup_quicklinks(self, user, tb):
        super(Site, self).setup_quicklinks(user, tb)
        tb.add_action(self.modules.contacts.Persons)
        tb.add_action(self.modules.contacts.Companies)

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino_xl.lib.contacts'

SITE = Site(globals())
DEBUG = True
