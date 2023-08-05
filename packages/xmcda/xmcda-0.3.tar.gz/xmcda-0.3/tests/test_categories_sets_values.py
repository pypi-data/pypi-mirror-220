from xmcda import set_version, version
from xmcda.categories_sets import CategoriesSet
from xmcda.categories_sets_values import (
    CategoriesSetsValues,
    CategoriesSetValues,
)
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestCategoriesSetValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)

    xml = (  # noqa E731
        lambda s: f'''
        <{s.categoriesSetValues} id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <categoriesSetID>o1</categoriesSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </{s.categoriesSetValues}>'''
    )
    xml = property(xml)

    xml_empty = lambda s: f'<{s.categoriesSetValues}/>'  # noqa E731
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        categories_set_values = CategoriesSetValues(self.read_xml(self.xml))
        self.assertEqual(categories_set_values.id, 'v1')
        self.assertEqual(categories_set_values.name, 'v1-n')
        self.assertEqual(categories_set_values.mcda_concept, 'v1-m')
        self.assertEqual(categories_set_values.description.comment, 'v1-c')
        self.assertIsInstance(categories_set_values.values, Values)
        self.assertEqual(len(categories_set_values.values), 2)
        self.assertEqual(categories_set_values.values[0].v, 1)
        self.assertEqual(categories_set_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.categories_sets['o1']
        categories_set_values = (
          CategoriesSetValues(self.read_xml(self.xml), xmcda))
        self.assertEqual(categories_set_values.categories_set, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CategoriesSetValues)
        # accept to read/write an empty tag
        self._test_to_xml(self.xml_empty, CategoriesSetValues)


class TestCategoriesSetValue_v3(_TestCategoriesSetValues, XMCDATestCase):
    version = XMCDA_3_1_1
    categoriesSetValues = 'categoriesSetValue'


class TestCategoriesSetValue_v4(_TestCategoriesSetValues, XMCDATestCase):
    version = XMCDA_4_0_0
    categoriesSetValues = 'categoriesSetValues'


class _TestCategoriesSetsValues:

    def setUp(self):
        self.current_version = version()
        set_version(self.version)

    def tearDown(self):
        set_version(self.current_version)


    xml = (  # noqa E731
        lambda s: f'''
    <categoriesSetsValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.categoriesSetValues} id="v1">
            <categoriesSetID>o1</categoriesSetID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.categoriesSetValues}>
        <{s.categoriesSetValues} id="v2">
            <categoriesSetID>o2</categoriesSetID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.categoriesSetValues}>
    </categoriesSetsValues>'''
    )
    xml = property(xml)

    xml_empty = '<categoriesSetsValues/>'

    def test_init_with_args(self):
        categories_sets_values = CategoriesSetsValues(id='csv1', attr=12)
        self.assertEqual(categories_sets_values.id, 'csv1')
        self.assertEqual(categories_sets_values.attr, 12)

    def test_from_xml(self):
        categories_sets_values = \
            CategoriesSetsValues(self.read_xml(self.xml))
        self.assertEqual(categories_sets_values.id, 'vs1')
        self.assertEqual(categories_sets_values.name, 'vs1-n')
        self.assertEqual(categories_sets_values.mcda_concept, 'vs1-m')
        self.assertEqual(categories_sets_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(categories_sets_values), 2)
        for categories_set_values in categories_sets_values:
            self.assertIsInstance(categories_set_values,
                                  CategoriesSetValues)
        self.assertEqual(categories_sets_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.categories_sets['o2']
        categories_sets_values = \
            CategoriesSetsValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(categories_sets_values), 2)
        self.assertEqual({c.id for c in xmcda.categories_sets},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(categories_sets_values[1].categories_set),
                         id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, CategoriesSetsValues)
        self._test_to_xml(self.xml_empty, CategoriesSetsValues)

    def test_get_item(self):
        categories_sets_values = \
            CategoriesSetsValues(self.read_xml(self.xml))
        self.assertEqual(categories_sets_values[0].id, 'v1')
        self.assertEqual(categories_sets_values['o2'].categories_set.id,
                         'o2')
        self.assertEqual(categories_sets_values['o2'].categories_set.id,
                         categories_sets_values[1].categories_set.id)
        o1 = categories_sets_values[0].categories_set
        self.assertEqual(categories_sets_values[o1],
                         categories_sets_values[0])

        with self.assertRaises(IndexError):
            categories_sets_values[CategoriesSet(id='unknown')]
        with self.assertRaises(IndexError):
            categories_sets_values['unknown']

        with self.assertRaises(TypeError):
            categories_sets_values[None]
        with self.assertRaises(TypeError):
            categories_sets_values[2.3]

    def test_set_item(self):
        categories_sets_values = \
            CategoriesSetsValues(self.read_xml(self.xml))
        value_1 = categories_sets_values[0]
        value_2 = categories_sets_values[1]
        categoriesSet_1 = value_1.categories_set
        categoriesSet_2 = value_2.categories_set
        categoriesSet_3 = CategoriesSet(id='o3')
        value_3 = CategoriesSetValues(id='v3')
        value_3.categories_set = categoriesSet_3
        value_3.value = Values('moo')

        categories_sets_values[0] = value_3
        self.assertEqual(categories_sets_values[0].value[0].v, 'moo')

        categories_sets_values[categoriesSet_2] = value_3
        self.assertEqual(categories_sets_values[1], value_3)

        with self.assertRaises(IndexError):
            categories_sets_values[CategoriesSet(id='unknown')] = value_2

        with self.assertRaises(IndexError):
            categories_sets_values['o1'] = value_2

        value_3.categories_set = categoriesSet_1
        categories_sets_values['o1'] = value_2
        self.assertEqual(categories_sets_values[0], value_2)

        with self.assertRaises(TypeError):
            categories_sets_values[None] = value_1
        with self.assertRaises(TypeError):
            categories_sets_values[2.3] = value_1


class TestCategoriesSetsValue_v3(_TestCategoriesSetsValues, XMCDATestCase):
    version = XMCDA_3_1_1
    categoriesSetValues = 'categoriesSetValue'


class TestCategoriesSetsValue_v4(_TestCategoriesSetsValues, XMCDATestCase):
    version = XMCDA_4_0_0
    categoriesSetValues = 'categoriesSetValues'
