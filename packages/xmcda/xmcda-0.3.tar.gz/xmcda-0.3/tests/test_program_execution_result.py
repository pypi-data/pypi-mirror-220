import xmcda
from xmcda.program_execution_result import (
    Message,
    MessageLevel,
    ProgramExecutionResult,
    Status,
)

from .utils import XMCDATestCase


class TestStatus(XMCDATestCase):

    def test_exit_status(self):
        self.assertEqual(Status.OK.exit_status(), 0)
        self.assertEqual(Status.WARNING.exit_status(), 0)
        self.assertNotEqual(Status.OK, Status.WARNING)

        self.assertNotEqual(
            Status.OK.exit_status(), Status.ERROR.exit_status()
        )
        self.assertNotEqual(
            Status.OK.exit_status(), Status.TERMINATED.exit_status()
        )

        for status in Status:  # make sure none was forgotten
            status.exit_status()

    def test_get(self):
        self.assertRaises(KeyError, Status.get, None)
        self.assertRaises(KeyError, Status.get, '')
        self.assertEqual(Status.get('ok'), Status.OK)
        self.assertEqual(Status.get('warning'), Status.WARNING)
        self.assertEqual(Status.get('error'), Status.ERROR)
        self.assertEqual(Status.get('terminated'), Status.TERMINATED)

    def test_for_message_level(self):
        level_to_status = Status.for_message_level
        self.assertEqual(level_to_status(MessageLevel.DEBUG),   Status.OK)
        self.assertEqual(level_to_status(MessageLevel.INFO),    Status.OK)
        self.assertEqual(level_to_status(MessageLevel.WARNING), Status.WARNING)
        self.assertEqual(level_to_status(MessageLevel.ERROR),   Status.ERROR)
        with self.assertRaises(ValueError):
            level_to_status('moo')

    def test_compare(self):
        self.assertTrue(Status.OK < Status.WARNING)
        self.assertTrue(Status.OK < Status.ERROR)
        self.assertTrue(Status.OK < Status.TERMINATED)
        self.assertTrue(Status.ERROR > Status.WARNING)
        self.assertTrue(Status.OK <= Status.WARNING)

        self.assertFalse(Status.OK > Status.WARNING)
        self.assertFalse(Status.OK >= Status.WARNING)

        self.assertEqual(Status.TERMINATED, Status.TERMINATED)
        self.assertNotEqual(Status.OK, Status.WARNING)


class TestMessageLevel(XMCDATestCase):

    def test_get(self):
        self.assertRaises(KeyError, MessageLevel.get, None)
        self.assertRaises(KeyError, MessageLevel.get, '')


class TestMessage(XMCDATestCase):

    xml_1 = '''<message name="executionStatus" level="warning">
                   <description><comment>a comment</comment></description>
                   <text>OK</text>
               </message>'''

    xml_default = '''<message name="executionStatus">
                         <text>OK</text>
                     </message>'''

    def test_load_xml(self):
        msg = Message(self.read_xml(self.xml_1))
        self.assertEqual(msg.name, 'executionStatus')
        self.assertEqual(msg.level, MessageLevel.WARNING)
        self.assertEqual(msg.description.comment, "a comment")

    def test_default_level(self):
        message = Message(self.read_xml(self.xml_default))
        self.assertEqual(message.level, MessageLevel.INFO)

    def test_to_xml(self):
        self._test_to_xml(self.xml_1, Message)

    def test_str(self):
        msg = Message.debug("42")
        self.assertEqual(str(msg), "DEBUG: 42")
        msg = Message.info("")  # not very useful, agreed
        self.assertEqual(str(msg), "INFO")


class TestProgramExecutionResult(XMCDATestCase):

    xml_1 = '''
        <programExecutionResult id="per01" name="per01n" mcdaConcept="per01m">
            <description><comment>per01 comment</comment></description>
            <status>warning</status>
            <messages>
                    <message name="executionStatus" level="info">
                        <text>OK</text>
                    </message>
                    <message name="color_ignored" level="warning">
                        <text>Warning: the selected color was ignored</text>
                    </message>
                </messages>
        </programExecutionResult>
    '''

    xml_default = '<programExecutionResult id="per02"/>'
    serialized_xml_default = '''
        <programExecutionResult id="per02">
            <status>ok</status>
        </programExecutionResult>'''

    def test_init_with_kw(self):
        r = ProgramExecutionResult(id='result', attr=3)
        self.assertEqual(r.id, 'result')
        self.assertEqual(r.attr, 3)

    def test_load_xml(self):
        r = ProgramExecutionResult(self.read_xml(self.xml_1))
        self.assertEqual(r.id, 'per01')
        self.assertEqual(r.name, 'per01n')
        self.assertEqual(r.mcda_concept, 'per01m')
        self.assertEqual(r.description.comment, 'per01 comment')
        self.assertEqual(r.status, Status.WARNING)
        self.assertEqual(len(r.messages), 2)

        r = ProgramExecutionResult(self.read_xml(self.xml_default))
        self.assertEqual(r.status, Status.OK)

    def test_to_xml(self):
        self.maxDiff = None
        self._test_to_xml(self.xml_1, ProgramExecutionResult)
        self._test_to_xml(self.serialized_xml_default, ProgramExecutionResult)

        self.maxDiff = None
        from .utils import compact_xml
        source = compact_xml(self.serialized_xml_default)
        result = ProgramExecutionResult(self.read_xml(self.xml_default))
        result = xmcda.utils.tostring(result.to_xml())
        self.assertEqual(source, compact_xml(result))

    def test_init_defaults(self):
        r = ProgramExecutionResult()
        self.assertEqual(r.status, Status.OK)

    def test_update_status(self):
        r = ProgramExecutionResult()
        self.assertEqual(r.update_status(Status.OK), Status.OK)
        self.assertEqual(r.update_status(Status.ERROR), Status.ERROR)
        # now its status is Error, a warning does not change the status
        self.assertEqual(r.update_status(Status.WARNING), Status.ERROR)

    def test_add_message(self):
        r = ProgramExecutionResult()
        r.add_message(Message.debug("moo"))
        self.assertEqual(r.status, Status.OK)
        r.add_message(Message.info("tweet"))
        self.assertEqual(r.status, Status.OK)
        r.add_message(Message.warning("bah"))
        self.assertEqual(r.status, Status.WARNING)
        r.add_message(Message.error("miaow"))
        self.assertEqual(r.status, Status.ERROR)
        # there is no going back
        r.add_message(Message.info("woof"))
        self.assertEqual(r.status, Status.ERROR)

    def test_shortcuts(self):
        r = ProgramExecutionResult()
        r.add_debug("moo")
        self.assertEqual(r.status, Status.OK)
        r.add_info("tweet")
        self.assertEqual(r.status, Status.OK)
        r.add_warning("bah")
        self.assertEqual(r.status, Status.WARNING)
        r.add_error("miaow")
        self.assertEqual(r.status, Status.ERROR)
        # there is no going back
        r.add_info("woof")
        self.assertEqual(r.status, Status.ERROR)
