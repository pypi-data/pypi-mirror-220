from xmcda.categories_profiles import (
    CategoriesProfiles,
    CategoryProfile,
    Profile,
)
from xmcda.value import Rational
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, make_xmcda_v4


class TestType(XMCDATestCase):

    def test_get(self):
        T = CategoryProfile.Type
        self.assertEqual(T.get('bounding'), T.BOUNDING)
        self.assertRaises(KeyError, T.get, None)
        self.assertRaises(KeyError, T.get, 'invalid')
        self.assertRaises(KeyError, T.get, 1)


class TestProfile(XMCDATestCase):

    def test_init(self):
        profile = Profile()
        self.assertIsNone(profile.alternative)

        from xmcda.alternatives import Alternative
        profile = Profile(alternative=Alternative(id='a1'))
        self.assertEqual(profile.alternative.id, 'a1')


class TestCategoryProfile(XMCDATestCase):

    xml_bounding_profile = '''
        <categoryProfile id="cp1" name="cp1-n" mcdaConcept="cp1-m">
            <description>
                <comment>cp1 desc.comment</comment>
            </description>
            <categoryID>c1</categoryID>
            <bounding>
                <lowerBound>
                    <alternativeID>a1</alternativeID>
                </lowerBound>
                <upperBound>
                    <alternativeID>a2</alternativeID>
                </upperBound>
            </bounding>
        </categoryProfile>
    '''

    def test_init_with_args(self):
        category_profile = CategoryProfile(id='cp', attr=6)
        self.assertEqual(category_profile.id, 'cp')
        self.assertEqual(category_profile.attr, 6)

    def test_bounding_profile_from_xml(self):
        xml = self.read_xml(self.xml_bounding_profile)
        category_profile = CategoryProfile(xml)
        self.assertEqual(category_profile.id, 'cp1')
        self.assertEqual(category_profile.name, 'cp1-n')
        self.assertEqual(category_profile.mcda_concept, 'cp1-m')
        self.assertIsInstance(category_profile.upper_bound, Profile)
        self.assertIsInstance(category_profile.lower_bound, Profile)
        self.assertEqual(category_profile.central_profile, None)

    def test_bounding_profile_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_bounding_profile)
        c1 = xmcda.categories['c1']
        a1 = xmcda.alternatives['a1']
        category_profile = CategoryProfile(xml, xmcda)

        self.assertEqual(category_profile.category, c1)
        self.assertEqual(category_profile.lower_bound.alternative, a1)

    def test_bounding_profile_to_xml(self):
        self._test_to_xml(self.xml_bounding_profile, CategoryProfile)

    xml_bounding_profile_with_values = '''
        <categoryProfile>
            <!-- a categoryProfile with values -->
            <categoryID>c3</categoryID>
            <bounding>
                <lowerBound>
                    <alternativeID>a3</alternativeID>
                    <values>
                        <value>
                            <real>0.5</real>
                        </value>
                        <value>
                            <integer>2</integer>
                        </value>
                        <value>
                            <rational>
                                <numerator>3</numerator>
                                <denominator>5</denominator>
                            </rational>
                        </value>
                    </values>
                </lowerBound>
                <upperBound>
                    <alternativeID>a4</alternativeID>
                </upperBound>
            </bounding>
        </categoryProfile>
        '''

    def test_bounding_profile_from_xml_with_values(self):
        xml = self.read_xml(self.xml_bounding_profile_with_values)
        category_profile = CategoryProfile(xml)
        self.assertIsInstance(category_profile.upper_bound, Profile)
        values = category_profile.lower_bound.values
        self.assertEqual(len(values), 3)
        self.assertIsInstance(values[0].v, float)
        self.assertIsInstance(values[1].v, int)
        self.assertIsInstance(values[2].v, Rational)
        self.assertIsInstance(category_profile.lower_bound, Profile)
        self.assertEqual(category_profile.central_profile, None)

    def test_bounding_profile_to_xml_with_values(self):
        self._test_to_xml(self.xml_bounding_profile_with_values,
                          CategoryProfile)

    xml_bounding_profile_no_lower_bound = '''
        <categoryProfile>
            <!-- Only one upper bound -->
            <categoryID>c10</categoryID>
            <bounding>
                <upperBound>
                    <alternativeID>a10</alternativeID>
                </upperBound>
            </bounding>
        </categoryProfile>
    '''

    def test_bounding_profile_no_lower_bound(self):
        xml = self.read_xml(self.xml_bounding_profile_no_lower_bound)
        category_profile = CategoryProfile(xml)
        self.assertIsNone(category_profile.lower_bound)
        self.assertIsInstance(category_profile.upper_bound, Profile)

    def test_bounding_profile_no_lower_bound_to_xml(self):
        self._test_to_xml(self.xml_bounding_profile_no_lower_bound,
                          CategoryProfile)

    xml_bounding_profile_no_upper_bound = '''
        <categoryProfile>
            <!-- Only one lower bound -->
            <categoryID>c12</categoryID>
            <bounding>
                <lowerBound>
                    <alternativeID>a11</alternativeID>
                </lowerBound>
            </bounding>
        </categoryProfile>
    '''

    def test_bounding_profile_no_upper_bound(self):
        xml = self.read_xml(self.xml_bounding_profile_no_upper_bound)
        category_profile = CategoryProfile(xml)
        self.assertIsInstance(category_profile.lower_bound, Profile)
        self.assertIsNone(category_profile.upper_bound)

    def test_bounding_profile_no_upper_bound_to_xml(self):
        self._test_to_xml(self.xml_bounding_profile_no_upper_bound,
                          CategoryProfile)

    xml_central_profile_no_values = '''
        <!-- categoryProfile / central -->
        <!-- no values -->
        <categoryProfile>
            <categoryID>c5</categoryID>
            <central>
                <alternativeID>a5</alternativeID>
            </central>
        </categoryProfile>
    '''

    def test_central_profile_no_values_from_xml(self):
        xml = self.read_xml(self.xml_central_profile_no_values)
        category_profile = CategoryProfile(xml)
        self.assertIsNone(category_profile.upper_bound)
        self.assertIsNone(category_profile.lower_bound)
        self.assertIsInstance(category_profile.central_profile, Profile)

    def test_central_profile_no_values_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_central_profile_no_values)
        c5 = xmcda.categories['c5']
        a5 = xmcda.alternatives['a5']
        category_profile = CategoryProfile(xml, xmcda)
        self.assertEqual(category_profile.category, c5)
        self.assertEqual(category_profile.central_profile.alternative, a5)

    def test_central_profile_no_values_to_xml(self):
        self._test_to_xml(self.xml_central_profile_no_values, CategoryProfile)

    xml_central_profile_with_values = '''
        <!-- w/ values -->
        <categoryProfile>
            <categoryID>c6</categoryID>
            <central>
                <alternativeID>a6</alternativeID>
                <values>
                    <value>
                        <integer>515</integer>
                    </value>
                    <value>
                        <integer>525</integer>
                    </value>
                </values>
            </central>
        </categoryProfile>
    '''

    # empty and w/ no category, make sure this is readable and serializable
    # even if it's invalid with respect to the XML Schema for XMCDA
    xml_central_profile_empty = '''
        <categoryProfile>
            <central/>
        </categoryProfile>
    '''

    def test_central_profile_with_values_from_xml(self):
        xml = self.read_xml(self.xml_central_profile_with_values)
        category_profile = CategoryProfile(xml)
        central_profile = category_profile.central_profile
        self.assertEqual(len(central_profile.values), 2)
        self.assertIsInstance(central_profile.values[0].v, int)

    def test_central_profile_with_values_to_xml(self):
        self._test_to_xml(self.xml_central_profile_with_values,
                          CategoryProfile)
        self._test_to_xml(self.xml_central_profile_empty, CategoryProfile)


class TestCategoriesProfiles(XMCDATestCase):

    xml_1 = '''
        <categoriesProfiles id="cps" name="cps-n" mcdaConcept="cps-m">
            <description>
                <comment>cps comment</comment>
            </description>
            <categoryProfile id="cp1" name="cp1-n" mcdaConcept="cp1-m">
                <categoryID>c1</categoryID>
                <bounding>
                    <lowerBound>
                        <alternativeID>a1</alternativeID>
                    </lowerBound>
                    <upperBound>
                        <alternativeID>a2</alternativeID>
                    </upperBound>
                </bounding>
            </categoryProfile>
        </categoriesProfiles>
    '''

    xml_empty = '<categoriesProfiles/>'

    def test_init_with_args(self):
        categories_profile = CategoriesProfiles(id='cp', attr=1)
        self.assertEqual(categories_profile.id, 'cp')
        self.assertEqual(categories_profile.attr, 1)

    def test_categories_profiles_from_xml(self):
        xml = self.read_xml(self.xml_1)
        categories_profiles = CategoriesProfiles(xml)
        self.assertEqual(categories_profiles.id, 'cps')
        self.assertEqual(categories_profiles.name, 'cps-n')
        self.assertEqual(categories_profiles.mcda_concept, 'cps-m')
        self.assertEqual(categories_profiles.description.comment,
                         'cps comment')
        self.assertEqual(len(categories_profiles), 1)
        self.assertIsInstance(categories_profiles[0], CategoryProfile)
        self.assertEqual(categories_profiles[0].id, 'cp1')

    def test_categories_profiles_from_xml_with_xmcda(self):
        xmcda = XMCDA()
        xml = self.read_xml(self.xml_1)
        c1 = xmcda.categories['c1']
        a1 = xmcda.alternatives['a1']
        categories_profiles = CategoriesProfiles(xml, xmcda)
        self.assertEqual(categories_profiles[0].category, c1)
        self.assertEqual(categories_profiles[0].lower_bound.alternative, a1)

    def test_categories_profiles_to_xml(self):
        self._test_to_xml(self.xml_1, CategoriesProfiles)

    xmcda_1 = make_xmcda_v4(xml_1)

    def test_load_with_xmcda(self):
        xmcda = XMCDA()
        xmcda.fromstring(self.xmcda_1)
        c1 = xmcda.categories['c1']
        a1 = xmcda.alternatives['a1']
        self.assertEqual(len(xmcda.categories_profiles_list), 1)
        categories_profiles = xmcda.categories_profiles_list[0]
        self.assertEqual(categories_profiles[0].category, c1)
        self.assertEqual(categories_profiles[0].lower_bound.alternative, a1)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, CategoriesProfiles)
        self._test_to_xml(self.xml_empty, CategoriesProfiles)
