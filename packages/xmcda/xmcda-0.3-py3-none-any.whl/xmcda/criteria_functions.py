import xmcda

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .criteria import Criteria
from .functions import Functions
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext


class CriterionFunctions(CommonAttributes, HasDescription):

    criterion = None
    functions = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        criteria = xmcda.criteria if xmcda is not None else Criteria()
        self.criterion = criteria[xfindtext(element, 'criterionID')]
        self.functions = Functions(xfind(element, './functions'))

    def to_xml(self):
        E = utils.element_maker()

        attrs = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            criterionFunctions_xml = E.criterionFunction(attrs)
        elif xmcda_version().major == 4:
            criterionFunctions_xml = E.criterionFunctions(attrs)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            criterionFunctions_xml.append(self.description.to_xml())
        if self.criterion is not None:
            criterionFunctions_xml.append(E.criterionID(self.criterion.id))
        if self.functions is not None:
            criterionFunctions_xml.append(self.functions.to_xml())
        return criterionFunctions_xml


class CriteriaFunctions(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaFunctions', 'criteria_functions_list',
                             cls, CriterionFunctions)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './criterionFunction')
        elif xmcda_version().major == 4:
            children = xfindall(element, './criterionFunctions')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for criterionFunctions in children:
            self.append(CriterionFunctions(criterionFunctions, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        cSs_xml = E.criteriaFunctions(utils.CommonAttributes_as_dict(self))
        if self.description is not None:
            cSs_xml.append(self.description.to_xml())
        for criterionFunction in self:
            cSs_xml.append(criterionFunction.to_xml())
        return cSs_xml
