import xmcda
from xmcda import set_version, version
from xmcda.criteria import Criterion
from xmcda.criteria_scales import CriteriaScales, CriterionScales
from xmcda.scales import ScaleReference, Scales
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, compact_xml, file_to_utf8


class _TestCriterionScales:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml_1 = (  # noqa 731
        lambda s: f'''
        <{s.criterionScales} id="cS1" name="cS1n" mcdaConcept="cS1m">
            <description><comment>meuh</comment></description>
            <criterionID>g1</criterionID>
            <scales>
                <scale>
                    <quantitative>
                        <preferenceDirection>min</preferenceDirection>
                    </quantitative>
                </scale>
                <scale>
                    <nominal>
                        <labels>
                            <label>piou-piou</label>
                        </labels>
                    </nominal>
                </scale>
            </scales>
        </{s.criterionScales}>'''
    )
    xml_1 = property(xml_1)

    def test_init_with_args(self):
        critScales = CriterionScales(id='cSid', attr=99)
        self.assertEqual(critScales.id, 'cSid')
        self.assertEqual(critScales.attr, 99)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        critScales = CriterionScales(xml)

        self.assertEqual(critScales.id, 'cS1')
        self.assertEqual(critScales.name, 'cS1n')
        self.assertEqual(critScales.mcda_concept, 'cS1m')
        self.assertEqual(critScales.criterion.id, 'g1')
        self.assertIsInstance(critScales.scales, Scales)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        g1 = xmcda.criteria['g1']
        critScales = CriterionScales(xml, xmcda)

        self.assertEqual(critScales.criterion, g1)

    xml_empty = lambda s: f'<{s.criterionScales}/>'  # noqa E731
    xml_empty = property(xml_empty)

    xml_empty_serialized = (  # noqa E731
        lambda s: f'<{s.criterionScales}><scales/></{s.criterionScales}>'
    )
    xml_empty_serialized = property(xml_empty_serialized)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriterionScales)

        r = CriterionScales(self.read_xml(self.xml_empty)).to_xml()
        self.assertEqual(xmcda.utils.tostring(r), self.xml_empty_serialized)

        # if scale is None: serialization works as if empty
        r = CriterionScales(self.read_xml(self.xml_empty))
        r.scales = None
        r = r.to_xml()
        self.assertEqual(xmcda.utils.tostring(r), self.xml_empty_serialized)


class TestCriterionScales_v3(_TestCriterionScales, XMCDATestCase):
    version = XMCDA_3_1_1
    criterionScales = 'criterionScale'


class TestCriterionScales_v4(_TestCriterionScales, XMCDATestCase):
    version = XMCDA_4_0_0
    criterionScales = 'criterionScales'


class _TestCriteriaScales:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml_1 = (  # noqa E731
        lambda s: f'''
        <criteriaScales id="cSs1" name="cSs1n" mcdaConcept="cSs1m">
            <description><comment>fsqd</comment></description>
            <{s.criterionScales}>
                <criterionID>g1</criterionID>
                <scales>
                    <scale>
                        <quantitative>
                            <preferenceDirection>min</preferenceDirection>
                        </quantitative>
                    </scale>
                </scales>
            </{s.criterionScales}>
            <{s.criterionScales}>
                <criterionID>g2</criterionID>
                <scales>
                    <scale>
                        <quantitative>
                            <preferenceDirection>max</preferenceDirection>
                        </quantitative>
                    </scale>
                </scales>
            </{s.criterionScales}>
        </criteriaScales>'''
    )
    xml_1 = property(xml_1)

    xmcda_1 = lambda s: s.make_xmcda(s.xml_1)  # noqa E731
    xmcda_1 = property(xmcda_1)

    xml_empty = '<criteriaScales/>'

    xmcda_criteria = lambda s: s.make_xmcda(  # noqa E731
'''
    <criteria id="id1" name="n1" mcdaConcept="m1">
            <criterion id="g1" name="n01" />
            <criterion id="g2" name="n02"><active>false</active></criterion>
    </criteria>
''')
    xmcda_criteria = property(xmcda_criteria)

    def test_init_with_args(self):
        critScales = CriteriaScales(id='cSsid', attr=999)
        self.assertEqual(critScales.id, 'cSsid')
        self.assertEqual(critScales.attr, 999)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        critScales = CriteriaScales(xml)
        self.assertEqual(critScales.id, 'cSs1')
        self.assertEqual(critScales.name, 'cSs1n')
        self.assertEqual(critScales.mcda_concept, 'cSs1m')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        g1 = xmcda.criteria['g1']
        critScales = CriteriaScales(xml, xmcda)

        self.assertEqual(critScales[0].criterion, g1)

    def test_load_criteriaScales(self):
        # load the criteriaScales, and the criteria afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.criteria), 2)

        g2 = xmcda.criteria['g2']
        self.assertEqual(g2.name, None)
        self.assertTrue(g2.active)

        xmcda.fromstring(self.xmcda_criteria)
        self.assertEqual(len(xmcda.criteria), 2)
        self.assertEqual(g2, xmcda.criteria['g2'])
        self.assertEqual(g2.name, 'n02')
        self.assertFalse(g2.active)

        # load the criteria, and the criteriaScales afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_criteria)
        self.assertEqual(len(xmcda.criteria), 2)
        g2 = xmcda.criteria['g2']
        self.assertEqual(g2.name, 'n02')
        self.assertFalse(g2.active)

        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.criteria), 2)
        self.assertEqual(g2, xmcda.criteria['g2'])
        self.assertEqual(g2.name, 'n02')
        self.assertFalse(g2.active)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriteriaScales)
        self._test_to_xml(self.xml_empty, CriteriaScales)

    def test_get_criterion_scales(self):
        critScales = CriteriaScales()
        s1 = CriterionScales(id="s1")
        s1a = CriterionScales(id="s1")
        s2 = CriterionScales(id="s2")
        s3 = CriterionScales()
        critScales.append(s1)
        critScales.append(s2)
        critScales.append(s3)
        critScales.append(s1a)

        self.assertIs(critScales.get_criterion_scales("s1"), s1)
        self.assertIs(critScales.get_criterion_scales("s2"), s2)
        self.assertIsNone(critScales.get_criterion_scales("unknown"))

    def test_get_criterion_scales_2(self):
        "Test the function w/ parameter criterion_id"
        xml = self.read_xml(self.xml_1)
        cScales = CriteriaScales(xml)
        cScales.append(CriterionScales())

        self.assertIs(cScales.get_criterion_scales(criterion_id="g2"),
                      cScales[1])
        self.assertIsNone(cScales.get_criterion_scales(criterion_id="unknown"))

    def test_get_criterion_scales_3(self):
        "Test the function w/ parameter criterion"
        critScales = CriteriaScales()
        s1 = CriterionScales(id="s1")
        s2 = CriterionScales(id="s2")
        s3 = CriterionScales()
        critScales.append(s1)
        critScales.append(s2)
        critScales.append(s3)
        c2 = Criterion(id="c2")
        s2.criterion = c2

        self.assertIs(critScales.get_criterion_scales(criterion=c2), s2)
        c2bis = Criterion(id="c2")
        self.assertIsNone(critScales.get_criterion_scales(criterion=c2bis))


class TestCriteriaScales_v3(_TestCriteriaScales, XMCDATestCase):
    version = XMCDA_3_1_1
    criterionScales = 'criterionScale'
    make_xmcda = XMCDATestCase.make_xmcda_v3


class TestCriteriaScales_v4(_TestCriteriaScales, XMCDATestCase):
    version = XMCDA_4_0_0
    criterionScales = 'criterionScales'
    make_xmcda = XMCDATestCase.make_xmcda_v4

    xml_with_ref = '''
        <criteriaScales id="cSs1" name="cSs1n" mcdaConcept="cSs1m">
            <description><comment>fsqd</comment></description>
            <criterionScales>
                <criterionID>g1</criterionID>
                <scales>
                    <scaleID>scale_id_1</scaleID>
                </scales>
            </criterionScales>
            <criterionScales>
                <criterionID>g2</criterionID>
                <scales>
                    <scale id="scale_id_1">
                        <quantitative>
                            <preferenceDirection>max</preferenceDirection>
                        </quantitative>
                    </scale>
                </scales>
            </criterionScales>
            <criterionScales>
                <criterionID>g3</criterionID>
                <scales>
                    <scale id="scale_id_1"><!-- same id -->
                        <quantitative>
                            <preferenceDirection>max</preferenceDirection>
                        </quantitative>
                    </scale>
                </scales>
            </criterionScales>
            <criterionScales>
                <criterionID>g1</criterionID>
                <scales>
                    <scaleID>scale_id_1</scaleID>
                </scales>
            </criterionScales>
        </criteriaScales>'''

    def test_with_reference(self):
        xml = self.read_xml(self.xml_with_ref)
        criteria_scales = CriteriaScales(xml)

        for criterion_scales in criteria_scales:
            for scale in criterion_scales.scales:
                self.assertNotIsInstance(scale, ScaleReference)
        self.assertIs(criteria_scales[0].scales[0],
                      criteria_scales[1].scales[0])
        self.assertIsNot(criteria_scales[0].scales[0],
                         criteria_scales[2].scales[0])
        # the last ref. to scale_id_1 point to the 1st occurence
        self.assertIs(criteria_scales[3].scales[0],
                      criteria_scales[1].scales[0])

    def test_with_reference_from_file(self):
        xmcda = XMCDA()
        xmcda.load("tests/files/v4/criteriaScales.fuzzyNumbers.xml")
        cSc1 = xmcda.criteria_scales_list[0]
        cSc2 = xmcda.criteria_scales_list[1]

        # defined then referenced
        cS_c01 = cSc1.get_criterion_scales(criterion_id="c01")
        cS_c01b = cSc1.get_criterion_scales(criterion_id="c01b")
        self.assertIs(cS_c01.scales[0], cS_c01b.scales[0])

        # referenced before being defined
        cS_g9a = cSc1.get_criterion_scales(criterion_id="g9a")
        cS_g9 = cSc1.get_criterion_scales(criterion_id="g9")
        self.assertIs(cS_g9.scales[0], cS_g9a.scales[0])

        # referenced but not defined anywhere
        cS_g9b = cSc1.get_criterion_scales(criterion_id=("g9b"))
        self.assertIsInstance(cS_g9b.scales[0], ScaleReference)
        self.assertEqual("g9s", cS_g9b.scales[0].ref_id)

        # referenced but not defined in its criteriaScales
        cS2_c01 = cSc2.get_criterion_scales(criterion_id="c01")
        self.assertIsNot(cS_c01, cS2_c01)
        self.assertIsInstance(cS2_c01.scales[0], ScaleReference)
        self.assertEqual("fuzzy_scales", cS2_c01.scales[0].ref_id)

        v4dir = "tests/files/v4"
        expected = (
            f"{v4dir}/criteriaScales.fuzzyNumbers.expected-serialization.xml"
        )
        with open(expected, 'r') as f:
            expected = compact_xml(f.read())
        self.assertEqual(
            expected,
            file_to_utf8(f"{v4dir}/criteriaScales.fuzzyNumbers.xml",
                         tags="criteriaScales")
        )
