import xmcda

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .criteria import Criteria
from .mixins import CommonAttributes, HasDescription
from .thresholds import Thresholds
from .utils import xfind, xfindall, xfindtext


class CriterionThresholds(CommonAttributes, HasDescription):

    criterion = None
    thresholds = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        criteria = xmcda.criteria if xmcda is not None else Criteria()
        criterionID = xfindtext(element, 'criterionID')
        if criterionID is not None:
            self.criterion = criteria[criterionID]
        self.thresholds = Thresholds(xfind(element, './thresholds'))

    def to_xml(self):
        E = utils.element_maker()

        _attrs = utils.CommonAttributes_as_dict(self)

        if xmcda_version().major == 3:
            criterion_thresholds_xml = E.criterionThreshold(_attrs)
        elif xmcda_version().major == 4:
            criterion_thresholds_xml = E.criterionThresholds(_attrs)
        else:
            raise NotSupportedVersionError(xmcda_version().major)

        if self.description is not None:
            criterion_thresholds_xml.append(self.description.to_xml())
        if self.criterion is not None:
            criterion_thresholds_xml.append(E.criterionID(self.criterion.id))
        if self.thresholds is not None:
            criterion_thresholds_xml.append(self.thresholds.to_xml())
        else:
            criterion_thresholds_xml.append(Thresholds().to_xml())
        return criterion_thresholds_xml


class CriteriaThresholds(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaThresholds', 'criteria_thresholds_list',
                             cls, CriterionThresholds)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './criterionThreshold')
        elif xmcda_version().major == 4:
            children = xfindall(element, './criterionThresholds')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for criterionThresholds in children:
            self.append(CriterionThresholds(criterionThresholds, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        cSs_xml = E.criteriaThresholds(utils.CommonAttributes_as_dict(self))
        if self.description is not None:
            cSs_xml.append(self.description.to_xml())
        for criterionThresholds in self:
            cSs_xml.append(criterionThresholds.to_xml())
        return cSs_xml
