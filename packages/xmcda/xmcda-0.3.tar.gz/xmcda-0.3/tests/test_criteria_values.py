from xmcda import set_version, version
from xmcda.criteria import Criterion
from xmcda.criteria_values import CriteriaValues, CriterionValues
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestCriterionValue:

    xml = (  # noqa E731
        lambda s: f'''
        <{s.criterionValues} id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <criterionID>o1</criterionID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </{s.criterionValues}>'''
    )
    xml = property(xml)

    xml_empty = (  # noqa E731
        lambda s: f'<{s.criterionValues}/>'
    )
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        criterion_value = CriterionValues(self.read_xml(self.xml))
        self.assertEqual(criterion_value.id, 'v1')
        self.assertEqual(criterion_value.name, 'v1-n')
        self.assertEqual(criterion_value.mcda_concept, 'v1-m')
        self.assertEqual(criterion_value.description.comment, 'v1-c')
        self.assertIsInstance(criterion_value.values, Values)
        self.assertEqual(len(criterion_value.values), 2)
        self.assertEqual(criterion_value.values[0].v, 1)
        self.assertEqual(criterion_value.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        criterion_value = CriterionValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(criterion_value.criterion, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CriterionValues)
        self._test_to_xml(self.xml_empty, CriterionValues)

    def test_is_numeric(self):
        criterion_value = CriterionValues(self.read_xml(self.xml))
        self.assertTrue(criterion_value.is_numeric())
        criterion_value.values[1] = Value('a string')
        self.assertFalse(criterion_value.is_numeric())


class TestCriterionValue_v3(_TestCriterionValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.criterionValues = 'criterionValue'

    def tearDown(self):
        set_version(self.current_version)


class TestCriterionValue_v4(_TestCriterionValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.criterionValues = 'criterionValues'

    def tearDown(self):
        set_version(self.current_version)


class _TestCriteriaValues:

    xml = (  # noqa E731
        lambda s: f'''
    <criteriaValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.criterionValues} id="v1">
            <criterionID>o1</criterionID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.criterionValues}>
        <{s.criterionValues} id="v2">
            <criterionID>o2</criterionID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.criterionValues}>
    </criteriaValues>'''
    )
    xml = property(xml)

    xml_empty = '''<criteriaValues/>'''

    def test_init_with_kw(self):
        criteria_values = CriteriaValues(id='an_id', h=6.626e-34)
        self.assertEqual(criteria_values.id, 'an_id')
        self.assertEqual(criteria_values.h, 6.626e-34)

    def test_from_xml(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        self.assertEqual(criteria_values.id, 'vs1')
        self.assertEqual(criteria_values.name, 'vs1-n')
        self.assertEqual(criteria_values.mcda_concept, 'vs1-m')
        self.assertEqual(criteria_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(criteria_values), 2)
        for criterion_value in criteria_values:
            self.assertIsInstance(criterion_value, CriterionValues)
        self.assertEqual(criteria_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.criteria['o2']
        criteria_values = \
            CriteriaValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(criteria_values), 2)
        self.assertEqual({c.id for c in xmcda.criteria},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(criteria_values[1].criterion), id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, CriteriaValues)
        self._test_to_xml(self.xml_empty, CriteriaValues)

    def test_get_item(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        self.assertEqual(criteria_values[0].id, 'v1')
        self.assertEqual(criteria_values['o2'].criterion.id, 'o2')
        self.assertEqual(criteria_values['o2'].criterion.id,
                         criteria_values[1].criterion.id)
        o1 = criteria_values[0].criterion
        self.assertEqual(criteria_values[o1],
                         criteria_values[0])
        with self.assertRaises(IndexError):
            criteria_values[Criterion(id='unknown')]
        with self.assertRaises(IndexError):
            criteria_values['unknown']
        with self.assertRaises(TypeError):
            criteria_values[None]
        with self.assertRaises(TypeError):
            criteria_values[2.3]

    def test_set_item(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        value_1, value_2 = criteria_values[0], criteria_values[1]
        criterion_1, criterion_2 = value_1.criterion, value_2.criterion
        criterion_3 = Criterion(id='o3')
        value_3 = CriterionValues(id='v3')
        value_3.criterion = criterion_3
        value_3.value = Values('moo')

        criteria_values[0] = value_3
        self.assertEqual(criteria_values[0].value[0].v, 'moo')

        criteria_values[criterion_2] = value_3
        self.assertEqual(criteria_values[1], value_3)

        with self.assertRaises(IndexError):
            criteria_values['o1'] = value_2

        value_3.criterion = criterion_1
        criteria_values['o1'] = value_2
        self.assertEqual(criteria_values[0], value_2)

        with self.assertRaises(IndexError):
            criteria_values[Criterion(id='unknown')] = value_1

        with self.assertRaises(TypeError):
            criteria_values[None] = value_1
        with self.assertRaises(TypeError):
            criteria_values[2.3] = value_1

    def test_criteria(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        criteria = criteria_values.criteria()
        self.assertSetEqual({Criterion},
                            {type(criterion)
                             for criterion in criteria})
        self.assertSetEqual({'o1', 'o2'},
                            {criterion.id for criterion in criteria})

    def test_is_numeric(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        self.assertTrue(criteria_values.is_numeric())
        criteria_values['o1'].values = Values("blah")
        self.assertFalse(criteria_values.is_numeric())


class TestCriteriaValues_v3(_TestCriteriaValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.criterionValues = 'criterionValue'

    def tearDown(self):
        set_version(self.current_version)


class TestCriteriaValues_v4(_TestCriteriaValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.criterionValues = 'criterionValues'

    def tearDown(self):
        set_version(self.current_version)
