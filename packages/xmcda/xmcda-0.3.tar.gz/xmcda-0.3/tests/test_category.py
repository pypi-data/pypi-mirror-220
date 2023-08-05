import xmcda
from xmcda.categories import Category
from xmcda.description import Description

from .utils import XMCDATestCase


class TestCategory(XMCDATestCase):

    xml_1 = '''
        <category id="cat01" name="n1" mcdaConcept="m1">
                <description>
                        <comment>cat01 comment</comment>
                </description>
                <active>false</active>
        </category>'''

    xml_2 = '<category id="cat02"/>'  # check default values

    def setUp(self):
        # restore defaults
        xmcda.reset_settings()

    def _test_defaults(self, c, _id):
        self.assertEqual(c.id, _id)
        self.assertIsNone(c.name)
        self.assertIsNone(c.mcda_concept)
        self.assertTrue(c.active)
        self.assertIsNone(c.description)

    def test_init(self):
        c_id = 'c01'
        c = Category(id=c_id)
        self._test_defaults(c, c_id)

    def test_init_with_values(self):
        c = Category(id='i', name='n', mcda_concept='m', active=False)
        self.assertEqual(c.id, 'i')
        self.assertEqual(c.name, 'n')
        self.assertEqual(c.mcda_concept, 'm')
        self.assertEqual(c.active, False)

    def test_active_not_nullable(self):
        c = Category()
        c.active = None
        self.assertEqual(c.active, True)

    def test_str(self):
        c = Category()
        self.assertEqual(str(c), "Category()")
        c = Category(id='c1', name='n1', mcda_concept='m1', active=False)
        self.assertEqual(str(c),
                         "Category(id='c1', name='n1', mcda_concept='m1')")

    def test_repr(self):
        c = Category()
        self.assertTrue(repr(c), "<Category at ")

    def _test_load_xml_1(self, c):
        self.assertEqual(c.id, 'cat01')
        self.assertEqual(c.name, 'n1')
        self.assertEqual(c.mcda_concept, 'm1')
        self.assertFalse(c.active)
        self.assertIsNotNone(c.description)
        self.assertIsInstance(c.description, Description)
        self.assertEqual(c.description.comment, 'cat01 comment')

    def test_load_xml_1_constructor(self):
        element = self.read_xml(TestCategory.xml_1)
        c = Category(element)

        self._test_load_xml_1(c)

    def test_load_xml_2(self):
        element = self.read_xml(TestCategory.xml_2)
        c = Category(element)

        self.assertEqual(c.id, 'cat02')
        self.assertIsNone(c.name)
        self.assertIsNone(c.mcda_concept)
        self.assertTrue(c.active)
        self.assertIsNone(c.description)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestCategory.xml_1)

        result = utf8_to_utf8(TestCategory.xml_1, Category)
        self.assertEqual(source, result)
