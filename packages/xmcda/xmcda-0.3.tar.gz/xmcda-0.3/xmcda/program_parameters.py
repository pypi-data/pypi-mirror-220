import xmcda

from . import utils
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall


class ProgramParameters(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('programParameters', 'program_parameters_list',
                             cls, ProgramParameter)

    description = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        # parameter xmcda is ignored but it is present when XMCDA
        # instanciates a new ProgramParameters
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for parameter in xfindall(element, './programParameter'):
            self.append(ProgramParameter(parameter))

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for p in self:
            args.append(p.to_xml())
        prg_params = E.programParameters(*args, **d)
        return prg_params


class ProgramParameter(CommonAttributes, HasDescription):

    values = None

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        from xmcda.value import Values
        self.values = Values(xfind(element, './values'))

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        args.append(self.values.to_xml())
        prg_param = E.programParameter(*args, **d)
        return prg_param
