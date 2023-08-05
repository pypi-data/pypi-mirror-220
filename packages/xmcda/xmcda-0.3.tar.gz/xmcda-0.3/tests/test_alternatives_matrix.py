from xmcda.alternatives import Alternative
from xmcda.alternatives_matrix import AlternativesMatrix
from xmcda.value import Values
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestAlternativesMatrix(XMCDATestCase):

    def test_init_with_values(self):
        matrix = AlternativesMatrix(id="m1", attr="a matrix attr")
        self.assertEqual(matrix.id, "m1")
        self.assertEqual(matrix.attr, "a matrix attr")

    def test_1(self):
        matrix = AlternativesMatrix()
        with self.assertRaises(KeyError):
            matrix['o1']
        with self.assertRaises(KeyError):
            matrix['o1']['o2'] = 2

        o1 = Alternative(id='o1')
        o4 = Alternative(id='o4')
        v = Values()
        matrix[o1][o4] = v
        self.assertEqual(v, matrix[o1][o4])
        self.assertEqual(v, matrix['o1'][o4])  # access with ids as strings
        self.assertEqual(v, matrix[o1]['o4'])
        self.assertEqual(v, matrix['o1']['o4'])

    def test_get_alternative(self):
        matrix = AlternativesMatrix()
        self.assertIsNone(matrix.get_alternative('o1'))
        o1 = Alternative(id='o1')
        o2 = Alternative(id='o2')
        matrix[o1][o2] = Values()
        self.assertEqual(matrix.get_alternative('o1'), o1)
        self.assertEqual(matrix.get_alternative('o2'), o2)
        self.assertIsNone(matrix.get_alternative('o4'))

    xml_1 = '''
    <alternativesMatrix id="id m" name="name m" mcdaConcept="mcdaConcept m">
        <row>
            <alternativeID>o1</alternativeID>
            <column>
                <alternativeID>o1</alternativeID>
                <values><value><real>11.0</real></value></values>
            </column>
            <column>
                <alternativeID>o4</alternativeID>
                <values><value><integer>14</integer></value></values>
            </column>
        </row>
        <row>
            <alternativeID>o2</alternativeID>
            <column>
                <alternativeID>o2</alternativeID>
                <values><value><NA/></value></values>
            </column>
            <column>
                <alternativeID>o1</alternativeID>
                <values><value><NA/></value></values>
            </column>
        </row>
        <row>
            <alternativeID>o3</alternativeID>
            <column>
                <alternativeID>o1</alternativeID>
                <values><value><NA/></value></values>
            </column>
        </row>
    </alternativesMatrix>
'''

    def test_from_xml(self):
        xml = self.read_xml(self.xml_1)
        matrix = AlternativesMatrix(xml)

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
        o1 = xmcda.alternatives['o1']
        matrix = AlternativesMatrix(xml, xmcda)
        self.assertTrue(o1 in matrix.rows())

    def test_to_xml(self):
        from .utils import compact_xml, utf8_to_utf8
        source = compact_xml(self.xml_1)

        result = utf8_to_utf8(self.xml_1, AlternativesMatrix)
        self.maxDiff = None
        self.assertEqual(source, result)
