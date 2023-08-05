import xmcda
from xmcda import set_version, version
from xmcda.criteria_thresholds import CriteriaThresholds, CriterionThresholds
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.thresholds import AffineThreshold, ConstantThreshold, Thresholds
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestCriterionThresholds:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml_1 = (  # noqa E731
        lambda s: f'''
        <{s.criterionThresholds} id="cS1" name="cS1n" mcdaConcept="cS1m">
            <description><comment>meuh</comment></description>
            <criterionID>g1</criterionID>
            <thresholds>
                <description><comment>thresholds desc</comment></description>
                <threshold id="indifference">
                    <constant>
                        <real>2.5</real>
                    </constant>
                </threshold>
                <threshold id="preference">
                    <affine>
                        <type>direct</type>
                        <slope>
                            <real>1.0</real>
                        </slope>
                        <intercept>
                            <integer>2</integer>
                        </intercept>
                    </affine>
                </threshold>
            </thresholds>
        </{s.criterionThresholds}>'''
    )
    xml_1 = property(xml_1)

    def test_init_with_kw(self):
        critThresholds = CriterionThresholds(id='cT', attr=4)
        self.assertEqual(critThresholds.id, 'cT')
        self.assertEqual(critThresholds.attr, 4)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        critThresholds = CriterionThresholds(xml)

        self.assertEqual(critThresholds.id, 'cS1')
        self.assertEqual(critThresholds.name, 'cS1n')
        self.assertEqual(critThresholds.mcda_concept, 'cS1m')
        self.assertEqual(critThresholds.criterion.id, 'g1')
        self.assertIsInstance(critThresholds.thresholds, Thresholds)

        self.assertIsNotNone(critThresholds.thresholds.description)
        self.assertEqual(critThresholds.thresholds.description.comment,
                         "thresholds desc")

        ind = critThresholds.thresholds[0]
        pref = critThresholds.thresholds[1]
        self.assertIsInstance(ind, ConstantThreshold)
        self.assertIsInstance(pref, AffineThreshold)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        g1 = xmcda.criteria['g1']
        critThresholds = CriterionThresholds(xml, xmcda)

        self.assertEqual(critThresholds.criterion, g1)

    xml_empty = lambda s: f'<{s.criterionThresholds}/>'  # noqa E731
    xml_empty = property(xml_empty)

    xml_empty_serialized = (  # noqa E731
        lambda s: f'''
          <{s.criterionThresholds}><thresholds/></{s.criterionThresholds}>
        '''.strip()
    )
    xml_empty_serialized = property(xml_empty_serialized)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriterionThresholds)

        r = CriterionThresholds(self.read_xml(self.xml_empty)).to_xml()
        self.assertEqual(xmcda.utils.tostring(r), self.xml_empty_serialized)

        # even if thresholds is None, serialize it the same way
        r = CriterionThresholds(self.read_xml(self.xml_empty))
        r.thresholds = None
        r = r.to_xml()
        self.assertEqual(xmcda.utils.tostring(r), self.xml_empty_serialized)


class TestCriterionThresholds_v3(_TestCriterionThresholds, XMCDATestCase):
    version = XMCDA_3_1_1
    criterionThresholds = 'criterionThreshold'


class TestCriterionThresholds_v4(_TestCriterionThresholds, XMCDATestCase):
    version = XMCDA_4_0_0
    criterionThresholds = 'criterionThresholds'


class _TestCriteriaThresholds:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    # no description in <thresholds> here: test for the description is
    # in TestCriterionThreshold
    xml_1 = (  # noqa E731
        lambda s: f'''
        <criteriaThresholds id="cSs1" name="cSs1n" mcdaConcept="cSs1m">
            <description><comment>blah</comment></description>
            <{s.criterionThresholds}>
                <criterionID>g1</criterionID>
                <thresholds>
                    <threshold id="indifference">
                        <constant>
                            <real>2.5</real>
                        </constant>
                    </threshold>
                </thresholds>
            </{s.criterionThresholds}>
            <{s.criterionThresholds}>
                <criterionID>g2</criterionID>
                <thresholds>
                    <threshold id="indifference">
                        <constant>
                            <real>20.0</real>
                        </constant>
                    </threshold>
                </thresholds>
            </{s.criterionThresholds}>
        </criteriaThresholds>'''
    )
    xml_1 = property(xml_1)

    xmcda_1 = lambda s: s.make_xmcda(s.xml_1)  # noqa E731
    xmcda_1 = property(xmcda_1)

    xmcda_criteria = lambda s: s.make_xmcda(  # noqa E731
'''
    <criteria id="id1" name="n1" mcdaConcept="m1">
        <description><comment>crits comment</comment></description>
            <criterion id="g1" name="n01" />
            <criterion id="g2" name="n02"><active>false</active></criterion>
    </criteria>
''')
    xmcda_criteria = property(xmcda_criteria)

    def test_init_with_kw(self):
        critThresholds = CriteriaThresholds(id='cTs', attr=44)
        self.assertEqual(critThresholds.id, 'cTs')
        self.assertEqual(critThresholds.attr, 44)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        critThresholds = CriteriaThresholds(xml)
        self.assertEqual(critThresholds.id, 'cSs1')
        self.assertEqual(critThresholds.name, 'cSs1n')
        self.assertEqual(critThresholds.mcda_concept, 'cSs1m')
        self.assertIsNone(critThresholds[0].thresholds.description)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        g1 = xmcda.criteria['g1']
        critThresholds = CriteriaThresholds(xml, xmcda)

        self.assertEqual(critThresholds[0].criterion, g1)

    def test_load_criteriaThresholds(self):
        # load the criteriaThresholds, and the criteria afterwards
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

        # load the criteria, and the criteriaThresholds afterwards
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

    xml_empty = '<criteriaThresholds/>'

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriteriaThresholds)
        self._test_to_xml(self.xml_empty, CriteriaThresholds)


class TestCriteriaThresholds_v3(_TestCriteriaThresholds, XMCDATestCase):
    version = XMCDA_3_1_1
    criterionThresholds = 'criterionThreshold'
    make_xmcda = XMCDATestCase.make_xmcda_v3


class TestCriteriaThresholds_v4(_TestCriteriaThresholds, XMCDATestCase):
    version = XMCDA_4_0_0
    criterionThresholds = 'criterionThresholds'
    make_xmcda = XMCDATestCase.make_xmcda_v4
