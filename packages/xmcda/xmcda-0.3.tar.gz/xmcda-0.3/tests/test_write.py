# -*- coding: utf-8 -*-
from lxml import etree

from xmcda import set_version, version
from xmcda.alternatives import Alternative
from xmcda.criteria import Criterion
from xmcda.description import Description
from xmcda.performance_table import PerformanceTable
from xmcda.schemas import XMCDA_3_1_1
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase, compact_xml


class TestWriteXMCDA(XMCDATestCase):

    xml_1 = '''
<xmcda:XMCDA xmlns:xmcda="http://www.decision-deck.org/2019/XMCDA-3.1.1">
  <alternatives id="alts_id" name="alts_name" mcdaConcept="alts_mcdaConcept">
    <alternative id="a01" name="n01" mcdaConcept="m01">
      <type>real</type>
      <active>true</active>
    </alternative>
    <alternative id="a02">
      <type>real</type>
      <active>false</active>
    </alternative>
    <alternative id="a03">
      <type>fictive</type>
      <active>true</active>
    </alternative>
  </alternatives>
</xmcda:XMCDA>
'''

    @staticmethod
    def build_xmcda_for_xml_1():
        '''Builds a object corresponding to self.xml_1'''
        xmcda = XMCDA()
        xmcda.alternatives.id = 'alts_id'
        xmcda.alternatives.name = 'alts_name'
        xmcda.alternatives.mcda_concept = 'alts_mcdaConcept'

        a01 = Alternative(id='a01', name='n01', mcda_concept='m01')
        a02 = Alternative(id='a02')
        a02.active = False
        a03 = Alternative(id='a03')
        a03.is_real = False
        xmcda.alternatives.append(a01)
        xmcda.alternatives.append(a02)
        xmcda.alternatives.append(a03)
        return xmcda

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)

    def tearDown(self):
        set_version(self.current_version)

    def test_to_xml(self):
        self.maxDiff = None
        import xmcda
        xmcda.set_export_defaults(True)

        xmcda = TestWriteXMCDA.build_xmcda_for_xml_1()

        s = etree.tounicode(xmcda.to_xml())
        self.assertEqual(compact_xml(self.xml_1), s)

    def test_write(self):
        self.maxDiff = None
        import xmcda
        xmcda.set_export_defaults(True)

        xmcda = TestWriteXMCDA.build_xmcda_for_xml_1()

        from io import BytesIO
        binary_stream = BytesIO()
        xmcda.write(binary_stream,
                    xml_declaration=False, pretty_print=False)
        self.assertEqual(compact_xml(self.xml_1),
                         binary_stream.getvalue().decode('utf-8'))

    def test_write_specific_tags(self):
        self.maxDiff = None
        import xmcda
        xmcda.set_export_defaults(True)

        xmcda = TestWriteXMCDA.build_xmcda_for_xml_1()
        xmcda.criteria.append(Criterion(id='c01'))
        xmcda.performance_tables.append(PerformanceTable(id='p1'))

        from io import BytesIO
        binary_stream = BytesIO()
        xmcda.write(binary_stream,
                    xml_declaration=False, pretty_print=False,
                    tags='alternatives')
        self.assertEqual(compact_xml(self.xml_1),
                         binary_stream.getvalue().decode('utf-8'))
        binary_stream.close()

    xml_prg_exec_result = '''
<xmcda:XMCDA xmlns:xmcda="http://www.decision-deck.org/2019/XMCDA-3.1.1">
    <programExecutionResult id="per01" name="per01n" mcdaConcept="per01m">
        <description><comment>per01 comment</comment></description>
        <status>warning</status>
        <messages>
                <message name="executionStatus" level="info">
                    <text>OK</text>
                </message>
        </messages>
    </programExecutionResult>
</xmcda:XMCDA>
'''

    @staticmethod
    def build_xmcda_for_xml_prg_exec_result():
        '''Builds a object corresponding to self.xml_prg_exec_result'''
        from xmcda.program_execution_result import (
            ProgramExecutionResult,
            Status,
        )

        xmcda = XMCDA()
        per = ProgramExecutionResult()
        xmcda.program_execution_results.append(per)
        per.id = 'per01'
        per.name = 'per01n'
        per.mcda_concept = 'per01m'

        per.update_status(Status.WARNING)
        per.add_info('OK')
        per.messages[0].name = 'executionStatus'

        d = Description(comment="per01 comment")
        per.description = d

        return xmcda

    def test_write_prg_exec_results(self):
        self.maxDiff = None
        xmcda = TestWriteXMCDA.build_xmcda_for_xml_prg_exec_result()

        from io import BytesIO
        binary_stream = BytesIO()
        xmcda.write(binary_stream,
                    xml_declaration=False, pretty_print=False)
        self.assertEqual(compact_xml(self.xml_prg_exec_result),
                         binary_stream.getvalue().decode('utf-8'))

    xml_alternatives_assignments = '''
<xmcda:XMCDA xmlns:xmcda="http://www.decision-deck.org/2019/XMCDA-3.1.1">
    <alternativesAssignments id="asAs1" name="asAs1_n" mcdaConcept="asAs1_m">
        <alternativeAssignment id="aA1" name="aA1n" mcdaConcept="aA1m">
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
</xmcda:XMCDA>
'''

    def test_write_alternatives_assignments(self):

        self.maxDiff = None
        from .utils import compact_xml
        xml_source = TestWriteXMCDA.xml_alternatives_assignments
        xmcda = XMCDA().fromstring(xml_source)

        from io import BytesIO
        binary_stream = BytesIO()
        xmcda.write(binary_stream,
                    xml_declaration=False, pretty_print=False,
                    tags=('alternativesAssignments',))
        self.assertEqual(compact_xml(xml_source),
                         binary_stream.getvalue().decode('utf-8'))
