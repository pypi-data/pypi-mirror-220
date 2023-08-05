from xmcda.criteria_sets_hierarchy import CriteriaSetsHierarchy
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCriteriaSetsHierarchy(XMCDATestCase):

    xml_1 = '''
    <criteriaSetsHierarchy id="h1" name="n1" mcdaConcept="m1">
        <nodes>
            <node>
                <criteriaSetID>root1</criteriaSetID>
                <nodes>
                    <node>
                        <criteriaSetID>a</criteriaSetID>
                        <nodes>
                            <node>
                                <criteriaSetID>a1</criteriaSetID>
                            </node>
                            <node>
                                <criteriaSetID>a2</criteriaSetID>
                            </node>
                        </nodes>
                    </node>
                    <node>
                        <criteriaSetID>b</criteriaSetID>
                    </node>
                </nodes>
            </node>
            <node>
                <criteriaSetID>root2</criteriaSetID>
            </node>
        </nodes>
    </criteriaSetsHierarchy>
'''

    xml_empty = '''
        <criteriaSetsHierarchy name="empty h">
            <nodes/>
        </criteriaSetsHierarchy>'''

    def test_init_kw(self):
        sets1 = CriteriaSetsHierarchy(id='criteria_sets_h_id', attr=12)
        self.assertEqual(sets1.id, 'criteria_sets_h_id')
        self.assertEqual(sets1.attr, 12)

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        hierarchy = CriteriaSetsHierarchy(xml)

        self.assertEqual(hierarchy.id, 'h1')
        self.assertEqual(hierarchy.name, 'n1')
        self.assertEqual(hierarchy.mcda_concept, 'm1')

        self.assertEqual(len(hierarchy), 2)
        root1 = hierarchy[0]
        self.assertEqual(len(root1), 2)
        self.assertEqual(root1[0].criteria_set.id, 'a')
        self.assertEqual(root1[1].criteria_set.id, 'b')

        a = root1[0]
        self.assertEqual(len(a), 2)
        self.assertCountEqual([node.criteria_set.id for node in a],
                              ('a1', 'a2'))

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        root1 = xmcda.criteria_sets['root1']
        a2 = xmcda.criteria_sets['a2']
        hierarchy = CriteriaSetsHierarchy(xml, xmcda)
        self.assertEqual(root1, hierarchy[0].criteria_set)
        self.assertEqual(a2, hierarchy[0][0][1].criteria_set)

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)
        result = utf8_to_utf8(self.xml_1, CriteriaSetsHierarchy)
        self.maxDiff = None
        self.assertEqual(source, result)

        source = compact_xml(self.xml_empty)
        result = utf8_to_utf8(self.xml_empty, CriteriaSetsHierarchy)
        self.assertEqual(source, result)
