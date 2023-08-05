from enum import Enum
from functools import total_ordering

import xmcda

from . import utils
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall


@total_ordering
class Status(Enum):
    OK = 0
    WARNING = 1
    ERROR = 2
    TERMINATED = 3

    def exit_status(self):
        if self in (Status.OK, Status.WARNING):
            return 0
        elif self == Status.ERROR:
            return 1
        elif self == Status.TERMINATED:
            return 2
        raise NotImplementedError("Forgot to handle an anum value")

    @staticmethod
    def get(status_str):
        if status_str is None:
            raise KeyError(None)
        return Status[status_str.upper()]

    @staticmethod
    def for_message_level(msg_level):
        if msg_level in (MessageLevel.DEBUG, MessageLevel.INFO):
            return Status.OK
        if msg_level == MessageLevel.WARNING:
            return Status.WARNING
        elif msg_level == MessageLevel.ERROR:
            return Status.ERROR
        raise ValueError("Invalid parameter")

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value


class MessageLevel(Enum):
    DEBUG = -1
    INFO = 0
    WARNING = 1
    ERROR = 2

    @staticmethod
    def get(level_str):
        if level_str is None:
            raise KeyError(None)
        return MessageLevel[level_str.upper()]


class Message(CommonAttributes, HasDescription):

    level = MessageLevel.INFO
    text = ""

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        level = element.get('level')
        if level is not None:
            self.level = MessageLevel.get(level)

        self.text = xfind(element, './text').text

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        d['level'] = self.level.name.lower()
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        args.append(E.text(self.text))
        message = E.message(*args, **d)
        return message

    def __str__(self):
        _str = f'{self.level.name}'
        if self.text not in (None, ''):
            _str += f': {self.text}'
        return _str

    @staticmethod
    def debug(message):
        return Message(level=MessageLevel.DEBUG, text=message)

    @staticmethod
    def info(message):
        return Message(level=MessageLevel.INFO, text=message)

    @staticmethod
    def warning(message):
        return Message(level=MessageLevel.WARNING, text=message)

    @staticmethod
    def error(message):
        return Message(level=MessageLevel.ERROR, text=message)


class ProgramExecutionResult(CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        # contained_class should not be set here, simply to prevent using it:
        # it is useles in this context
        return xmcda.TagInfo('programExecutionResult',
                             'program_execution_results', cls,
                             contained_class=None)

    status = Status.OK

    messages = ()

    def __init__(self, xml_element=None, xmcda=None, **kw):
        "Build a new result.  The argument 'xmcda' is ignored"
        # Parameter xmcda is supplied by XMCDA.merge_xml
        # but we do not need it here (same for ProgramParameters)

        self.messages = []

        if xml_element is not None:
            self.merge_xml(xml_element)

        for k, v in kw.items():
            setattr(self, k, v)

    def add_debug(self, message):
        self.add_message(Message.debug(message))
        return self

    def add_info(self, message):
        self.add_message(Message.info(message))
        return self

    def add_warning(self, message):
        self.add_message(Message.warning(message))
        return self

    def add_error(self, message):
        self.add_message(Message.error(message))
        return self

    def add_message(self, message):
        self.update_status(Status.for_message_level(message.level))
        self.messages.append(message)
        return self

    def update_status(self, status):
        if status > self.status:
            self.status = status
        return self.status

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        status = xfind(element, './status')
        if status is not None:
            self.status = Status.get(status.text)

        messages = xfind(element, './messages')
        if messages is not None:
            for message in xfindall(messages, './message'):
                self.add_message(Message(message))

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        # status is not mandatory, however omitting it discouraged so
        # we do not want to omit it when serializing the result
        args.append(E.status(self.status.name.lower()))
        messages = []
        if len(self.messages) != 0:
            messages = [E.messages(*(msg.to_xml() for msg in self.messages))]
        args.extend(messages)
        return E.programExecutionResult(*args, **d)
