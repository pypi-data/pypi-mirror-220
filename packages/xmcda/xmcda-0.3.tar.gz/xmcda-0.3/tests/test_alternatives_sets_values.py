from xmcda import set_version, version
from xmcda.alternatives_sets import AlternativesSet
from xmcda.alternatives_sets_values import (
    AlternativesSetsValues,
    AlternativesSetValues,
)
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestAlternativesSetValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml = (  # noqa E731
        lambda s: f'''
        <{s.alternativesSetValues} id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <alternativesSetID>o1</alternativesSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </{s.alternativesSetValues}>'''
    )
    xml = property(xml)

    xml_empty = lambda s: f'<{s.alternativesSetValues}/>'  # noqa E731
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        alternatives_set_values = AlternativesSetValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_set_values.id, 'v1')
        self.assertEqual(alternatives_set_values.name, 'v1-n')
        self.assertEqual(alternatives_set_values.mcda_concept, 'v1-m')
        self.assertEqual(alternatives_set_values.description.comment, 'v1-c')
        self.assertIsInstance(alternatives_set_values.values, Values)
        self.assertEqual(len(alternatives_set_values.values), 2)
        self.assertEqual(alternatives_set_values.values[0].v, 1)
        self.assertEqual(alternatives_set_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.alternatives_sets['o1']
        alternatives_set_values = (
          AlternativesSetValues(self.read_xml(self.xml), xmcda))
        self.assertEqual(alternatives_set_values.alternatives_set, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, AlternativesSetValues)
        # accept to read/write an empty tag
        self._test_to_xml(self.xml_empty, AlternativesSetValues)


class TestAlternativesSetValue_v3(_TestAlternativesSetValues, XMCDATestCase):
    version = XMCDA_3_1_1
    alternativesSetValues = 'alternativesSetValue'


class TestAlternativesSetValue_v4(_TestAlternativesSetValues, XMCDATestCase):
    version = XMCDA_4_0_0
    alternativesSetValues = 'alternativesSetValues'


class _TestAlternativesSetsValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)


    xml = (  # noqa E731
        lambda s: f'''
    <alternativesSetsValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.alternativesSetValues} id="v1">
            <alternativesSetID>o1</alternativesSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.alternativesSetValues}>
        <{s.alternativesSetValues} id="v2">
            <alternativesSetID>o2</alternativesSetID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.alternativesSetValues}>
    </alternativesSetsValues>'''
    )
    xml = property(xml)

    xml_empty = '<alternativesSetsValues/>'

    def test_init_with_args(self):
        alternatives_sets_values = AlternativesSetsValues(id='csv1', attr=12)
        self.assertEqual(alternatives_sets_values.id, 'csv1')
        self.assertEqual(alternatives_sets_values.attr, 12)

    def test_from_xml(self):
        alternatives_sets_values = \
            AlternativesSetsValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_sets_values.id, 'vs1')
        self.assertEqual(alternatives_sets_values.name, 'vs1-n')
        self.assertEqual(alternatives_sets_values.mcda_concept, 'vs1-m')
        self.assertEqual(alternatives_sets_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(alternatives_sets_values), 2)
        for alternatives_set_values in alternatives_sets_values:
            self.assertIsInstance(alternatives_set_values,
                                  AlternativesSetValues)
        self.assertEqual(alternatives_sets_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.alternatives_sets['o2']
        alternatives_sets_values = \
            AlternativesSetsValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(alternatives_sets_values), 2)
        self.assertEqual({c.id for c in xmcda.alternatives_sets},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(alternatives_sets_values[1].alternatives_set),
                         id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, AlternativesSetsValues)
        self._test_to_xml(self.xml_empty, AlternativesSetsValues)

    def test_get_item(self):
        alternatives_sets_values = \
            AlternativesSetsValues(self.read_xml(self.xml))
        self.assertEqual(alternatives_sets_values[0].id, 'v1')
        self.assertEqual(alternatives_sets_values['o2'].alternatives_set.id,
                         'o2')
        self.assertEqual(alternatives_sets_values['o2'].alternatives_set.id,
                         alternatives_sets_values[1].alternatives_set.id)
        o1 = alternatives_sets_values[0].alternatives_set
        self.assertEqual(alternatives_sets_values[o1],
                         alternatives_sets_values[0])

        with self.assertRaises(IndexError):
            alternatives_sets_values[AlternativesSet(id='unknown')]
        with self.assertRaises(IndexError):
            alternatives_sets_values['unknown']

        with self.assertRaises(TypeError):
            alternatives_sets_values[None]
        with self.assertRaises(TypeError):
            alternatives_sets_values[2.3]

    def test_set_item(self):
        alternatives_sets_values = \
            AlternativesSetsValues(self.read_xml(self.xml))
        value_1 = alternatives_sets_values[0]
        value_2 = alternatives_sets_values[1]
        alternativesSet_1 = value_1.alternatives_set
        alternativesSet_2 = value_2.alternatives_set
        alternativesSet_3 = AlternativesSet(id='o3')
        value_3 = AlternativesSetValues(id='v3')
        value_3.alternatives_set = alternativesSet_3
        value_3.value = Values('moo')

        alternatives_sets_values[0] = value_3
        self.assertEqual(alternatives_sets_values[0].value[0].v, 'moo')

        alternatives_sets_values[alternativesSet_2] = value_3
        self.assertEqual(alternatives_sets_values[1], value_3)

        with self.assertRaises(IndexError):
            alternatives_sets_values[AlternativesSet(id='unknown')] = value_2

        with self.assertRaises(IndexError):
            alternatives_sets_values['o1'] = value_2

        value_3.alternatives_set = alternativesSet_1
        alternatives_sets_values['o1'] = value_2
        self.assertEqual(alternatives_sets_values[0], value_2)

        with self.assertRaises(TypeError):
            alternatives_sets_values[None] = value_1
        with self.assertRaises(TypeError):
            alternatives_sets_values[2.3] = value_1


class TestAlternativesSetsValue_v3(_TestAlternativesSetsValues, XMCDATestCase):
    version = XMCDA_3_1_1
    alternativesSetValues = 'alternativesSetValue'


class TestAlternativesSetsValue_v4(_TestAlternativesSetsValues, XMCDATestCase):
    version = XMCDA_4_0_0
    alternativesSetValues = 'alternativesSetValues'
