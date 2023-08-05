from xmcda.alternatives import Alternative, Alternatives
from xmcda.description import Description
from xmcda.schemas import XMCDA_4_0_0
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestAlternatives(XMCDATestCase):

    xml_1 = '<alternatives><alternative id="a01"/></alternatives>'

    xml_2 = '''
<alternatives id="id1" name="n1" mcdaConcept="m1">
    <description><comment>42</comment></description>
    <alternative id="a01" name="na01"/>
    <alternative id="a02" name="na02"><active>false</active></alternative>
</alternatives>'''

    xmcda_2 = f'<xmcda xmlns="{XMCDA_4_0_0.id}">{xml_2}</xmcda>'

    xmcda_3 = '''
<xmcda xmlns="http://www.decision-deck.org/2021/XMCDA-4.0.0">
    <alternatives id='id_xmcda_3'>
        <alternative id="a01" name="na01"/>
    </alternatives>
</xmcda>'''

    def tearDown(self):
        # restore defaults
        import xmcda
        xmcda.reset_settings()

    def _test_defaults(self, alts):
        for a in ('id', 'name', 'mcda_concept', 'description'):
            self.assertIsNone(getattr(alts, a))

    def test_init(self):
        alts = Alternatives()
        self._test_defaults(alts)
        self.assertEqual(Alternatives(id='id_alts').id, 'id_alts')

    def test_getitem_int(self):
        alternatives = Alternatives()
        a = Alternative(id='id_a')
        alternatives.append(a)
        self.assertEqual(alternatives[0], a)

    def test_getitem_by_id(self):
        alternatives = Alternatives()
        a01 = Alternative(id='a01')
        alternatives.append(a01)
        self.assertEqual(alternatives[a01.id], a01)

    def test_getitem_str_automatic_creation(self):
        alternatives = Alternatives()
        a01 = Alternative(id='a01')
        self.assertIsNotNone(a01)

        import xmcda
        xmcda.set_create_on_access(False, 'alternative')
        with self.assertRaises(IndexError):
            alternatives['cui-cui']

    def test_load_xml_1(self):
        xml = self.read_xml(TestAlternatives.xml_1)
        alts = Alternatives(xml)

        self._test_defaults(alts)
        self.assertEqual(len(alts), 1)
        self.assertEqual(alts[0].id, 'a01')

    def test_load_xml_2(self):
        xml = self.read_xml(TestAlternatives.xml_2)
        alts = Alternatives(xml)
        self.assertEqual(alts.id, 'id1')
        self.assertEqual(alts.name, 'n1')
        self.assertEqual(alts.mcda_concept, 'm1')
        self.assertIsNotNone(alts.description)
        self.assertIsInstance(alts.description, Description)
        self.assertEqual(alts.description.comment, '42')
        # test content
        self.assertEqual(len(alts), 2)
        self.assertEqual(alts[0].id, 'a01')  # preserve xml order
        self.assertEqual(alts[1].id, 'a02')

    def test_load_with_xmcda(self):
        xmcda = XMCDA()
        a01 = Alternative(id='a01')
        xmcda.alternatives.append(a01)

        xml = self.read_xml(TestAlternatives.xml_2)
        xmcda.alternatives.merge_xml(xml)
        # a1 must have been used when loading the xml
        alts = xmcda.alternatives
        self.assertEqual(len(alts), 2)
        self.assertEqual(alts[0], a01)  # xml order must be preserved
        self.assertEqual(alts[1].id, 'a02')

    def test_to_xml_1(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestAlternatives.xml_1)

        result = utf8_to_utf8(TestAlternatives.xml_1, Alternatives)
        self.assertEqual(source, result)

    def test_to_xml_2(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(TestAlternatives.xml_2)

        result = utf8_to_utf8(TestAlternatives.xml_2, Alternatives)
        self.assertEqual(source, result)

    def test_merge(self):
        '''
        Tests that Alternative objects are enhanced, not replaced when an
        Alternatives object is merged into an other one
        '''
        xmcda = XMCDA()
        a01 = Alternative(id='a01')
        xmcda.alternatives.append(a01)
        self.assertEqual(a01.name, None)

        xml = self.read_xml(TestAlternatives.xml_2)
        xmcda.alternatives.merge_xml(xml)

        # a01 should have been updated with a new name, not replaced
        a01_bis = xmcda.alternatives['a01']
        self.assertEqual(a01, a01_bis)
        self.assertEqual(a01.name, 'na01')

    def test_load_xmcda_2(self):
        '''
        Tests that Alternative objects are enhanced, not replaced when a
        XMCDA object loads an other file containing alternatives
        '''
        xmcda = XMCDA()
        a01 = Alternative(id='a01')
        xmcda.alternatives.append(a01)
        self.assertEqual(a01.name, None)

        xmcda.fromstring(TestAlternatives.xmcda_2)

        self.assertEqual(xmcda.alternatives.id, 'id1')
        # a01 should have been updated with a new name, not replaced
        a01_bis = xmcda.alternatives['a01']
        self.assertEqual(a01, a01_bis)
        self.assertEqual(a01.name, 'na01')

    def test_load_xmcda_3(self):
        '''
        Tests that Alternative objects are enhanced, not replaced when a
        XMCDA object loads an other file containing alternatives

        '''
        xmcda = XMCDA()
        a01 = Alternative(id='a01')
        xmcda.alternatives.append(a01)
        self.assertEqual(a01.name, None)

        xmcda.fromstring(TestAlternatives.xmcda_3)
        # TODO decide if this loading an alternatives with a different
        # id updates its name (curent behaviour), or if it should be denied
        # (+ same for categories, criteria, alternatives_sets etc.)
        self.assertEqual(xmcda.alternatives.id, 'id_xmcda_3')

        # a01 should have been updated with a new name, not replaced
        a01_bis = xmcda.alternatives['a01']
        self.assertEqual(a01, a01_bis)
        self.assertEqual(a01.name, 'na01')
