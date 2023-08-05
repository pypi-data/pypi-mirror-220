from xmcda.criteria import Criterion
from xmcda.criteria_hierarchy import CriteriaHierarchy, Node
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCriteriaHierarchy(XMCDATestCase):

    def test_init_kw(self):
        sets1 = CriteriaHierarchy(id='criteria_h_id', attr=11)
        self.assertEqual(sets1.id, 'criteria_h_id')
        self.assertEqual(sets1.attr, 11)

    def test_append_contains_remove(self):
        hierarchy = CriteriaHierarchy()
        self.assertEqual(len(hierarchy), 0)
        o1 = Criterion(id='o1')
        o2 = Criterion(id='o2')

        hierarchy.append(Node(o1))
        hierarchy.append(Node(o2))
        self.assertEqual(len(hierarchy), 2)
        self.assertTrue(Node(o1) in hierarchy)
        self.assertTrue(Node(o2) in hierarchy)

        hierarchy.remove(Node(o2))
        self.assertEqual(len(hierarchy), 1)
        self.assertTrue(Node(o1) in hierarchy)
        self.assertFalse(Node(o2) in hierarchy)

    def test_append_contains_remove_with_criterion(self):
        hierarchy = CriteriaHierarchy()
        self.assertEqual(len(hierarchy), 0)
        o1 = Criterion(id='o1')
        o2 = Criterion(id='o2')

        hierarchy.append(o1)
        hierarchy.append(o2)
        self.assertEqual(len(hierarchy), 2)
        self.assertTrue(Node(o1) in hierarchy,
                        "node was not added when appending o1")
        self.assertTrue(o1 in hierarchy)
        self.assertTrue(o2 in hierarchy)

        hierarchy.remove(o2)
        self.assertEqual(len(hierarchy), 1)
        self.assertTrue(o1 in hierarchy)
        self.assertFalse(o2 in hierarchy)

    def test_node_equality(self):
        o1 = Criterion(id='o1')
        o2 = Criterion(id='o2')

        self.assertEqual(Node(o1), Node(o1))
        self.assertNotEqual(Node(o1), Node(o2))

        n1, n2 = Node(o1), Node(o1)
        n1.append(o1)
        n2.append(o2)
        self.assertNotEqual(n1, Node(o1))
        self.assertNotEqual(n1, n2)

        # same nodes
        n1, n2 = Node(o1), Node(o1)
        [n1.append(x) for x in (o1, o2)]
        [n2.append(x) for x in (o1, o2)]
        self.assertEqual(n1, n2)

        n1, n2 = Node(o1), Node(o1)
        [n1.append(x) for x in (o1, o2)]
        [n2.append(x) for x in (o2, o1)]
        self.assertNotEqual(n1, n2)  # TODO equal or not? order important?

    def _hierarchy(self):
        hierarchy = CriteriaHierarchy()
        root1 = Node(Criterion(id='root1'))
        root2 = Node(Criterion(id='root2'))
        a = Node(Criterion(id='a'))
        b = Node(Criterion(id='b'))
        a1 = Node(Criterion(id='a1'))
        a2 = Node(Criterion(id='a2'))
        hierarchy.append(root1)
        hierarchy.append(root2)
        root1.append(a)
        root1.append(b)
        a.append(a1)
        a.append(a2)
        return hierarchy, root1, root2, a, b, a1, a2

    def test_remove_node(self):
        hierarchy, root1, root2, a, b, a1, a2 = self._hierarchy()
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root1', 'a', 'a1', 'a2', 'b', 'root2'))

        hierarchy.remove_node(root1)
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root2',))

        hierarchy, root1, root2, a, b, a1, a2 = self._hierarchy()
        hierarchy.remove_node(root2)
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root1', 'a', 'a1', 'a2', 'b'))

        hierarchy, root1, root2, a, b, a1, a2 = self._hierarchy()
        hierarchy.remove_node(a)
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root1', 'b', 'root2'))

        hierarchy, root1, root2, a, b, a1, a2 = self._hierarchy()
        hierarchy.remove_node(a2)
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root1', 'a', 'a1', 'b', 'root2'))

        # exceptions
        hierarchy, root1, root2, a, b, a1, a2 = self._hierarchy()
        hierarchy.remove_node(a2)
        with self.assertRaises(ValueError):
            hierarchy.remove_node(a2)  # already removed

        with self.assertRaises(ValueError):
            # should not remove a different criterion with the same id
            hierarchy.remove_node(Criterion(id='a1'))

        # removing arbitrary values
        with self.assertRaises(ValueError): hierarchy.remove_node(None)
        with self.assertRaises(ValueError): hierarchy.remove_node(1)
        with self.assertRaises(ValueError): hierarchy.remove_node(1.0)
        with self.assertRaises(ValueError): hierarchy.remove_node(True)
        with self.assertRaises(ValueError): hierarchy.remove_node([])
        with self.assertRaises(ValueError): hierarchy.remove_node(())
        with self.assertRaises(ValueError): hierarchy.remove_node({})

    def test_remove_node_with_criterion(self):
        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, a2, b, root2))

        hierarchy.remove_node(root1)
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root2,))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node(root2)
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, a2, b))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node(a)
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, b, root2))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node(a2)
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, b, root2))

        # exceptions
        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node(a2)
        with self.assertRaises(ValueError):
            hierarchy.remove_node(a2)  # already removed

        with self.assertRaises(ValueError):
            # should not remove a different criterion with the same id
            hierarchy.remove_node(Criterion(id='a1'))

    def test_remove_node_with_criterion_id(self):
        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, a2, b, root2))

        hierarchy.remove_node('root1')
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root2,))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node('root2')
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, a2, b))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node('a')
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, b, root2))

        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        hierarchy.remove_node('a2')
        self.assertCountEqual([n.criterion for n in hierarchy.nodes()],
                              (root1, a, a1, b, root2))

    def test_get_node_with_criterion(self):
        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]

        self.assertEqual(hierarchy.get_node(root1).criterion, root1)
        self.assertEqual(hierarchy.get_node(a).criterion, a)
        self.assertEqual(hierarchy.get_node(a2).criterion, a2)

        hierarchy.remove_node(a2)
        with self.assertRaises(ValueError):
            hierarchy.get_node(a2)

        # arbitrary values
        with self.assertRaises(ValueError): hierarchy.get_node(None)
        with self.assertRaises(ValueError): hierarchy.get_node(1)
        with self.assertRaises(ValueError): hierarchy.get_node(1.0)

    def test_get_node_with_criterion_id(self):
        hierarchy, *nodes = self._hierarchy()
        root1, root2, a, b, a1, a2 = [x.criterion for x in nodes]
        self.assertEqual(hierarchy.get_node(root1.id).criterion, root1)
        self.assertEqual(hierarchy.get_node(a.id).criterion, a)
        self.assertEqual(hierarchy.get_node(a2.id).criterion, a2)

        hierarchy.remove_node(a2)
        with self.assertRaises(ValueError):
            hierarchy.get_node('a2')

    def test_str(self):
        h = CriteriaHierarchy()
        self.assertEqual(str(h), "CriteriaHierarchy(<empty>)")
        h = CriteriaHierarchy(id='c1', name='n1', mcda_concept='m1')
        self.assertEqual(
            str(h),
            "CriteriaHierarchy(id='c1', name='n1', mcda_concept='m1', <empty>)"
        )

    # XML
    xml_1 = '''
    <criteriaHierarchy id="h1" name="n1" mcdaConcept="m1">
        <nodes>
            <node>
                <criterionID>root1</criterionID>
                <nodes>
                    <node>
                        <criterionID>a</criterionID>
                        <nodes>
                            <node>
                                <criterionID>a1</criterionID>
                            </node>
                            <node>
                                <criterionID>a2</criterionID>
                            </node>
                        </nodes>
                    </node>
                    <node>
                        <criterionID>b</criterionID>
                    </node>
                </nodes>
            </node>
            <node>
                <criterionID>root2</criterionID>
            </node>
        </nodes>
    </criteriaHierarchy>
'''

    xml_empty = '''
        <criteriaHierarchy name="empty h">
            <nodes/>
        </criteriaHierarchy>'''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        hierarchy = CriteriaHierarchy(xml)

        self.assertEqual(hierarchy.id, 'h1')
        self.assertEqual(hierarchy.name, 'n1')
        self.assertEqual(hierarchy.mcda_concept, 'm1')

        self.assertEqual(len(hierarchy), 2)
        root1 = hierarchy[0]
        self.assertEqual(len(root1), 2)
        self.assertEqual(root1[0].criterion.id, 'a')
        self.assertEqual(root1[1].criterion.id, 'b')

        a = root1[0]
        self.assertEqual(len(a), 2)
        self.assertCountEqual([node.criterion.id for node in a],
                              ('a1', 'a2'))

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        root1 = xmcda.criteria['root1']
        a2 = xmcda.criteria['a2']
        hierarchy = CriteriaHierarchy(xml, xmcda)
        self.assertEqual(root1, hierarchy[0].criterion)
        self.assertEqual(a2, hierarchy[0][0][1].criterion)

    def test_str_2(self):
        xml = self.read_xml(self.xml_1)
        hierarchy = CriteriaHierarchy(xml)

        h = "CriteriaHierarchy(id='h1', name='n1', mcda_concept='m1'"
        root1 = "Criterion(id='root1')"
        a = "Criterion(id='a')"
        a1 = "Criterion(id='a1')"
        a2 = "Criterion(id='a2')"
        b = "Criterion(id='b')"
        root2 = "Criterion(id='root2')"

        s = f"{h}, [{root1}: [{a}: [{a1}, {a2}], {b}], {root2}])"
        self.assertEqual(str(hierarchy), s)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)
        result = utf8_to_utf8(self.xml_1, CriteriaHierarchy)
        self.maxDiff = None
        self.assertEqual(source, result)

        source = compact_xml(self.xml_empty)
        result = utf8_to_utf8(self.xml_empty, CriteriaHierarchy)
        self.assertEqual(source, result)

    def test_nodes(self):
        xml = self.read_xml(self.xml_1)
        hierarchy = CriteriaHierarchy(xml)
        self.assertCountEqual([n.criterion.id for n in hierarchy.nodes()],
                              ('root1', 'a', 'a1', 'a2', 'b', 'root2'))
