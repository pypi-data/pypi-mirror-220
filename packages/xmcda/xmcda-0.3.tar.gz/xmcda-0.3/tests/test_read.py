from pathlib import Path

from xmcda import ValidationError
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestReadXMCDA(XMCDATestCase):

    def test_load_1(self):
        xmcda = XMCDA()
        xmcda.load('tests/files/v3/xmcda_1.xml')
        alternatives = xmcda.alternatives
        self.assertEqual(len(alternatives), 3)
        a01 = alternatives['a01']
        self.assertTrue(a01.is_real)
        self.assertTrue(a01.active)

    def test_load_2(self):
        xmcda = XMCDA()
        xmcda.load('tests/files/v3/xmcda_2.xml')
        alternatives = xmcda.alternatives
        self.assertEqual(len(alternatives), 3)
        a01 = alternatives['a02']
        self.assertTrue(a01.is_real)
        self.assertFalse(a01.active)

    def test_load_path(self):
        xmcda = XMCDA()
        xmcda.load(Path('tests/files/v3/xmcda_1.xml'))
        alternatives = xmcda.alternatives
        self.assertEqual(len(alternatives), 3)
        a01 = alternatives['a01']
        self.assertTrue(a01.is_real)
        self.assertTrue(a01.active)

    def test_load_two_performance_tables(self):
        xmcda = XMCDA()
        xmcda.load('tests/files/v3/two_performance_tables.xml')
        perfTables = xmcda.performance_tables
        self.assertEqual(len(perfTables), 2)

    def test_read_specific_tags(self):
        xmcda = XMCDA()
        xmcda.load('tests/files/v3/read_specific_tags_only.xml',
                   tags='performanceTable')
        from xmcda import create_on_access, set_create_on_access
        ori = create_on_access()
        try:
            set_create_on_access(False)

            self.assertEqual(len(xmcda.performance_tables), 1)
            self.assertEqual(xmcda.alternatives['a01'].name, None)

            with self.assertRaises(IndexError):
                xmcda.alternatives['a02']
        finally:
            set_create_on_access(ori)

    def test_load_invalid(self):
        with self.assertRaises(ValidationError):
            XMCDA().load('tests/files/v3/sample-invalid-XMCDA.xml')
        with self.assertRaises(ValidationError):
            XMCDA().load('tests/files/v4/invalid.xml')

    def test_fromstring_invalid(self):
        with self.assertRaises(ValidationError):
            with open('tests/files/v3/sample-invalid-XMCDA.xml') as invalid:
                XMCDA().fromstring(invalid.read())
        with self.assertRaises(ValidationError):
            with open('tests/files/v4/invalid.xml') as invalid:
                XMCDA().fromstring(invalid.read())
