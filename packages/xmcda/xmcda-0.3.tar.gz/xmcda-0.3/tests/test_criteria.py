from xmcda.criteria import Criteria, Criterion
from xmcda.description import Description
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class TestCriteria(XMCDATestCase):

    xml_1 = '<criteria><criterion id="c01"/></criteria>'

    xml_2 = '''
        <criteria id="id1" name="n1" mcdaConcept="m1">
            <description><comment>crits comment</comment></description>
            <criterion id="c01" name="n01"/>
            <criterion id="c02" name="n02"><active>false</active></criterion>
        </criteria>'''

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
        cs = Criteria()
        self._test_defaults(cs)
        self.assertEqual(Criteria(id='id_cs').id, 'id_cs')

    def test_getitem_int(self):
        criteria = Criteria()
        c = Criterion(id='id_a')
        criteria.append(c)
        self.assertEqual(criteria[0], c)

    def test_getitem_by_id(self):
        criteria = Criteria()
        c01 = Criterion(id='c01')
        criteria.append(c01)
        self.assertEqual(criteria[c01.id], c01)

    def test_getitem_str_automatic_creation(self):
        x = XMCDA()

        c01 = Criterion(id='c01')
        self.assertIsNotNone(c01)

        import xmcda
        xmcda.set_create_on_access(False, 'criterion')
        with self.assertRaises(IndexError):
            x.criteria['cui-cui']

    def test_load_xml_1(self):
        xml = self.read_xml(TestCriteria.xml_1)

        cs = Criteria(xml)
        self._test_defaults(cs)
        self.assertEqual(len(cs), 1)
        self.assertEqual(cs[0].id, 'c01')

    def test_load_xml_2(self):
        xml = self.read_xml(TestCriteria.xml_2)

        crits = Criteria(xml)
        self.assertEqual(crits.id, 'id1')
        self.assertEqual(crits.name, 'n1')
        self.assertEqual(crits.mcda_concept, 'm1')
        self.assertIsNotNone(crits.description)
        self.assertIsInstance(crits.description, Description)
        self.assertEqual(crits.description.comment, 'crits comment')
        # test content
        self.assertEqual(len(crits), 2)
        self.assertEqual(crits[0].id, 'c01')  # xml order must be preserved
        self.assertEqual(crits[1].id, 'c02')

    def test_merge_with_xmcda(self):
        xmcda = XMCDA()
        c01 = Criterion(id='c01')
        xmcda.criteria.append(c01)

        xml = self.read_xml(TestCriteria.xml_2)
        xmcda.criteria.merge_xml(xml)
        # a1 must have been used when loading the xml
        crits = xmcda.criteria
        self.assertEqual(len(crits), 2)
        self.assertEqual(crits[0], c01)  # xml order must be preserved
        self.assertEqual(c01.name, 'n01')  # it has been updated
        self.assertEqual(crits[1].id, 'c02')

    def test_load_with_xmcda(self):
        xmcda = XMCDA()
        c01 = Criterion(id='c01')
        xmcda.criteria.append(c01)

        xmcda.fromstring(TestCriteria.xmcda_2)
        # a1 must have been updated when loading the xml
        crits = xmcda.criteria
        self.assertEqual(len(crits), 2)
        self.assertEqual(crits[0], c01)  # xml order must be preserved
        self.assertEqual(c01.name, 'n01')  # it has been updated
        self.assertEqual(crits[1].id, 'c02')

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestCriteria.xml_1)
        result = utf8_to_utf8(TestCriteria.xml_1, Criteria)
        self.assertEqual(source, result)

        source = compact_xml(TestCriteria.xml_2)
        result = utf8_to_utf8(TestCriteria.xml_2, Criteria)
        self.assertEqual(source, result)
