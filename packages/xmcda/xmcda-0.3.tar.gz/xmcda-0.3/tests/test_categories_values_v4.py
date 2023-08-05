from xmcda.categories import Category
from xmcda.categories_values import CategoriesValues, CategoryValues
from xmcda.value import Value, Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCategoryValues(XMCDATestCase):

    xml = '''
        <categoryValues id="v1" name="v1-n" mcdaConcept="v1-m">
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
        </categoryValues>
    '''

    def test_from_xml(self):
        category_values = CategoryValues(self.read_xml(self.xml))
        self.assertEqual(category_values.id, 'v1')
        self.assertEqual(category_values.name, 'v1-n')
        self.assertEqual(category_values.mcda_concept, 'v1-m')
        self.assertEqual(category_values.description.comment, 'v1-c')
        self.assertIsInstance(category_values.values, Values)
        self.assertEqual(len(category_values.values), 2)
        self.assertEqual(category_values.values[0].v, 1)
        self.assertEqual(category_values.values[1].v, 2.0)

    def test_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        o1 = xmcda.categories['o1']
        category_values = CategoryValues(self.read_xml(self.xml), xmcda)
        self.assertEqual(category_values.category, o1)

    def test_to_xml(self):
        self._test_to_xml(self.xml, CategoryValues)

    def test_is_numeric(self):
        category_values = CategoryValues(self.read_xml(self.xml))
        self.assertTrue(category_values.is_numeric())
        category_values.values[1] = Value('a string')
        self.assertFalse(category_values.is_numeric())


class TestCategoriesValues(XMCDATestCase):

    xml = '''
    <categoriesValues id="vs1" name="vs1-n" mcdaConcept="vs1-m">
        <description>
            <comment>vs1 comment</comment>
        </description>
        <categoryValues id="v1">
            <categoryID>o1</categoryID>
            <values>
                <value>
                    <integer>1</integer>
                </value>
            </values>
        </categoryValues>
        <categoryValues id="v2">
            <categoryID>o2</categoryID>
            <values>
                <value>
                    <integer>2</integer>
                </value>
                <value>
                    <integer>22</integer>
                </value>
            </values>
        </categoryValues>
    </categoriesValues>'''

    def test_from_xml(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        self.assertEqual(categories_values.id, 'vs1')
        self.assertEqual(categories_values.name, 'vs1-n')
        self.assertEqual(categories_values.mcda_concept, 'vs1-m')
        self.assertEqual(categories_values.description.comment,
                         'vs1 comment')

        self.assertEqual(len(categories_values), 2)
        for category_values in categories_values:
            self.assertIsInstance(category_values, CategoryValues)
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

    def test_get_item(self):
        categories_values = CategoriesValues(self.read_xml(self.xml))
        self.assertEqual(categories_values[0].id, 'v1')
        self.assertEqual(categories_values['o2'].category.id, 'o2')
        self.assertEqual(categories_values['o2'].category.id,
                         categories_values[1].category.id)
        o1 = categories_values[0].category
        self.assertEqual(categories_values[o1],
                         categories_values[0])
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
