from xmcda import set_version, version
from xmcda.categories import Category
from xmcda.categories_values import CategoriesValues, CategoryValues
from xmcda.schemas import XMCDA_3_1_1, XMCDA_4_0_0
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class _TestCategoryValue:

    xml = (  # noqa E731
        lambda s: f'''
        <{s.categoryValues} id="v1" name="v1-n" mcdaConcept="v1-m">
            <description>
                <comment>v1-c</comment>
            </description>
            <categoryID>o1</categoryID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
                <value>
                    <real>2.0</real>
                </value>
            </values>
        </{s.categoryValues}>'''
    )
    xml = property(xml)

    xml_empty = (  # noqa E731
        lambda s: f'<{s.categoryValues}/>'
    )
    xml_empty = property(xml_empty)

    def test_from_xml(self):
        category_value = CategoryValues(self.read_xml(self.xml))
        self.assertEqual(category_value.id, 'v1')
        self.assertEqual(category_value.name, 'v1-n')
        self.assertEqual(category_value.mcda_concept, 'v1-m')
        self.assertEqual(category_value.description.comment, 'v1-c')
        self.assertIsInstance(category_value.values, Values)
        self.assertEqual(len(category_value.values), 2)
        self.assertEqual(category_value.values[0].v, 1)
        self.assertEqual(category_value.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.categories['o1']
        category_value = CategoryValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(category_value.category, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CategoryValues)
        self._test_to_xml(self.xml_empty, CategoryValues)

    def test_is_numeric(self):
        category_value = CategoryValues(self.read_xml(self.xml))
        self.assertTrue(category_value.is_numeric())
        category_value.values[1] = Value('a string')
        self.assertFalse(category_value.is_numeric())


class TestCategoryValue_v3(_TestCategoryValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.categoryValues = 'categoryValue'

    def tearDown(self):
        set_version(self.current_version)


class TestCategoryValue_v4(_TestCategoryValue, XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.categoryValues = 'categoryValues'

    def tearDown(self):
        set_version(self.current_version)


class _TestCategoriesValues:

    xml = (  # noqa E731
        lambda s: f'''
    <categoriesValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <{s.categoryValues} id="v1">
            <categoryID>o1</categoryID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </{s.categoryValues}>
        <{s.categoryValues} id="v2">
            <categoryID>o2</categoryID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </{s.categoryValues}>
    </categoriesValues>'''
    )
    xml = property(xml)

    xml_empty = '''<categoriesValues/>'''

    def test_init_with_kw(self):
        categories_values = CategoriesValues(id='an_id', h=6.626e-34)
        self.assertEqual(categories_values.id, 'an_id')
        self.assertEqual(categories_values.h, 6.626e-34)

    def test_from_xml(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        self.assertEqual(categories_values.id, 'vs1')
        self.assertEqual(categories_values.name, 'vs1-n')
        self.assertEqual(categories_values.mcda_concept, 'vs1-m')
        self.assertEqual(categories_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(categories_values), 2)
        for category_value in categories_values:
            self.assertIsInstance(category_value, CategoryValues)
        self.assertEqual(categories_values[1].id, 'v2')

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o2 = xmcda.categories['o2']
        categories_values = \
            CategoriesValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(len(categories_values), 2)
        self.assertEqual({c.id for c in xmcda.categories},
                         {'o1', 'o2'})
        # check that the existing element is the same object in xxx_values
        self.assertEqual(id(categories_values[1].category), id(o2))

    def test_to_xml(self):
        self._test_to_xml(self.xml, CategoriesValues)
        self._test_to_xml(self.xml_empty, CategoriesValues)

    def test_get_item(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        self.assertEqual(categories_values[0].id, 'v1')
        self.assertEqual(categories_values['o2'].category.id, 'o2')
        self.assertEqual(categories_values['o2'].category.id,
                         categories_values[1].category.id)
        o1 = categories_values[0].category
        self.assertEqual(categories_values[o1],
                         categories_values[0])
        with self.assertRaises(IndexError):
            categories_values[Category(id='unknown')]
        with self.assertRaises(IndexError):
            categories_values['unknown']
        with self.assertRaises(TypeError):
            categories_values[None]
        with self.assertRaises(TypeError):
            categories_values[2.3]

    def test_set_item(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        value_1, value_2 = categories_values[0], categories_values[1]
        category_1, category_2 = value_1.category, value_2.category
        category_3 = Category(id='o3')
        value_3 = CategoryValues(id='v3')
        value_3.category = category_3
        value_3.value = Values('moo')

        categories_values[0] = value_3
        self.assertEqual(categories_values[0].value[0].v, 'moo')

        categories_values[category_2] = value_3
        self.assertEqual(categories_values[1], value_3)

        with self.assertRaises(IndexError):
            categories_values['o1'] = value_2

        value_3.category = category_1
        categories_values['o1'] = value_2
        self.assertEqual(categories_values[0], value_2)

        with self.assertRaises(IndexError):
            categories_values[Category(id='unknown')] = value_1

        with self.assertRaises(TypeError):
            categories_values[None] = value_1
        with self.assertRaises(TypeError):
            categories_values[2.3] = value_1

    def test_categories(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        categories = categories_values.categories()
        self.assertSetEqual({Category},
                            {type(category)
                             for category in categories})
        self.assertSetEqual({'o1', 'o2'},
                            {category.id for category in categories})

    def test_is_numeric(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        self.assertTrue(categories_values.is_numeric())
        categories_values['o1'].values = Values("blah")
        self.assertFalse(categories_values.is_numeric())


class TestCategoriesValues_v3(_TestCategoriesValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)
        self.categoryValues = 'categoryValue'

    def tearDown(self):
        set_version(self.current_version)


class TestCategoriesValues_v4(_TestCategoriesValues, XMCDATestCase):
    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_4_0_0)
        self.categoryValues = 'categoryValues'

    def tearDown(self):
        set_version(self.current_version)
