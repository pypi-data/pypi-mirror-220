from xmcda.categories import Categories, Category
from xmcda.description import Description
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class TestCategories(XMCDATestCase):

    xml_1 = '<categories><category id="c01"/></categories>'

    xml_2 = '''
        <categories id="id1" name="n1" mcdaConcept="m1">
            <description><comment>poney</comment></description>
            <category id="c1" name="nc1"/>
            <category id="c2"/>
            <category id="c3"/>
        </categories>'''

    xmcda_2 = make_xmcda_v4(xml_2)

    def tearDown(self):
        # restore defaults
        import xmcda
        xmcda.reset_settings()

    def _test_defaults(self, cs):
        self.assertIsNone(cs.id)
        self.assertIsNone(cs.name)
        self.assertIsNone(cs.mcda_concept)
        self.assertIsNone(cs.description)

    def test_init(self):
        cs = Categories()
        self._test_defaults(cs)
        self.assertEqual(Categories(id='id_cs').id, 'id_cs')

    def test_getitem_int(self):
        categories = Categories()
        cat01 = Category(id='cat01')
        categories.append(cat01)
        self.assertEqual(categories[0], cat01)

    def test_getitem_by_id(self):
        categories = Categories()
        cat01 = Category(id='cat01')
        categories.append(cat01)
        self.assertEqual(categories[cat01.id], cat01)

    def test_getitem_str_automatic_creation(self):
        categories = Categories()
        cat01 = categories['cat01']
        self.assertIsNotNone(cat01)
        import xmcda
        xmcda.set_create_on_access(False, 'category')
        with self.assertRaises(IndexError):
            categories['cui-cui']

    def test_load_xml_1(self):
        xml = self.read_xml(TestCategories.xml_1)

        cs = Categories(xml)
        self._test_defaults(cs)
        self.assertEqual(len(cs), 1)
        self.assertEqual(cs[0].id, 'c01')

    def test_load_xml_2(self):
        xml = self.read_xml(TestCategories.xml_2)

        cs = Categories(xml)
        self.assertEqual(cs.id, 'id1')
        self.assertEqual(cs.name, 'n1')
        self.assertEqual(cs.mcda_concept, 'm1')
        self.assertIsNotNone(cs.description)
        self.assertIsInstance(cs.description, Description)
        self.assertEqual(cs.description.comment, 'poney')
        # test content
        self.assertEqual(len(cs), 3)
        self.assertEqual(cs[0].id, 'c1')  # xml order must be preserved
        self.assertEqual(cs[1].id, 'c2')
        self.assertEqual(cs[2].id, 'c3')

    def test_merge_with_xmcda(self):
        xmcda = XMCDA()
        c1 = Category(id='c1')
        xmcda.categories.append(c1)

        xml = self.read_xml(TestCategories.xml_2)
        xmcda.categories.merge_xml(xml)
        # c1 must have been used when loading the xml
        cs = xmcda.categories
        self.assertEqual(len(cs), 3)
        self.assertEqual(cs[0], c1)  # xml order must be preserved
        self.assertEqual(c1.name, 'nc1')  # name has been updated
        self.assertEqual(cs[1].id, 'c2')
        self.assertEqual(cs[2].id, 'c3')

    def test_load_with_xmcda(self):
        xmcda = XMCDA()
        c1 = Category(id='c1')
        xmcda.categories.append(c1)

        xmcda.fromstring(TestCategories.xmcda_2)
        # c1 must have been updated when loading the xml
        cs = xmcda.categories
        self.assertEqual(len(cs), 3)
        self.assertEqual(cs[0], c1)  # xml order must be preserved
        self.assertEqual(c1.name, 'nc1')  # name has been updated
        self.assertEqual(cs[1].id, 'c2')
        self.assertEqual(cs[2].id, 'c3')

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestCategories.xml_1)
        result = utf8_to_utf8(TestCategories.xml_1, Categories)
        self.assertEqual(source, result)

        source = compact_xml(TestCategories.xml_2)
        result = utf8_to_utf8(TestCategories.xml_2, Categories)
        self.assertEqual(source, result)
