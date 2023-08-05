from xmcda.program_parameters import ProgramParameter, ProgramParameters

from .utils import XMCDATestCase


class TestProgramParameters(XMCDATestCase):

    xml_1 = '''
        <programParameters>
            <description><comment>prg params comment</comment></description>
            <programParameter id="p1" name="n1" mcdaConcept="m1">
                <description><comment>p1 comment</comment></description>
                <values>
                        <value>
                                <boolean>false</boolean>
                        </value>
                </values>
            </programParameter>
            <programParameter id="p2" name="alternative">
                <values>
                    <value>
                        <label>a08</label>
                    </value>
                </values>
            </programParameter>
        </programParameters>'''

    xml_2 = '''<programParameters id="empty-set"/>'''

    def test_load_xml(self):
        params = ProgramParameters(self.read_xml(self.xml_1))
        self.assertEqual(params.description.comment, 'prg params comment')
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0].id, 'p1')
        self.assertEqual(params[0].name, 'n1')
        self.assertEqual(params[0].mcda_concept, 'm1')
        self.assertEqual(params[0].description.comment, 'p1 comment')

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, ProgramParameters)
        self._test_to_xml(self.xml_2, ProgramParameters)

    def test_append_remove(self):
        params = ProgramParameters(id='params')
        p1, p2, p3, p4 = [ProgramParameter(id=x)
                          for x in ('p1', 'p2', 'p3', 'p4')]
        for _ in (p1, p2, p3, p4):
            params.append(_)
        self.assertCountEqual(params, [p1, p2, p3, p4])

        params.remove(p2)
        self.assertCountEqual(params, [p1, p3, p4])

        params.remove(p3.id)  # remove by id
        self.assertCountEqual(params, [p1, p4])


class TestProgramParameter(XMCDATestCase):

    xml_1 = '''
        <programParameter id="p1" name="pn1" mcdaConcept="pm1">
            <description><comment>param comment</comment></description>
            <values>
                <value>
                    <boolean>false</boolean>
                </value>
            </values>
        </programParameter>'''

    def test_load_xml(self):
        param = ProgramParameter(self.read_xml(self.xml_1))
        self.assertEqual(param.id, 'p1')
        self.assertEqual(param.name, 'pn1')
        self.assertEqual(param.mcda_concept, 'pm1')
        self.assertEqual(param.description.comment, 'param comment')
        self.assertEqual(len(param.values), 1)
        self.assertEqual(param.values[0].v, False)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, ProgramParameter)
