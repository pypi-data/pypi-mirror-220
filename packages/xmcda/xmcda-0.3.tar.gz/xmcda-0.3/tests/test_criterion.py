import xmcda
from xmcda.criteria import Criterion
from xmcda.description import Description

from .utils import XMCDATestCase, compact_xml, utf8_to_utf8


class TestCriterion(XMCDATestCase):

    xml_1 = '''
<criterion id="c01" name="n1" mcdaConcept="m1">
    <description><comment>c01 criterion</comment></description>
    <active>false</active>
</criterion>'''

    xml_2 = '<criterion id="c02"/>'  # check default values

    def setUp(self):
        # restore defaults
        xmcda.reset_settings()

    def test_init(self):
        c = Criterion()
        self.assertIsNone(c.id)
        self.assertIsNone(c.name)
        self.assertIsNone(c.mcda_concept)
        self.assertTrue(c.active)
        self.assertIsNone(c.description)

    def test_init_with_values(self):
        c = Criterion(id='i', name='n', mcda_concept='m', active=False)
        self.assertEqual(c.id, 'i')
        self.assertEqual(c.name, 'n')
        self.assertEqual(c.mcda_concept, 'm')
        self.assertEqual(c.active, False)

    def test_active_not_none(self):
        c = Criterion()
        c.active = None
        self.assertEqual(c.active, True)

    def test_str(self):
        c = Criterion()
        self.assertEqual(str(c), "Criterion()")
        c = Criterion(id='c1', name='n1', mcda_concept='m1', active=False)
        self.assertEqual(str(c),
                         "Criterion(id='c1', name='n1', mcda_concept='m1')")

    def test_repr(self):
        c = Criterion()
        self.assertTrue(repr(c), "<Criterion at ")

    def _test_load_xml_1(self, c):
        self.assertEqual(c.id, 'c01')
        self.assertEqual(c.name, 'n1')
        self.assertEqual(c.mcda_concept, 'm1')
        self.assertFalse(c.active)
        self.assertIsInstance(c.description, Description)
        self.assertEqual(c.description.comment, 'c01 criterion')

    def test_load_xml_1_instance_method(self):
        element = self.read_xml(TestCriterion.xml_1)

        c = Criterion(element)
        self._test_load_xml_1(c)

    def test_load_xml_1_class_method(self):
        element = self.read_xml(TestCriterion.xml_1)

        c = Criterion.build(element)
        self._test_load_xml_1(c)

    def test_load_xml_2(self):
        xml = self.read_xml(TestCriterion.xml_2)

        c = Criterion(xml)
        self.assertEqual(c.id, 'c02')
        self.assertIsNone(c.name)
        self.assertIsNone(c.mcda_concept)
        self.assertTrue(c.active)
        self.assertIsNone(c.description)

    def test_to_xml(self):
        source = compact_xml(TestCriterion.xml_1)
        result = utf8_to_utf8(TestCriterion.xml_1, Criterion)
        self.assertEqual(source, result)

        source = compact_xml(TestCriterion.xml_2)
        result = utf8_to_utf8(TestCriterion.xml_2, Criterion)
        self.assertEqual(source, result)
