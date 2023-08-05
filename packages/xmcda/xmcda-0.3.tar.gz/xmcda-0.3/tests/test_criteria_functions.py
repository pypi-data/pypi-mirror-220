import xmcda
from xmcda import set_version, version
from xmcda.criteria_functions import CriteriaFunctions, CriterionFunctions
from xmcda.functions import Functions
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class _TestCriterionFunctions:

    def test_init_with_kw(self):
        criterion_functions = CriterionFunctions(id='cF', attr=77)
        self.assertEqual(criterion_functions.id, 'cF')
        self.assertEqual(criterion_functions.attr, 77)

    xml_1 = (  # noqa E731
        lambda s: f'''
        <{s.criterionFunctions} id="cF1" name="cF1n" mcdaConcept="cF1m">
            <description><comment>bla</comment></description>
            <criterionID>o1</criterionID>
            <functions>
                <function>
                    <discrete>
                        <point>
                            <abscissa>
                                <real>0.0</real>
                            </abscissa>
                            <ordinate>
                                <real>0.0</real>
                            </ordinate>
                        </point>
                        <point>
                            <abscissa>
                                <real>21334.0</real>
                            </abscissa>
                            <ordinate>
                                <real>1.0</real>
                            </ordinate>
                        </point>
                    </discrete>
                </function>
            </functions>
      </{s.criterionFunctions}>'''
    )
    xml_1 = property(xml_1)

    xml_empty = (  # noqa E731
        lambda s: f'''
<{s.criterionFunctions}>
    <criterionID>o1</criterionID>
    <functions/>
</{s.criterionFunctions}>'''
    )
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        criterion_functions = CriterionFunctions(xml)

        self.assertEqual(criterion_functions.id, 'cF1')
        self.assertEqual(criterion_functions.name, 'cF1n')
        self.assertEqual(criterion_functions.mcda_concept, 'cF1m')
        self.assertEqual(criterion_functions.criterion.id, 'o1')
        self.assertEqual(criterion_functions.description.comment, 'bla')
        self.assertIsInstance(criterion_functions.functions, Functions)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        o1 = xmcda.criteria['o1']
        criterion_functions = CriterionFunctions(xml, xmcda)

        self.assertEqual(criterion_functions.criterion, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriterionFunctions)
        self._test_to_xml(self.xml_empty, CriterionFunctions)

        criterion_functions = CriterionFunctions()
        self.assertEqual(
            f'<{self.criterionFunctions}/>',
            xmcda.utils.tostring(criterion_functions.to_xml()))


class TestCriterionFunctions_v3(_TestCriterionFunctions, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.criterionFunctions = 'criterionFunction'

    def tearDown(self):
        set_version(self.current_version)


class TestCriterionFunctions_v4(_TestCriterionFunctions, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.criterionFunctions = 'criterionFunctions'

    def tearDown(self):
        set_version(self.current_version)


class _TestCriteriaFunctions:

    def test_init_with_kw(self):
        criteria_functions = CriteriaFunctions(id='cFs', attr=777)
        self.assertEqual(criteria_functions.id, 'cFs')
        self.assertEqual(criteria_functions.attr, 777)

    xml_1 = (  # noqa E731
        lambda s: f'''
    <criteriaFunctions id="cFs1" name="cFs1n" mcdaConcept="cFs1m">
        <description><comment>cFs1 comment</comment></description>
        <{s.criterionFunctions}>
            <criterionID>o1</criterionID>
            <functions>
                <function>
                    <constant>
                        <integer>3210</integer>
                    </constant>
                </function>
            </functions>
        </{s.criterionFunctions}>
        <{s.criterionFunctions}>
            <criterionID>o2</criterionID>
            <functions>
                <function>
                    <constant>
                        <integer>2222</integer>
                    </constant>
                </function>
            </functions>
        </{s.criterionFunctions}>
    </criteriaFunctions>'''
    )
    xml_1 = property(xml_1)

    xmcda_1 = lambda s: s.make_xmcda_v4(s.xml_1)  # noqa E731
    xmcda_1 = property(xmcda_1)

    xmcda_criteria = lambda s: s.make_xmcda_v4(  # noqa E731
'''
    <criteria id="id1" name="n1" mcdaConcept="m1">
        <criterion id="o1" name="n01" />
        <criterion id="o2" name="n02"><active>false</active></criterion>
    </criteria>
''')
    xmcda_criteria = property(xmcda_criteria)
    xml_empty = '<criteriaFunctions/>'

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        criteria_functions = CriteriaFunctions(xml)
        self.assertEqual(criteria_functions.id, 'cFs1')
        self.assertEqual(criteria_functions.name, 'cFs1n')
        self.assertEqual(criteria_functions.mcda_concept, 'cFs1m')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        o1 = xmcda.criteria['o1']
        criteria_functions = CriteriaFunctions(xml, xmcda)

        self.assertEqual(criteria_functions[0].criterion, o1)

    def test_load_criteriaFunctions(self):
        # load the criteriaFunctions, and the criteria afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.criteria), 2)

        o2 = xmcda.criteria['o2']
        self.assertEqual(o2.name, None)
        self.assertTrue(o2.active)

        xmcda.fromstring(self.xmcda_criteria)
        self.assertEqual(len(xmcda.criteria), 2)
        self.assertEqual(o2, xmcda.criteria['o2'])
        self.assertEqual(o2.name, 'n02')
        self.assertFalse(o2.active)

        # load the criteria, and the criteriaFunctions afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_criteria)
        self.assertEqual(len(xmcda.criteria), 2)
        o2 = xmcda.criteria['o2']
        self.assertEqual(o2.name, 'n02')
        self.assertFalse(o2.active)

        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.criteria), 2)
        self.assertEqual(o2, xmcda.criteria['o2'])
        self.assertEqual(o2.name, 'n02')
        self.assertFalse(o2.active)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CriteriaFunctions)
        self._test_to_xml(self.xml_empty, CriteriaFunctions)


class TestCriteriaFunctions_v3(_TestCriteriaFunctions, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.criterionFunctions = 'criterionFunction'

    def tearDown(self):
        set_version(self.current_version)

    def make_xmcda_v4(self, text):
        return f'''
<xmcda:XMCDA xmlns:xmcda="http://www.decision-deck.org/2019/XMCDA-3.1.1">
    {text}
</xmcda:XMCDA>'''


class TestCriteriaFunctions_v4(_TestCriteriaFunctions, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.criterionFunctions = 'criterionFunctions'

    def tearDown(self):
        set_version(self.current_version)

    def make_xmcda_v4(self, text):
        return make_xmcda_v4(text)
