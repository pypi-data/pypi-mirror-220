from xmcda.alternatives import Alternative
from xmcda.criteria import Criterion
from xmcda.performance_table import PerformanceTable
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class TestPerformanceTable(XMCDATestCase):

    def setUp(self):
        self.p = PerformanceTable()
        self.a1 = Alternative(id='a1')
        self.a2 = Alternative(id='a2')
        self.c1 = Criterion(id='c1')
        self.c2 = Criterion(id='c2')

    def test_getter_setter(self):
        a1, a2, c1, c2, p = self.a1, self.a2, self.c1, self.c2, self.p

        p.set(a1, c1, Values(Value(42)))
        # perf.table.get() returns a Values object
        self.assertIsInstance(p.get(a1, c1), Values)
        self.assertEqual(len(p.get(a1, c1)), 1)
        self.assertEqual(p.get(a1, c1)[0].v, 42)

        self.assertRaises(KeyError, p.get, a1, c2)
        self.assertRaises(KeyError, p.get, a2, c1)
        with self.assertRaises(KeyError):
            p[a1][c2]
        with self.assertRaises(KeyError):
            p[a2][c1]
        with self.assertRaises(KeyError):
            p[0][c1]

        p.set(a1, c1, 'v11')
        # perf.table.get() returns a Values object
        self.assertEqual(p.get(a1, c1)[0].v, 'v11')

    def test_getter_setter_2(self):
        a1, a2, c1, p = self.a1, self.a2, self.c1, self.p

        self.assertEqual(p[a1], {})  # empty row

        p[a1][c1] = 42
        self.assertEqual(p[a1][c1], 42)

        self.assertEqual(p['a1'][c1], 42)
        self.assertEqual(p[a1]['c1'], 42)

        # set an existing location
        p['a1'][c1] = 43
        self.assertEqual(p[a1][c1], 43)
        p[a1]['c1'] = 44
        self.assertEqual(p[a1][c1], 44)

        with self.assertRaises(KeyError):
            p[a1]['c2'] = 45

        # set an empty emplacement
        with self.assertRaises(KeyError):
            p['a2'][c1] = 5

        p[a2][c1] = 5
        self.assertEqual(p[a2][c1], 5)
        with self.assertRaises(KeyError):
            p[a1]['c2'] = 45

        # invalid index
        with self.assertRaises(KeyError):
            p[0][c1] = 0
        with self.assertRaises(KeyError):
            p[a1][0] = 0

    def test_getter_absent_value(self):
        'Accessing an absent value raises KeyError'
        a1, a2, c1, c2, p = self.a1, self.a2, self.c1, self.c2, self.p

        p[a2][c2] = 1
        with self.assertRaises(KeyError):
            p.get(a1, c1)
        with self.assertRaises(KeyError):
            p[a1][c1]
        with self.assertRaises(KeyError):
            p[a2][c1]  # existing row, absent value

    def test_smart_dict_getter_setter(self):
        a1, c1, p = self.a1, self.c1, self.p
        # integer supplied...
        p[a1][c1] = 42
        # ...a Values object has been created...
        self.assertIsInstance(p.get(a1, c1), Values)
        self.assertEqual(p.get(a1, c1)[0].v, 42)
        # ... and using [] getters on the perf.table returns the raw integer
        self.assertEqual(p[a1][c1], 42)

        # but with two or more values, we get Values():
        v11 = Values()
        v11.append(Value(42))
        p[a1][c1] = v11
        self.assertIsInstance(p.get(a1, c1), Values)
        self.assertEqual(p[a1][c1], 42)  # same as above: one Value in Values

        v11.append(Value(12))  # add a second value
        self.assertEqual(p[a1][c1], v11)

    def test_smart_dict_getter_setter_2(self):
        a1, c1 = self.a1, self.c1
        p = PerformanceTable()

        # set w/ an Alternative and a Criterion
        p[a1][c1] = 11

        # Access values w/ Alternative and Criterion
        v = p.get(a1, c1)
        self.assertIsInstance(v, Values)
        self.assertEqual(len(v), 1)
        self.assertEqual(v[0].v, 11)

        # or access w/ ids:
        v = p['a1']['c1']
        self.assertIsInstance(v, int)
        self.assertEqual(v, 11)

    def test_smart_dict_getter_setter_3(self):
        # test that, when alternative and/or criterion are already
        # referenced in a performance table, we can set new or
        # existing cells in the performance table using ids

        a1, a2, c1, c2 = self.a1, self.a2, self.c1, self.c2
        p = PerformanceTable()
        p[a1][c1] = 11
        p[a2][c2] = 22

        for _a1 in (a1, 'a1'):
            for _c2 in (c2, 'c2'):
                with self.assertRaises(KeyError):
                    p[_a1][_c2]

        with self.assertRaises(KeyError):
            p[a1]['c3'] = 7

        # performance table already knows about A&, a2, c1 and c2:
        # let's use their (string) ids
        # ... to access a cell
        p[a1][c2] = 12
        for _a1 in (a1, 'a1'):
            for _c2 in (c2, 'c2'):
                self.assertEqual(p[_a1][_c2], 12)

        # ... and to assign value to a cell (1/3)
        p['a1'][c2] = 121
        for _a1 in (a1, 'a1'):
            for _c2 in (c2, 'c2'):
                self.assertEqual(p[_a1][_c2], 121, f'{_a1}/{_c2}')

        # ... and to assign value to a cell (2/3)
        p[a1]['c2'] = 122
        for _a1 in (a1, 'a1'):
            for _c2 in (c2, 'c2'):
                self.assertEqual(p[_a1][_c2], 122, f'{_a1}/{_c2}')

        # ... and to assign value to a cell (3/3)
        p['a1']['c2'] = 'all strings'
        for _a1 in (a1, 'a1'):
            for _c2 in (c2, 'c2'):
                self.assertEqual(p[_a1][_c2], 'all strings', f'{_a1}/{_c2}')

    xml_empty_cell = '''
<performanceTable>
    <alternativePerformances>
        <alternativeID>a1</alternativeID>
        <performance>
            <criterionID>c1</criterionID>
            <values/>
        </performance>
    </alternativePerformances>
</performanceTable>
'''

    def test_smart_dict_setter_assigns_None(self):
        "Using None assigns an empty values to the cell"
        p = PerformanceTable()
        a1, c1 = self.a1, self.c1
        p[a1][c1] = 12
        p[a1][c1] = None
        from .utils import compact_xml, element_to_utf8
        self.maxDiff = None
        self.assertEqual(compact_xml(self.xml_empty_cell),
                         element_to_utf8(p, PerformanceTable))

    def test_deletion_of_a_cell(self):
        a1, a2, c1, p = self.a1, self.a2, self.c1, self.p

        with self.assertRaises(KeyError):
            del self.p[a1][c1]

        p[a1][c1] = 12
        del p[a1][c1]
        with self.assertRaises(KeyError):
            p[a1][c1]

        p[a1][c1] = 12
        del self.p['a1']['c1']
        with self.assertRaises(KeyError):
            p[a1][c1]

        with self.assertRaises(KeyError):
            del p[a2][c1]
        with self.assertRaises(KeyError):
            del p['a2'][c1]
        with self.assertRaises(KeyError):
            del p[a2]['c1']

    def test_search_by_id(self):
        '''
        Referencing an alternative (resp. criterion) by its 'id' is ok, only
        when it is already known to the performance table.
        '''
        a1, c1, p = self.a1, self.c1, self.p

        with self.assertRaises(KeyError):
            p['a1']
        p[a1][c1] = 42
        with self.assertRaises(KeyError):
            p['a1']['c2']
        self.assertEqual(p['a1']['c1'], 42)
        self.assertEqual(p[a1][c1], 42)

    xml_1 = '''
<performanceTable id="p01" name="p01 name" mcdaConcept="p01 mcdaConcept">
    <description/>
    <alternativePerformances>
        <alternativeID>x1</alternativeID>
        <performance>
            <criterionID>g2</criterionID>
            <values>
                <value>
                    <real>0.375</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g3</criterionID>
            <values>
                <value>
                    <real>1.0</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g1</criterionID>
            <values>
                <value>
                    <real>0.4375</real>
                </value>
            </values>
        </performance>
    </alternativePerformances>
    <alternativePerformances>
        <alternativeID>x2</alternativeID>
        <performance>
            <criterionID>g2</criterionID>
            <values>
                <value>
                    <real>0.125</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g3</criterionID>
            <values>
                <value>
                    <real>0.375</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g1</criterionID>
            <values>
                <value>
                    <real>0.8125</real>
                </value>
            </values>
        </performance>
         <performance>
            <criterionID>g4</criterionID>
            <values>
                <value>
                    <integer>4</integer>
                </value>
            </values>
        </performance>
   </alternativePerformances>
    <alternativePerformances>
        <alternativeID>x3</alternativeID>
        <performance>
            <criterionID>g2</criterionID>
            <values>
                <value>
                    <real>1.0</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g3</criterionID>
            <values>
                <value>
                    <real>0.5</real>
                </value>
            </values>
        </performance>
        <performance>
            <criterionID>g1</criterionID>
            <values>
                <value>
                    <real>0.125</real>
                </value>
            </values>
        </performance>
    </alternativePerformances>
</performanceTable>
'''

    xmcda_1 = make_xmcda_v4(xml_1)

    xmcda_alternatives_1 = make_xmcda_v4('''
    <alternatives>
        <alternative id='x1' name='x1-name'>
            <type>fictive</type>
            <active>false</active>
        </alternative>
    </alternatives>
''')

    def test_load_xml(self):
        xml = self.read_xml(TestPerformanceTable.xml_1)
        p = PerformanceTable.build(xml)

        self.assertIsNotNone(p)

        alts = p.alternatives()
        crits = p.criteria()
        self.assertEqual(len(alts), 3)
        self.assertEqual(len(crits), 4)
        self.assertEqual({a.id for a in alts},
                         {'x1', 'x2', 'x3'})
        self.assertEqual({c.id for c in crits},
                         {'g1', 'g2', 'g3', 'g4'})

    def test_load_xml_with_xmcda(self):
        xml = self.read_xml(TestPerformanceTable.xml_1)

        xmcda = XMCDA()
        alt_x1 = xmcda.alternatives['x1']  # creates it
        p = PerformanceTable(xml, xmcda)

        self.assertIsNotNone(p)

        self.assertEqual(len(xmcda.alternatives), 3)
        self.assertEqual(len(xmcda.criteria), 4)

        self.assertEqual({a.id for a in xmcda.alternatives},
                         {'x1', 'x2', 'x3'})
        self.assertEqual({c.id for c in xmcda.criteria},
                         {'g1', 'g2', 'g3', 'g4'})

        # x1 created before loading the perf. table, it should have been used
        self.assertEqual([a for a in xmcda.alternatives if a.id == 'x1'][0],
                         alt_x1)

    xml_empty = '''<performanceTable/>'''

    def test_add_then_del_a_cell(self):
        "Make sure a row disappears in the XML when its last cell is deleted"
        a1, c1 = self.a1, self.c1
        p = PerformanceTable()
        p[a1][c1] = 12
        del p[a1][c1]
        from .utils import compact_xml, element_to_utf8
        self.maxDiff = None
        self.assertEqual(compact_xml(self.xml_empty),
                         element_to_utf8(p, PerformanceTable))

    def test_to_xml(self):
        self._test_to_xml(TestPerformanceTable.xml_1, PerformanceTable)
        self._test_to_xml(TestPerformanceTable.xml_empty, PerformanceTable)
        self._test_to_xml(
            TestPerformanceTable.xml_empty_cell, PerformanceTable
        )

    def test_has_missing_values(self):
        a1, a2, c1, c2, p = self.a1, self.a2, self.c1, self.c2, self.p

        p.set(a1, c1, 'v11')
        self.assertFalse(p.has_missing_values())

        p.set(a1, c2, 'v12')
        p.set(a2, c1, 'v21')

        self.assertTrue(p.has_missing_values())

        p.set(a2, c2, 'v22')
        self.assertFalse(p.has_missing_values())

    def test_is_numeric(self):
        a1, c1, c2, p = self.a1, self.c1, self.c2, self.p

        from xmcda.value import Values

        p.set(a1, c1, Values(value=11))
        self.assertTrue(p.is_numeric())

        p.set(a1, c2, Values(value='v12'))
        self.assertFalse(p.is_numeric())

        p.set(a1, c2, Values(value='12'))
        self.assertTrue(p.is_numeric())  # default: strict=False
        self.assertTrue(p.is_numeric(strict=False))
        self.assertFalse(p.is_numeric(strict=True))

    def test_as_float(self):
        a1, c1, c2, p = self.a1, self.c1, self.c2, self.p
        p.set(a1, c1, Values(value=11))
        p.set(a1, c2, Values(value='v12'))
        self.assertRaises(ValueError, p.as_float)
        p.set(a1, c2, Values(value='12'))
        p.as_float()
        self.assertEqual(p[a1][c1], 11)
        self.assertEqual(p[a1][c1], 11)

    def test_load_alternatives(self):
        # load the performance table, and the alternatives afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.alternatives), 3)
        x1 = xmcda.alternatives['x1']
        self.assertEqual(x1.name, None)
        self.assertTrue(x1.is_real)
        self.assertTrue(x1.active)

        xmcda.fromstring(self.xmcda_alternatives_1)
        self.assertEqual(len(xmcda.alternatives), 3)
        self.assertEqual(x1, xmcda.alternatives['x1'])
        self.assertEqual(x1.name, 'x1-name')
        self.assertFalse(x1.is_real)
        self.assertFalse(x1.active)

        # load than the alternatives, and the performance table afterwards
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_alternatives_1)
        self.assertEqual(len(xmcda.alternatives), 1)
        x1 = xmcda.alternatives['x1']
        self.assertEqual(x1.name, 'x1-name')
        self.assertFalse(x1.is_real)
        self.assertFalse(x1.active)

        xmcda.fromstring(self.xmcda_1)
        self.assertEqual(len(xmcda.alternatives), 3)
        self.assertEqual(x1, xmcda.alternatives['x1'])
        self.assertEqual(x1.name, 'x1-name')
        self.assertFalse(x1.is_real)
        self.assertFalse(x1.active)

    def test_iteration_order_on_alternatives_is_stable(self):
        xml = self.read_xml(TestPerformanceTable.xml_1)
        p = PerformanceTable.build(xml)

        alternatives = p.alternatives()
        # iterating 50x has proved to be enough to reveal a problem for now
        # see also test_iteration_order_on_criteria_is_stable(), below
        for _ in range(50):
            xml = self.read_xml(TestPerformanceTable.xml_1)
            p = PerformanceTable.build(xml)
            self.assertSequenceEqual([a.id for a in alternatives],
                                     [a.id for a in p.alternatives()])

    def test_iteration_order_on_criteria_is_stable(self):
        xml = self.read_xml(TestPerformanceTable.xml_1)
        p = PerformanceTable.build(xml)

        criteria = p.criteria()
        # iterating 50x has proved to be enough to reveal a problem for now
        # see also test_iteration_order_on_alternatives_is_stable(), above
        for _ in range(50):
            xml = self.read_xml(TestPerformanceTable.xml_1)
            p = PerformanceTable.build(xml)
            self.assertSequenceEqual([c.id for c in criteria],
                                     [c.id for c in p.criteria()])

#    def test_set_handles_values(self):
#        a1, a2, c1, c2, p = self.a1, self.a2, self.c1, self.c2, self.p
#
#        p[a1][c1]=
