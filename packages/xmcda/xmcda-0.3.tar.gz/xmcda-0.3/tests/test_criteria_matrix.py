from xmcda.criteria import Criterion
from xmcda.criteria_matrix import CriteriaMatrix
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestCriteriaMatrix(XMCDATestCase):

    def test_init_with_values(self):
        matrix = CriteriaMatrix(id="m1", attr="a matrix attr")
        self.assertEqual(matrix.id, "m1")
        self.assertEqual(matrix.attr, "a matrix attr")

    def test_1(self):
        matrix = CriteriaMatrix()
        with self.assertRaises(KeyError):
            matrix['o1']
        with self.assertRaises(KeyError):
            matrix['o1']['o2'] = 2

        o1 = Criterion(id='o1')
        o4 = Criterion(id='o4')
        v = Values()
        matrix[o1][o4] = v
        self.assertEqual(v, matrix[o1][o4])
        self.assertEqual(v, matrix['o1'][o4])  # access with ids as strings
        self.assertEqual(v, matrix[o1]['o4'])
        self.assertEqual(v, matrix['o1']['o4'])

    def test_get_criterion(self):
        matrix = CriteriaMatrix()
        self.assertIsNone(matrix.get_criterion('o1'))
        o1 = Criterion(id='o1')
        o2 = Criterion(id='o2')
        matrix[o1][o2] = Values()
        self.assertEqual(matrix.get_criterion('o1'), o1)
        self.assertEqual(matrix.get_criterion('o2'), o2)
        self.assertIsNone(matrix.get_criterion('o4'))

    xml_1 = '''
    <criteriaMatrix id="id m" name="name m" mcdaConcept="mcdaConcept m">
        <row>
            <criterionID>o1</criterionID>
            <column>
                <criterionID>o1</criterionID>
                <values><value><real>11.0</real></value></values>
            </column>
            <column>
                <criterionID>o4</criterionID>
                <values><value><integer>14</integer></value></values>
            </column>
        </row>
        <row>
            <criterionID>o2</criterionID>
            <column>
                <criterionID>o2</criterionID>
                <values><value><NA/></value></values>
            </column>
            <column>
                <criterionID>o1</criterionID>
                <values><value><NA/></value></values>
            </column>
        </row>
        <row>
            <criterionID>o3</criterionID>
            <column>
                <criterionID>o1</criterionID>
                <values><value><NA/></value></values>
            </column>
        </row>
    </criteriaMatrix>
'''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        matrix = CriteriaMatrix(xml)

        self.assertEqual(matrix.id, 'id m')
        self.assertEqual(matrix.name, 'name m')
        self.assertEqual(matrix.mcda_concept, 'mcdaConcept m')

        rows = matrix.rows()
        self.assertEqual(3, len(rows))
        self.assertTrue('o1' in [a.id for a in rows])
        self.assertTrue('o2' in [a.id for a in rows])
        self.assertTrue('o3' in [a.id for a in rows])

        columns = matrix.columns()
        self.assertEqual(3, len(columns))
        self.assertTrue('o1' in [a.id for a in columns])
        self.assertTrue('o2' in [a.id for a in columns])
        self.assertTrue('o4' in [a.id for a in columns])

        # order of elements is preserved
        self.assertEqual(['o1', 'o2', 'o3'], [a.id for a in matrix.keys()])
        self.assertEqual(['o1', 'o4'], [a.id for a in matrix['o1']])

    def test_from_xml_with_xmcda(self):
        xml = self.read_xml(self.xml_1)
        xmcda = XMCDA()
        o1 = xmcda.criteria['o1']
        matrix = CriteriaMatrix(xml, xmcda)
        self.assertTrue(o1 in matrix.rows())

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, CriteriaMatrix)
        self.maxDiff = None
        self.assertEqual(source, result)
