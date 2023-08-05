from xmcda.criteria import Criterion
from xmcda.criteria_values import CriteriaValues, CriterionValues
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCriterionValues(XMCDATestCase):

    xml = '''
        <criterionValues id="v1" name="v1-n" mcdaConcept="v1-m">
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
        </criterionValues>
    '''

    def test_from_xml(self):
        criterion_values = CriterionValues(self.read_xml(self.xml))
        self.assertEqual(criterion_values.id, 'v1')
        self.assertEqual(criterion_values.name, 'v1-n')
        self.assertEqual(criterion_values.mcda_concept, 'v1-m')
        self.assertEqual(criterion_values.description.comment, 'v1-c')
        self.assertIsInstance(criterion_values.values, Values)
        self.assertEqual(len(criterion_values.values), 2)
        self.assertEqual(criterion_values.values[0].v, 1)
        self.assertEqual(criterion_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        criterion_values = CriterionValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(criterion_values.criterion, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CriterionValues)

    def test_is_numeric(self):
        criterion_values = CriterionValues(self.read_xml(self.xml))
        self.assertTrue(criterion_values.is_numeric())
        criterion_values.values[1] = Value('a string')
        self.assertFalse(criterion_values.is_numeric())


class TestCriteriaValues(XMCDATestCase):

    xml = '''
    <criteriaValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <criterionValues id="v1">
            <criterionID>o1</criterionID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </criterionValues>
        <criterionValues id="v2">
            <criterionID>o2</criterionID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </criterionValues>
    </criteriaValues>'''

    def test_from_xml(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        self.assertEqual(criteria_values.id, 'vs1')
        self.assertEqual(criteria_values.name, 'vs1-n')
        self.assertEqual(criteria_values.mcda_concept, 'vs1-m')
        self.assertEqual(criteria_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(criteria_values), 2)
        for criterion_values in criteria_values:
            self.assertIsInstance(criterion_values, CriterionValues)
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

    def test_get_item(self):
        criteria_values = CriteriaValues(self.read_xml(self.xml))
        self.assertEqual(criteria_values[0].id, 'v1')
        self.assertEqual(criteria_values['o2'].criterion.id, 'o2')
        self.assertEqual(criteria_values['o2'].criterion.id,
                         criteria_values[1].criterion.id)
        o1 = criteria_values[0].criterion
        self.assertEqual(criteria_values[o1],
                         criteria_values[0])
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
