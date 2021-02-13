# -*- coding: utf-8 -*-
# Copyright 2014-2021 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
# pm test tests.test_ipdict

"""This module contains some quick tests:

- In a :class:`lino.modlib.sepa.models.Account`:

  - Fill IBAN and BIC from Belgian NBAN or IBAN
  - Test whether the record is being validated.


"""

import json
import time
from datetime import timedelta

from django.core.exceptions import ValidationError
# from django.test import TestCase
from lino.api import rt, dd
from lino.utils.instantiator import create_row
from lino.utils.test import DemoTestCase

ipdict = dd.plugins.ipdict

class TestCase(DemoTestCase):
    maxDiff = None

    def test_this(self):

        self.assertEqual(ipdict.max_failed_auth_per_ip, 4)
        self.assertEqual(ipdict.max_blacklist_time, timedelta(minutes=1))

        # For this test we reduce max_blacklist_time because we are going to
        # simulate a hacker who patiently waits:
        ipdict.max_blacklist_time = timedelta(seconds=1)

        self.assertEqual(ipdict.ip_records, {})

        def login(pwd):
            d = self.login('robin', pwd)
            return d.message

        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        rec = ipdict.ip_records['127.0.0.1']
        self.assertEqual(rec.login_failures, 1)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 2)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 3)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 4)
        self.assertEqual(login("bad"), 'Too many authentication failures from 127.0.0.1')

        # login_failures doesn't continue to increase when the ip is blacklisted:
        self.assertEqual(rec.login_failures, 4)

        # Even with the right password you cannot unlock a blacklisted ip
        self.assertEqual(login("1234"), 'Too many authentication failures from 127.0.0.1')

        # After max_blacklist_time, the IP gets removed from the blacklist, but
        # every new failure will now blacklist it again, the
        # max_failed_auth_per_ip no longer counts.

        time.sleep(1)
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        self.assertEqual(rec.login_failures, 5)
        self.assertEqual(login("bad"), 'Too many authentication failures from 127.0.0.1')
        self.assertEqual(rec.login_failures, 5)

        time.sleep(1)
        self.assertEqual(login("1234"), 'Now logged in as Robin Rood')

        # Once you manage to authenticate, your ip address gets removed from the
        # blacklist, i.e. when you log out and in for some reason, you get again
        # max_failed_auth_per_ip attempts

        self.assertEqual(ipdict.ip_records, {})
        self.assertEqual(login("bad"), 'Failed to log in as robin.')
        rec = ipdict.ip_records['127.0.0.1']
        self.assertEqual(rec.login_failures, 1)
