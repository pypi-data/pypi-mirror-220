from xmcda.criteria import Criterion
from xmcda.criteria_sets import CriteriaSet, CriteriaSets
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCriteriaSet(XMCDATestCase):

    def test_init_kw(self):
        set1 = CriteriaSet(id='set_id', attr=4)
        self.assertEqual(set1.id, 'set_id')
        self.assertEqual(set1.attr, 4)

    def test_add(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        from xmcda.value import Values
        set1.add(o1)
        self.assertIsInstance(set1[o1], Values)
        self.assertEqual(0, len(set1[o1]))

        o2 = Criterion(id='o2')
        set1.add(o2, 2)
        self.assertIsInstance(set1[o2], Values)
        self.assertEqual(1, len(set1[o2]))
        self.assertEqual(set1['o2'].v, 2)

        o3 = Criterion(id='o3')
        set1.add(o3, Values(3))
        self.assertIsInstance(set1[o3], Values)
        self.assertEqual(1, len(set1[o3]))
        self.assertEqual(set1['o3'].v, 3)

    def test_set_item(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        set1[o1] = 1
        self.assertEqual(set1[o1].v, 1)
        self.assertEqual(set1['o1'].v, 1)

    def test_invalid_access(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        with self.assertRaises(KeyError):
            set1[o1]

    def test_assign(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        set1[o1] = 1

        # re-assign
        set1[o1] = 11
        self.assertEqual(len(set1), 1)
        self.assertEqual(set1[o1].v, 11)

        with self.assertRaises(TypeError):
            set1[0] = 111

    def test_element_in_set(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        set1.add(o1)
        self.assertTrue(o1 in set1)

    def test_del_item(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
        with self.assertRaises(KeyError):
            del set1[o1]
        set1.add(o1)
        del set1[o1]
        self.assertFalse(o1 in set1)

    def test_reference_element_by_id(self):
        set1 = CriteriaSet(id='set1')
        o1 = Criterion(id='o1')
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
        <criteriaSet id="set1" name="set1n" mcdaConcept="set1m">
            <element>
                <criterionID>o1</criterionID>
            </element>
            <element>
                <criterionID>o2_v</criterionID>
                <values>
                    <value>
                        <integer>994</integer>
                    </value>
                </values>
            </element>
        </criteriaSet>
    '''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        set1 = CriteriaSet(xml)

        self.assertEqual(set1.id, 'set1')
        self.assertEqual(set1.name, 'set1n')
        self.assertEqual(set1.mcda_concept, 'set1m')

        self.assertEqual(len(set1), 2)
        self.assertIsNone(set1['o1'], 0)
        self.assertEqual(set1['o2_v'][0].v, 994)

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        set1 = CriteriaSet(xml, xmcda)
        self.assertTrue(o1 in set1.keys())

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, CriteriaSet)
        self.maxDiff = None
        self.assertEqual(source, result)


class TestCriteriaSets(XMCDATestCase):

    def test_init_kw(self):
        sets1 = CriteriaSets(id='sets_id', attr=4)
        self.assertEqual(sets1.id, 'sets_id')
        self.assertEqual(sets1.attr, 4)

    def test_equality(self):
        set1a = CriteriaSet(id='set1')
        set1b = CriteriaSet(id='set1')
        self.assertNotEqual(set1a, set1b)

        set2 = CriteriaSet(id='set2')
        self.assertNotEqual(set1a, set2)

    def test_add_remove(self):
        sets = CriteriaSets()
        set1 = CriteriaSet(id='set1')
        set2 = CriteriaSet(id='set2')
        set3 = CriteriaSet(id='set3')

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
        <criteriaSets id="sets" name="setsn" mcdaConcept="setsm">
            <description/>
            <criteriaSet id="set1" name="set1n" mcdaConcept="set1m">
                <element>
                    <criterionID>o1</criterionID>
                </element>
            </criteriaSet>
            <criteriaSet id="set2">
                <element>
                    <criterionID>o2</criterionID>
                </element>
            </criteriaSet>
        </criteriaSets>
    '''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        sets = CriteriaSets(xml)

        self.assertEqual(sets.id, 'sets')
        self.assertEqual(sets.name, 'setsn')
        self.assertEqual(sets.mcda_concept, 'setsm')
        self.assertEqual(len(sets), 2)
        self.assertEqual(len(sets['set1']), 1)

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        set1 = xmcda.criteria_sets['set1']

        xmcda.criteria_sets.merge_xml(xml, xmcda)
        sets = xmcda.criteria_sets
        self.assertEqual(sets['set1'], set1, "existing criteriaSet "
                         "is not used when loading the set")
        self.assertEqual(len(xmcda.criteria_sets), 2)

        # and existing criterion is used, too
        self.assertTrue(o1 in sets['set1'].keys())
        self.assertEqual(len(xmcda.criteria), 2)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, CriteriaSets)
        self.maxDiff = None
        self.assertEqual(source, result)

        # Make sure empty Values() ,assigned to elements are
        # not serialized: empty <values/> are invalid wrt XMCDA v4
        from .utils import element_to_utf8, make_xmcda_v4
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        sets1 = CriteriaSets(xml, xmcda)
        sets1[0][o1] = Values()
        xmcda.criteria_sets = sets1
        result = element_to_utf8(xmcda, 'criteriaSets')
        self.assertEqual(compact_xml(make_xmcda_v4(self.xml_1)),
                         result)
