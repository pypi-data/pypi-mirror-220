import unittest

import xmcda
from xmcda.alternatives import Alternative
from xmcda.criteria import Criterion


class TestPackageDefaults(unittest.TestCase):

    def tearDown(self):
        xmcda.reset_settings()

    def test_export_defaults(self):
        self.assertFalse(xmcda.export_defaults())

    def test_create_on_access(self):
        # (default: True)
        self.assertTrue(xmcda.create_on_access())
        self.assertTrue(xmcda.create_on_access('alternative'))
        self.assertTrue(xmcda.create_on_access('unspecified_tag'))

        # (default: True) alternative: false
        xmcda.set_create_on_access(False, 'alternative')
        self.assertTrue(xmcda.create_on_access())
        self.assertFalse(xmcda.create_on_access('alternative'))
        self.assertTrue(xmcda.create_on_access('unspecified_tag'))

        # default: False, (alternative: unspecified)
        xmcda.reset_settings()
        xmcda.set_create_on_access(False)
        self.assertFalse(xmcda.create_on_access())
        self.assertFalse(xmcda.create_on_access('alternative'))
        self.assertFalse(xmcda.create_on_access('unspecified_tag'))

        # default False, but alternative & criterion: True
        xmcda.reset_settings()
        xmcda.set_create_on_access(False)
        xmcda.set_create_on_access(True, 'alternative')
        xmcda.set_create_on_access(True, Criterion)
        self.assertFalse(xmcda.create_on_access())
        self.assertTrue(xmcda.create_on_access(Alternative))
        self.assertTrue(xmcda.create_on_access('criterion'))
        self.assertFalse(xmcda.create_on_access('unspecified_tag'))

    def test_mark_creation_does_not_overwrite_marker(self):
        class A:
            marker = 12
        self.assertRaises(ValueError, xmcda.mark_creation, A)
