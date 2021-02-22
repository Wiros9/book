import datetime

from lino_avanti.lib.avanti.settings import *

class Site(Site):

    the_demo_date = datetime.date(2017, 2, 15)
    languages = "en de fr"

    def get_plugin_configs(self):
        yield super(Site, self).get_plugin_configs()
        yield ('clients', 'demo_coach', 'nathalie')
        yield ('beid', 'simulate_eidreader_path', self.project_dir.child('simulate_eidreader'))
        yield ('uploads', 'remove_orphaned_files', True)

SITE = Site(globals())

DEBUG = True

# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'

# SITE.eidreader_timeout = 25
