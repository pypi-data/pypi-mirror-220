from xmcda import set_version, version
from xmcda.alternatives import Alternative
from xmcda.alternatives_values import AlternativesValues, AlternativeValues
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestAlternativeValue:

    xml = (  # noqa E731
        lambda s: f'''
        <{s.alternativeValues} id="v1" name="v1-n" mcdaConcept="v1-m">
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
        </{s.alternativeValues}>'''
    )
    xml = property(xml)

    xml_empty = (  # noqa E731
        lambda s: f'<{s.alternativeValues}/>'
    )
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        alternative_value = AlternativeValues(self.read_xml(self.xml))
        self.assertEqual(alternative_value.id, 'v1')
        self.assertEqual(alternative_value.name, 'v1-n')
        self.assertEqual(alternative_value.mcda_concept, 'v1-m')
        self.assertEqual(alternative_value.description.comment, 'v1-c')
        self.assertIsInstance(alternative_value.values, Values)
        self.assertEqual(len(alternative_value.values), 2)
        self.assertEqual(alternative_value.values[0].v, 1)
        self.assertEqual(alternative_value.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.alternatives['o1']
        alternative_value = AlternativeValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(alternative_value.alternative, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, AlternativeValues)
        self._test_to_xml(self.xml_empty, AlternativeValues)

    def test_is_numeric(self):
        alternative_value = AlternativeValues(self.read_xml(self.xml))
        self.assertTrue(alternative_value.is_numeric())
        alternative_value.values[1] = Value('a string')
        self.assertFalse(alternative_value.is_numeric())


class TestAlternativeValue_v3(_TestAlternativeValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.alternativeValues = 'alternativeValue'

    def tearDown(self):
        set_version(self.current_version)


class TestAlternativeValue_v4(_TestAlternativeValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.alternativeValues = 'alternativeValues'

    def tearDown(self):
        set_version(self.current_version)


class _TestAlternativesValues:

    xml = (  # noqa E731
        lambda s: f'''
    <alternativesValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.alternativeValues} id="v1">
            <alternativeID>o1</alternativeID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.alternativeValues}>
        <{s.alternativeValues} id="v2">
            <alternativeID>o2</alternativeID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.alternativeValues}>
    </alternativesValues>'''
    )
    xml = property(xml)

    xml_empty = '''<alternativesValues/>'''

    def test_init_with_kw(self):
        alternatives_values = AlternativesValues(id='an_id', h=6.626e-34)
        self.assertEqual(alternatives_values.id, 'an_id')
        self.assertEqual(alternatives_values.h, 6.626e-34)

    def test_from_xml(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_values.id, 'vs1')
        self.assertEqual(alternatives_values.name, 'vs1-n')
        self.assertEqual(alternatives_values.mcda_concept, 'vs1-m')
        self.assertEqual(alternatives_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(alternatives_values), 2)
        for alternative_value in alternatives_values:
            self.assertIsInstance(alternative_value, AlternativeValues)
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
        self._test_to_xml(self.xml_empty, AlternativesValues)

    def test_get_item(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_values[0].id, 'v1')
        self.assertEqual(alternatives_values['o2'].alternative.id, 'o2')
        self.assertEqual(alternatives_values['o2'].alternative.id,
                         alternatives_values[1].alternative.id)
        o1 = alternatives_values[0].alternative
        self.assertEqual(alternatives_values[o1],
                         alternatives_values[0])
        with self.assertRaises(IndexError):
            alternatives_values[Alternative(id='unknown')]
        with self.assertRaises(IndexError):
            alternatives_values['unknown']
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

        with self.assertRaises(IndexError):
            alternatives_values[Alternative(id='unknown')] = value_1

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

    def test_is_numeric(self):
        alternatives_values = AlternativesValues(self.read_xml(self.xml))
        self.assertTrue(alternatives_values.is_numeric())
        alternatives_values['o1'].values = Values("blah")
        self.assertFalse(alternatives_values.is_numeric())


class TestAlternativesValues_v3(_TestAlternativesValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.alternativeValues = 'alternativeValue'

    def tearDown(self):
        set_version(self.current_version)


class TestAlternativesValues_v4(_TestAlternativesValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.alternativeValues = 'alternativeValues'

    def tearDown(self):
        set_version(self.current_version)
