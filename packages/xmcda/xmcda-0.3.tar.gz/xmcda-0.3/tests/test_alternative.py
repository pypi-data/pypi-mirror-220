import xmcda
from xmcda.alternatives import Alternative
from xmcda.description import Description

from .utils import XMCDATestCase


class TestAlternative(XMCDATestCase):

    xml_1 = '''
<alternative id="a01" name="n01" mcdaConcept="m01">
    <description>
        <comment>a01 comment</comment>
    </description>
    <type>fictive</type>
    <active>false</active>
</alternative>
'''

    xml_2 = '<alternative id="a02" name="n02"/>'  # check default values

    def setUp(self):
        # restore defaults
        xmcda.reset_settings()

    def test_init(self):
        a = Alternative()
        self.assertIsNone(a.id)
        self.assertIsNone(a.name)
        self.assertIsNone(a.mcda_concept)
        self.assertTrue(a.is_real)
        self.assertTrue(a.active)
        self.assertIsNone(a.description)

    def test_init_with_values(self):
        a = Alternative(id='a01', name='n01', mcda_concept='m01', active=False)
        self.assertEqual(a.id, 'a01')
        self.assertEqual(a.name, 'n01')
        self.assertEqual(a.mcda_concept, 'm01')
        self.assertTrue(a.is_real)
        self.assertFalse(a.active)

    def test_is_real_not_none(self):
        a = Alternative()
        a.is_real = None
        self.assertEqual(a.is_real, True)

    def test_active_not_none(self):
        a = Alternative()
        a.active = None
        self.assertEqual(a.active, True)

    def test_str(self):
        a = Alternative()
        self.assertEqual(str(a), "Alternative()")
        a = Alternative(id='a1', name='n1', mcda_concept='m1', active=False)
        self.assertEqual(str(a),
                         "Alternative(id='a1', name='n1', mcda_concept='m1')")

    def test_repr(self):
        a = Alternative()
        self.assertTrue(repr(a), "<Alternative at ")

    def _test_load_xml_1(self, a):
        self.assertIsNotNone(a)
        self.assertEqual(a.id, 'a01')
        self.assertEqual(a.name, 'n01')
        self.assertEqual(a.mcda_concept, 'm01')
        self.assertFalse(a.active)
        self.assertFalse(a.is_real)
        self.assertIsInstance(a.description, Description)
        self.assertEqual(a.description.comment, 'a01 comment')

    def test_load_xml_1_constructor(self):
        element = self.read_xml(TestAlternative.xml_1)

        a = Alternative(element)
        self._test_load_xml_1(a)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestAlternative.xml_1)
        result = utf8_to_utf8(TestAlternative.xml_1, Alternative)
        self.assertEqual(source, result)

        source = compact_xml(TestAlternative.xml_2)
        result = utf8_to_utf8(TestAlternative.xml_2, Alternative)
        self.assertEqual(source, result)
