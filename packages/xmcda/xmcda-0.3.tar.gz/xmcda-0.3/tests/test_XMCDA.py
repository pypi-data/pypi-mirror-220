import xmcda
from xmcda.alternatives import Alternative, Alternatives
from xmcda.categories import Categories, Category
from xmcda.criteria import Criteria, Criterion
from xmcda.performance_table import PerformanceTable
from xmcda.schemas import XMCDA_4_0_0
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, compact_xml, make_xmcda_v4


class TestXMCDA_defaults(XMCDATestCase):

    def setUp(self):
        self.xmcda = XMCDA()

    def test_alternatives(self):
        xmcda = self.xmcda
        self.assertIsNotNone(xmcda.alternatives)
        self.assertTrue(isinstance(xmcda.alternatives, Alternatives))
        xmcda.alternatives.append(Alternative(id='a1'))
        self.assertIsNotNone(xmcda.alternatives['a1'])

    def test_criteria(self):
        xmcda = self.xmcda
        self.assertIsNotNone(xmcda.criteria)
        self.assertTrue(isinstance(xmcda.criteria, Criteria))
        xmcda.criteria.append(Criterion(id='c01'))
        self.assertIsNotNone(xmcda.criteria['c01'])

    def test_categories(self):
        xmcda = self.xmcda
        self.assertIsNotNone(xmcda.categories)
        self.assertTrue(isinstance(xmcda.categories, Categories))
        xmcda.categories.append(Category(id='cat1'))
        self.assertIsNotNone(xmcda.categories['cat1'])

    def test_performance_table(self):
        xmcda = self.xmcda
        self.assertIsNotNone(xmcda.performance_tables)
        self.assertTrue(isinstance(xmcda.performance_tables, list))
        xmcda.categories.append(PerformanceTable(id='perfTab1'))
        self.assertIsNotNone(xmcda.categories['perfTab1'])

    def test_criteria_scales(self):
        xmcda = self.xmcda
        self.assertIsNotNone(xmcda.criteria_scales_list)
        self.assertTrue(isinstance(xmcda.criteria_scales_list, list))

    xml_1 = make_xmcda_v4('''<alternatives><alternative id="a1"/></alternatives>
<criteria><criterion id="c1"></criterion></criteria>''')

    def test_merge_xml(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        xmcda.merge_xml(xml, Alternatives)
        self.assertEqual(len(xmcda.alternatives), 1)

        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        xmcda.merge_xml(xml, 'alternatives')
        self.assertEqual(len(xmcda.alternatives), 1)

        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        xmcda.merge_xml(xml, ('alternatives', Criteria))
        self.assertEqual(len(xmcda.alternatives), 1)
        self.assertEqual(len(xmcda.criteria), 1)

        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        xmcda.merge_xml(xml, (Category, Criterion))
        self.assertEqual(len(xmcda.alternatives), 0)
        self.assertEqual(len(xmcda.criteria), 0)

    def test_load_preconditions(self):
        with self.assertRaises(ValueError):
            xmcda.XMCDA.load(None)
        with self.assertRaises(ValueError):
            self.xmcda.load(None)

    def test_read_preconditions(self):
        with self.assertRaises(ValueError):
            xmcda.XMCDA.fromstring(None)
        with self.assertRaises(ValueError):
            self.xmcda.fromstring(None)

    empty_xmcda = compact_xml('''
<xmcda xmlns="http://www.decision-deck.org/2021/XMCDA-4.0.0"/>''')

    xmcda_with_a1 = compact_xml('''
<xmcda xmlns="http://www.decision-deck.org/2021/XMCDA-4.0.0">
    <alternatives><alternative id="a1"/></alternatives>
</xmcda>''')

    xmcda_with_a1_c1 = compact_xml('''
<xmcda xmlns="http://www.decision-deck.org/2021/XMCDA-4.0.0">
    <alternatives><alternative id="a1"/></alternatives>
    <criteria><criterion id="c1"/></criteria>
</xmcda>''')

    def test_to_xml(self):
        self.maxDiff = None
        xmcda_tostr = xmcda.utils.tostring

        xml_str = xmcda_tostr(XMCDA().to_xml())
        self.assertEqual(xml_str, self.empty_xmcda)

        x = self.xmcda
        x.alternatives.append(Alternative(id='a1'))
        x.criteria.append(Criterion(id='c1'))
        xml_str = xmcda_tostr(x.to_xml())
        self.assertEqual(xml_str, self.xmcda_with_a1_c1)

        xml_str = xmcda_tostr(x.to_xml(tags="alternatives"))
        self.assertEqual(xml_str, self.xmcda_with_a1)

        xml_str = xmcda_tostr(x.to_xml(tags=Alternatives))
        self.assertEqual(xml_str, self.xmcda_with_a1)

        xml_str = xmcda_tostr(x.to_xml(tags=('alternatives', 'criteria')))
        self.assertEqual(xml_str, self.xmcda_with_a1_c1)

        xml_str = xmcda_tostr(x.to_xml(tags=(Alternatives, Criteria)))
        self.assertEqual(xml_str, self.xmcda_with_a1_c1)

    def test_write(self):
        from io import BytesIO
        s = BytesIO()
        XMCDA().write(s, xml_declaration=False, schema=XMCDA_4_0_0)
        serialized_empty = s.getvalue().decode('utf-8').strip()
        self.assertEqual(serialized_empty, self.empty_xmcda)
