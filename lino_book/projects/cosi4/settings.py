# -*- coding: UTF-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


import datetime

from lino_cosi.lib.cosi.settings import *

class Site(Site):
    languages = 'en zh-hant'

    demo_fixtures = 'std all_countries minimal_ledger \
    furniture demo demo_bookings payments demo2'.split()

    # temporary:
    # demo_fixtures = 'std all_countries minimal_ledger \
    # furniture demo demo_bookings demo2'.split()

    #demo_fixtures = 'std few_countries minimal_ledger \
    #furniture \
    #demo demo_bookings payments demo2'.split()

    is_demo_site = True
    # ignore_dates_after = datetime.date(2019, 05, 22)
    the_demo_date = datetime.date(2021, 6, 12)
    # default_ui = 'lino_react.react'


    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('vat', 'declaration_plugin', 'lino_xl.lib.eevat')
        yield ('countries', 'hide_region', False)
        yield ('countries', 'country_code', 'EE')
        yield ('ledger', 'use_pcmn', True)
        yield ('ledger', 'start_year', 2020)


SITE = Site(globals())
DEBUG = True
