from xmcda import set_version, version
from xmcda.criteria_sets import CriteriaSet
from xmcda.criteria_sets_values import CriteriaSetsValues, CriteriaSetValues
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestCriteriaSetValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml = (  # noqa E731
        lambda s: f'''
        <{s.criteriaSetValues} id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <criteriaSetID>o1</criteriaSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </{s.criteriaSetValues}>'''
    )
    xml = property(xml)

    xml_empty = lambda s: f'<{s.criteriaSetValues}/>'  # noqa E731
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        criteria_set_values = CriteriaSetValues(self.read_xml(self.xml))
        self.assertEqual(criteria_set_values.id, 'v1')
        self.assertEqual(criteria_set_values.name, 'v1-n')
        self.assertEqual(criteria_set_values.mcda_concept, 'v1-m')
        self.assertEqual(criteria_set_values.description.comment, 'v1-c')
        self.assertIsInstance(criteria_set_values.values, Values)
        self.assertEqual(len(criteria_set_values.values), 2)
        self.assertEqual(criteria_set_values.values[0].v, 1)
        self.assertEqual(criteria_set_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.criteria_sets['o1']
        criteria_set_values = (
          CriteriaSetValues(self.read_xml(self.xml), xmcda))
        self.assertEqual(criteria_set_values.criteria_set, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CriteriaSetValues)
        # accept to read/write an empty tag
        self._test_to_xml(self.xml_empty, CriteriaSetValues)


class TestCriteriaSetValue_v3(_TestCriteriaSetValues, XMCDATestCase):
    version = XMCDA_3_1_1
    criteriaSetValues = 'criteriaSetValue'


class TestCriteriaSetValue_v4(_TestCriteriaSetValues, XMCDATestCase):
    version = XMCDA_4_0_0
    criteriaSetValues = 'criteriaSetValues'


class _TestCriteriaSetsValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)


    xml = (  # noqa E731
        lambda s: f'''
    <criteriaSetsValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.criteriaSetValues} id="v1">
            <criteriaSetID>o1</criteriaSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.criteriaSetValues}>
        <{s.criteriaSetValues} id="v2">
            <criteriaSetID>o2</criteriaSetID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.criteriaSetValues}>
    </criteriaSetsValues>'''
    )
    xml = property(xml)

    xml_empty = '<criteriaSetsValues/>'

    def test_init_with_args(self):
        criteria_sets_values = CriteriaSetsValues(id='csv1', attr=12)
        self.assertEqual(criteria_sets_values.id, 'csv1')
        self.assertEqual(criteria_sets_values.attr, 12)

    def test_from_xml(self):
        criteria_sets_values = \
            CriteriaSetsValues(self.read_xml(self.xml))
        self.assertEqual(criteria_sets_values.id, 'vs1')
        self.assertEqual(criteria_sets_values.name, 'vs1-n')
        self.assertEqual(criteria_sets_values.mcda_concept, 'vs1-m')
        self.assertEqual(criteria_sets_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(criteria_sets_values), 2)
        for criteria_set_values in criteria_sets_values:
            self.assertIsInstance(criteria_set_values,
                                  CriteriaSetValues)
        self.assertEqual(criteria_sets_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.criteria_sets['o2']
        criteria_sets_values = \
            CriteriaSetsValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(criteria_sets_values), 2)
        self.assertEqual({c.id for c in xmcda.criteria_sets},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(criteria_sets_values[1].criteria_set),
                         id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, CriteriaSetsValues)
        self._test_to_xml(self.xml_empty, CriteriaSetsValues)

    def test_get_item(self):
        criteria_sets_values = \
            CriteriaSetsValues(self.read_xml(self.xml))
        self.assertEqual(criteria_sets_values[0].id, 'v1')
        self.assertEqual(criteria_sets_values['o2'].criteria_set.id,
                         'o2')
        self.assertEqual(criteria_sets_values['o2'].criteria_set.id,
                         criteria_sets_values[1].criteria_set.id)
        o1 = criteria_sets_values[0].criteria_set
        self.assertEqual(criteria_sets_values[o1],
                         criteria_sets_values[0])

        with self.assertRaises(IndexError):
            criteria_sets_values[CriteriaSet(id='unknown')]
        with self.assertRaises(IndexError):
            criteria_sets_values['unknown']

        with self.assertRaises(TypeError):
            criteria_sets_values[None]
        with self.assertRaises(TypeError):
            criteria_sets_values[2.3]

    def test_set_item(self):
        criteria_sets_values = \
            CriteriaSetsValues(self.read_xml(self.xml))
        value_1 = criteria_sets_values[0]
        value_2 = criteria_sets_values[1]
        criteriaSet_1 = value_1.criteria_set
        criteriaSet_2 = value_2.criteria_set
        criteriaSet_3 = CriteriaSet(id='o3')
        value_3 = CriteriaSetValues(id='v3')
        value_3.criteria_set = criteriaSet_3
        value_3.value = Values('moo')

        criteria_sets_values[0] = value_3
        self.assertEqual(criteria_sets_values[0].value[0].v, 'moo')

        criteria_sets_values[criteriaSet_2] = value_3
        self.assertEqual(criteria_sets_values[1], value_3)

        with self.assertRaises(IndexError):
            criteria_sets_values[CriteriaSet(id='unknown')] = value_2

        with self.assertRaises(IndexError):
            criteria_sets_values['o1'] = value_2

        value_3.criteria_set = criteriaSet_1
        criteria_sets_values['o1'] = value_2
        self.assertEqual(criteria_sets_values[0], value_2)

        with self.assertRaises(TypeError):
            criteria_sets_values[None] = value_1
        with self.assertRaises(TypeError):
            criteria_sets_values[2.3] = value_1


class TestCriteriaSetsValue_v3(_TestCriteriaSetsValues, XMCDATestCase):
    version = XMCDA_3_1_1
    criteriaSetValues = 'criteriaSetValue'


class TestCriteriaSetsValue_v4(_TestCriteriaSetsValues, XMCDATestCase):
    version = XMCDA_4_0_0
    criteriaSetValues = 'criteriaSetValues'
