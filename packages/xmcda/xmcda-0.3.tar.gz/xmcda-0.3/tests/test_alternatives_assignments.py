from xmcda.alternatives_assignments import (
    AlternativeAssignment,
    AlternativesAssignments,
    CategoriesInterval,
)
from xmcda.categories import Category
from xmcda.categories_sets import CategoriesSet
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class TestCategoriesInterval(XMCDATestCase):

    def test_init_with_kw(self):
        categories_interval = CategoriesInterval(id='cI id', attr=8)
        self.assertEqual(categories_interval.id, 'cI id')
        self.assertEqual(categories_interval.attr, 8)

    xml_both_bounds = '''
        <categoriesInterval>
            <lowerBound>
                <categoryID>c01</categoryID>
            </lowerBound>
            <upperBound>
                <categoryID>c02</categoryID>
            </upperBound>
        </categoriesInterval>'''

    def test_both_bounds_from_xml(self):
        xml = self.read_xml(self.xml_both_bounds)
        categories_interval = CategoriesInterval(xml)
        self.assertEqual(categories_interval.lower_bound.id, 'c01')
        self.assertEqual(categories_interval.upper_bound.id, 'c02')

    def test_both_bounds_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_both_bounds)
        xmcda = XMCDA()
        c01 = xmcda.categories['c01']
        categories_interval = CategoriesInterval(xml, xmcda)
        self.assertEqual(categories_interval.lower_bound, c01)
        self.assertEqual(len(xmcda.categories), 2)

    def test_both_bounds_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_both_bounds)

        result = utf8_to_utf8(self.xml_both_bounds, CategoriesInterval)
        self.maxDiff = None
        self.assertEqual(source, result)

    # --
    xml_lower_bound_only = '''
        <!-- lowerBound alone -->
        <categoriesInterval>
            <lowerBound>
                <categoryID>c03</categoryID>
            </lowerBound>
        </categoriesInterval>
    '''

    def test_lower_bound_only(self):
        xml = self.read_xml(self.xml_lower_bound_only)
        categories_interval = CategoriesInterval(xml)
        self.assertEqual(categories_interval.lower_bound.id, 'c03')
        self.assertIsNone(categories_interval.upper_bound)

    def test_lower_bound_only_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_lower_bound_only)

        result = utf8_to_utf8(self.xml_lower_bound_only, CategoriesInterval)
        self.maxDiff = None
        self.assertEqual(source, result)

    xml_upper_bound_only = '''
        <!-- upperBound alone -->
        <categoriesInterval>
            <upperBound>
                <categoryID>c04</categoryID>
            </upperBound>
        </categoriesInterval>
    '''

    def test_upper_bound_only(self):
        xml = self.read_xml(self.xml_upper_bound_only)
        categories_interval = CategoriesInterval(xml)
        self.assertIsNone(categories_interval.lower_bound)
        self.assertEqual(categories_interval.upper_bound.id, 'c04')

    def test_upper_bound_only_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_upper_bound_only)

        result = utf8_to_utf8(self.xml_upper_bound_only, CategoriesInterval)
        self.maxDiff = None
        self.assertEqual(source, result)


class TestAlternativeAssignment(XMCDATestCase):

    def test_init_with_kw(self):
        aA = AlternativeAssignment(id='aA id', attr=9)
        self.assertEqual(aA.id, 'aA id')
        self.assertEqual(aA.attr, 9)

    xml_no_values = '''
        <alternativeAssignment id="aA1" name="aA1n" mcdaConcept="aA1m">
            <description>
                <author>aA1 description author 1</author>
                <comment>aA1 description comment</comment>
            </description>
            <alternativeID>a1</alternativeID>
            <categoriesInterval>
                <lowerBound>
                    <categoryID>c1</categoryID>
                </lowerBound>
                <upperBound>
                    <categoryID>c2</categoryID>
                </upperBound>
            </categoriesInterval>
            <!-- no values -->
        </alternativeAssignment>
    '''

    xmcda_no_value = make_xmcda_v4(xml_no_values)

    def test_categories_interval_no_values(self):
        xml = self.read_xml(self.xml_no_values)
        aA = AlternativeAssignment(xml)
        self.assertEqual(aA.id, 'aA1')
        self.assertEqual(aA.name, 'aA1n')
        self.assertEqual(aA.mcda_concept, 'aA1m')
        self.assertEqual(aA.description.authors[0], 'aA1 description author 1')
        self.assertEqual(aA.description.comment, 'aA1 description comment')
        categories_interval = aA.categories_interval
        self.assertIsInstance(categories_interval.lower_bound, Category)
        self.assertIsInstance(categories_interval.upper_bound, Category)
        self.assertEqual(categories_interval.lower_bound.id, 'c1')
        self.assertEqual(categories_interval.upper_bound.id, 'c2')
        self.assertEqual(len(aA.values), 0)

    def test_categories_interval_no_values_with_xmcda(self):
        xml = self.read_xml(self.xml_no_values)
        xmcda = XMCDA()
        c1 = xmcda.categories['c1']
        aA = AlternativeAssignment(xml, xmcda)
        self.assertEqual(aA.categories_interval.lower_bound, c1)
        a1 = aA.alternative
        self.assertTrue(a1 in xmcda.alternatives)

    # --
    xml_with_values = '''
        <alternativeAssignment>
            <alternativeID>a2</alternativeID>
            <categoriesInterval>
                <lowerBound>
                    <categoryID>c2</categoryID>
                </lowerBound>
                <upperBound>
                    <categoryID>c3</categoryID>
                </upperBound>
            </categoriesInterval>
            <!-- with values -->
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <label>big was here</label>
                </value>
            </values>
        </alternativeAssignment>
    '''

    def test_with_values(self):
        xml = self.read_xml(self.xml_with_values)
        aA = AlternativeAssignment(xml)
        self.assertIsInstance(aA.values, Values)
        self.assertEqual(len(aA.values), 2)

    # --
    xml_categoryID = '''
        <!-- categoryID -->
        <alternativeAssignment id="aA5">
            <alternativeID>a5</alternativeID>
            <categoryID>aA5-a5-c1</categoryID>
            <values>
                <value>
                    <label>aA5-a5-c1 value</label>
                </value>
            </values>
        </alternativeAssignment>
    '''

    def test_categoryID(self):
        xml = self.read_xml(self.xml_categoryID)
        aA = AlternativeAssignment(xml)
        self.assertIsInstance(aA.category, Category)
        self.assertEqual(aA.category.id, 'aA5-a5-c1')
        # the rest is tested above

    def test_categoryID_with_xmcda(self):
        xml = self.read_xml(self.xml_categoryID)
        xmcda = XMCDA()
        c1 = xmcda.categories['aA5-a5-c1']
        aA = AlternativeAssignment(xml, xmcda)
        self.assertIsInstance(aA.category, Category)
        self.assertEqual(aA.category, c1)

    # --
    xml_categoriesSetID = '''
        <!-- categoriesSetID -->
        <alternativeAssignment id="aA6">
            <alternativeID>aA6-a6</alternativeID>
            <categoriesSetID>aA6-a6-cS1</categoriesSetID>
        </alternativeAssignment>'''

    def test_categoriesSetID(self):
        xml = self.read_xml(self.xml_categoriesSetID)
        aA = AlternativeAssignment(xml)
        self.assertIsInstance(aA.categories_set, CategoriesSet)
        self.assertEqual(aA.categories_set.id, 'aA6-a6-cS1')
        # the rest is tested above

    def test_categoriesSetID_with_XMCDA(self):
        xml = self.read_xml(self.xml_categoriesSetID)
        xmcda = XMCDA()
        cS1 = xmcda.categories_sets['aA6-a6-cS1']
        aA = AlternativeAssignment(xml, xmcda)
        self.assertIsInstance(aA.categories_set, CategoriesSet)
        self.assertEqual(aA.categories_set, cS1)

    xml_empty = '<alternativeAssignment/>'

    def test_to_xml(self):
        self._test_to_xml(self.xml_no_values, AlternativeAssignment)
        self._test_to_xml(self.xml_empty, AlternativeAssignment)


class TestAlternativesAssignments(XMCDATestCase):

    def test_init_with_kw(self):
        aAs = AlternativesAssignments(id='aAs id', attr=10)
        self.assertEqual(aAs.id, 'aAs id')
        self.assertEqual(aAs.attr, 10)

    xml_no_values = '''
    <alternativesAssignments id="asAs1" name="asAs1_n" mcdaConcept="asAs1_m">
        <description>
            <author>asAs1 desc. author 1</author>
            <comment>asAs1 desc. comment</comment>
        </description>
        <alternativeAssignment id="aA1" name="aA1n" mcdaConcept="aA1m">
            <description>
                <author>aA1 desc. author 1</author>
                <comment>aA1 desc. comment</comment>
            </description>
            <alternativeID>a1</alternativeID>
            <categoryID>c1</categoryID>
            <!-- no values -->
        </alternativeAssignment>
        <alternativeAssignment id="aA2" name="aA2n" mcdaConcept="aA2m">
            <alternativeID>a2</alternativeID>
            <categoryID>c2</categoryID>
            <!-- no values -->
        </alternativeAssignment>
    </alternativesAssignments>
    '''

    xmcda_no_values = make_xmcda_v4(xml_no_values)

    xml_values = '''
    <alternativesAssignments>
        <alternativeAssignment>
            <alternativeID>a1</alternativeID>
            <categoriesSetID>c1</categoriesSetID>
            <values><value><label>high</label></value></values>
        </alternativeAssignment>
    </alternativesAssignments>
'''

    xml_empty = "<alternativesAssignments/>"

    def test_load_with_xmcda(self):
        xmcda = XMCDA()
        # a01 = Alternative(id='a01')
        # xmcda.alternatives.append(a01)
        xml_source = TestAlternativesAssignments.xmcda_no_values
        xmcda.fromstring(xml_source)
        self.assertEqual(len(xmcda.alternatives), 2)
        self.assertEqual(len(xmcda.alternatives_assignments_list), 1)
        self.assertEqual(len(xmcda.alternatives_assignments_list[0]), 2)

        asAs1 = xmcda.alternatives_assignments_list[0]
        self.assertEqual(asAs1.id, 'asAs1')
        self.assertEqual(asAs1.name, 'asAs1_n')
        self.assertEqual(asAs1.mcda_concept, 'asAs1_m')
        self.assertEqual(asAs1.description.authors[0], 'asAs1 desc. author 1')
        self.assertEqual(asAs1.description.comment, 'asAs1 desc. comment')

    def test_to_xml_1(self):
        self._test_to_xml(self.xml_no_values, AlternativesAssignments)
        self._test_to_xml(self.xml_empty, AlternativesAssignments)
        self._test_to_xml(self.xml_values, AlternativesAssignments)
