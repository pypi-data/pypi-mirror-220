from xmcda.alternatives import Alternative
from xmcda.alternatives_sets import AlternativesSet, AlternativesSets
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestAlternativesSet(XMCDATestCase):

    def test_init_kw(self):
        set1 = AlternativesSet(id='set_id', attr=4)
        self.assertEqual(set1.id, 'set_id')
        self.assertEqual(set1.attr, 4)

    def test_add(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        from xmcda.value import Values
        set1.add(o1)
        self.assertIsInstance(set1[o1], Values)
        self.assertEqual(0, len(set1[o1]))

        o2 = Alternative(id='o2')
        set1.add(o2, 2)
        self.assertIsInstance(set1[o2], Values)
        self.assertEqual(1, len(set1[o2]))
        self.assertEqual(set1['o2'].v, 2)

        o3 = Alternative(id='o3')
        set1.add(o3, Values(3))
        self.assertIsInstance(set1[o3], Values)
        self.assertEqual(1, len(set1[o3]))
        self.assertEqual(set1['o3'].v, 3)

    def test_set_item(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        set1[o1] = 1
        self.assertEqual(set1[o1].v, 1)
        self.assertEqual(set1['o1'].v, 1)

    def test_invalid_access(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        with self.assertRaises(KeyError):
            set1[o1]

    def test_assign(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        set1[o1] = 1

        # re-assign
        set1[o1] = 11
        self.assertEqual(len(set1), 1)
        self.assertEqual(set1[o1].v, 11)

        with self.assertRaises(TypeError):
            set1[0] = 111

    def test_element_in_set(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        set1.add(o1)
        self.assertTrue(o1 in set1)

    def test_del_item(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        with self.assertRaises(KeyError):
            del set1[o1]
        set1.add(o1)
        del set1[o1]
        self.assertFalse(o1 in set1)

    def test_reference_element_by_id(self):
        set1 = AlternativesSet(id='set1')
        o1 = Alternative(id='o1')
        set1[o1] = 1
        self.assertEqual(set1['o1'].v, 1)

        set1['o1'] = 11
        self.assertEqual(set1['o1'].v, 11)

        with self.assertRaises(KeyError):
            set1['o2']
        with self.assertRaises(KeyError):
            set1['o2'] = 2

        with self.assertRaises(KeyError):
            del set1['o3']
        del set1['o1']
        self.assertFalse(o1 in set1)

    # xml
    xml_1 = '''
        <alternativesSet id="set1" name="set1n" mcdaConcept="set1m">
            <element>
                <alternativeID>o1</alternativeID>
            </element>
            <element>
                <alternativeID>o2_v</alternativeID>
                <values>
                    <value>
                        <integer>994</integer>
                    </value>
                </values>
            </element>
        </alternativesSet>
    '''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        set1 = AlternativesSet(xml)

        self.assertEqual(set1.id, 'set1')
        self.assertEqual(set1.name, 'set1n')
        self.assertEqual(set1.mcda_concept, 'set1m')

        self.assertEqual(len(set1), 2)
        self.assertIsNone(set1['o1'])
        self.assertEqual(set1['o2_v'][0].v, 994)

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.alternatives['o1']
        set1 = AlternativesSet(xml, xmcda)
        self.assertTrue(o1 in set1.keys())

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, AlternativesSet)
        self.maxDiff = None
        self.assertEqual(source, result)


class TestAlternativesSets(XMCDATestCase):

    def test_init_kw(self):
        sets1 = AlternativesSets(id='sets_id', attr=4)
        self.assertEqual(sets1.id, 'sets_id')
        self.assertEqual(sets1.attr, 4)

    def test_equality(self):
        set1a = AlternativesSet(id='set1')
        set1b = AlternativesSet(id='set1')
        self.assertNotEqual(set1a, set1b)

        set2 = AlternativesSet(id='set2')
        self.assertNotEqual(set1a, set2)

    def test_add_remove(self):
        sets = AlternativesSets()
        set1 = AlternativesSet(id='set1')
        set2 = AlternativesSet(id='set2')
        set3 = AlternativesSet(id='set3')

        sets.append(set1)
        sets.append(set2)
        sets.append(set3)

        # remove an object
        self.assertEqual(len(sets), 3)
        sets.remove(set1)
        self.assertCountEqual(sets, (set2, set3))

        # remove the object given its id
        sets.remove('set3')
        self.assertCountEqual(sets, (set2,))

    xml_1 = '''
        <alternativesSets id="sets" name="setsn" mcdaConcept="setsm">
            <description/>
            <alternativesSet id="set1" name="set1n" mcdaConcept="set1m">
                <element>
                    <alternativeID>o1</alternativeID>
                </element>
            </alternativesSet>
            <alternativesSet id="set2">
                <element>
                    <alternativeID>o2</alternativeID>
                </element>
            </alternativesSet>
        </alternativesSets>
    '''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        sets = AlternativesSets(xml)

        self.assertEqual(sets.id, 'sets')
        self.assertEqual(sets.name, 'setsn')
        self.assertEqual(sets.mcda_concept, 'setsm')
        self.assertEqual(len(sets), 2)
        self.assertEqual(len(sets['set1']), 1)

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.alternatives['o1']
        set1 = xmcda.alternatives_sets['set1']

        xmcda.alternatives_sets.merge_xml(xml, xmcda)
        sets = xmcda.alternatives_sets
        self.assertEqual(sets['set1'], set1, "existing alternativesSet "
                         "is not used when loading the set")
        self.assertEqual(len(xmcda.alternatives_sets), 2)

        # and existing alternative is used, too
        self.assertTrue(o1 in sets['set1'].keys())
        self.assertEqual(len(xmcda.alternatives), 2)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, AlternativesSets)
        self.maxDiff = None
        self.assertEqual(source, result)
