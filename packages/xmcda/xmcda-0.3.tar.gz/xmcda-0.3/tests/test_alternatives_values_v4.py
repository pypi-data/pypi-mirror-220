from xmcda.alternatives import Alternative
from xmcda.alternatives_values import AlternativesValues, AlternativeValues
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestAlternativeValues(XMCDATestCase):

    xml = '''
        <alternativeValues id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <alternativeID>o1</alternativeID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </alternativeValues>
    '''

    def test_from_xml(self):
        alternative_values = AlternativeValues(self.read_xml(self.xml))
        self.assertEqual(alternative_values.id, 'v1')
        self.assertEqual(alternative_values.name, 'v1-n')
        self.assertEqual(alternative_values.mcda_concept, 'v1-m')
        self.assertEqual(alternative_values.description.comment, 'v1-c')
        self.assertIsInstance(alternative_values.values, Values)
        self.assertEqual(len(alternative_values.values), 2)
        self.assertEqual(alternative_values.values[0].v, 1)
        self.assertEqual(alternative_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.alternatives['o1']
        alternative_values = AlternativeValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(alternative_values.alternative, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, AlternativeValues)

    def test_is_numeric(self):
        alternative_values = AlternativeValues(self.read_xml(self.xml))
        self.assertTrue(alternative_values.is_numeric())
        alternative_values.values[1] = Value('a string')
        self.assertFalse(alternative_values.is_numeric())


class TestAlternativesValues(XMCDATestCase):

    xml = '''
    <alternativesValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <alternativeValues id="v1">
            <alternativeID>o1</alternativeID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </alternativeValues>
        <alternativeValues id="v2">
            <alternativeID>o2</alternativeID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </alternativeValues>
    </alternativesValues>'''

    def test_from_xml(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_values.id, 'vs1')
        self.assertEqual(alternatives_values.name, 'vs1-n')
        self.assertEqual(alternatives_values.mcda_concept, 'vs1-m')
        self.assertEqual(alternatives_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(alternatives_values), 2)
        for alternative_values in alternatives_values:
            self.assertIsInstance(alternative_values, AlternativeValues)
        self.assertEqual(alternatives_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.alternatives['o2']
        alternatives_values = \
            AlternativesValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(alternatives_values), 2)
        self.assertEqual({c.id for c in xmcda.alternatives},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(alternatives_values[1].alternative), id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, AlternativesValues)

    def test_get_item(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_values[0].id, 'v1')
        self.assertEqual(alternatives_values['o2'].alternative.id, 'o2')
        self.assertEqual(alternatives_values['o2'].alternative.id,
                         alternatives_values[1].alternative.id)
        o1 = alternatives_values[0].alternative
        self.assertEqual(alternatives_values[o1],
                         alternatives_values[0])
        with self.assertRaises(TypeError):
            alternatives_values[None]
        with self.assertRaises(TypeError):
            alternatives_values[2.3]

    def test_set_item(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        value_1, value_2 = alternatives_values[0], alternatives_values[1]
        alternative_1, alternative_2 = value_1.alternative, value_2.alternative
        alternative_3 = Alternative(id='o3')
        value_3 = AlternativeValues(id='v3')
        value_3.alternative = alternative_3
        value_3.value = Values('moo')

        alternatives_values[0] = value_3
        self.assertEqual(alternatives_values[0].value[0].v, 'moo')

        alternatives_values[alternative_2] = value_3
        self.assertEqual(alternatives_values[1], value_3)

        with self.assertRaises(IndexError):
            alternatives_values['o1'] = value_2

        value_3.alternative = alternative_1
        alternatives_values['o1'] = value_2
        self.assertEqual(alternatives_values[0], value_2)

        with self.assertRaises(TypeError):
            alternatives_values[None] = value_1
        with self.assertRaises(TypeError):
            alternatives_values[2.3] = value_1

    def test_alternatives(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        alternatives = alternatives_values.alternatives()
        self.assertSetEqual({Alternative},
                            {type(alternative)
                             for alternative in alternatives})
        self.assertSetEqual({'o1', 'o2'},
                            {alternative.id for alternative in alternatives})
