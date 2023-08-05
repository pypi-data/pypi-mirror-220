import xmcda

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .criteria import Criteria
from .mixins import CommonAttributes, HasDescription
from .scales import ScaleReference, Scales, scales_jar
from .utils import xfind, xfindall, xfindtext


class CriterionScales(CommonAttributes, HasDescription):

    criterion = None
    scales = None

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
        self.scales = Scales(xfind(element, './scales'))

    def to_xml(self):
        E = utils.element_maker()

        _attrs = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            critScales_xml = E.criterionScale(_attrs)
        elif xmcda_version().major == 4:
            critScales_xml = E.criterionScales(_attrs)
        else:
            raise NotSupportedVersionError(xmcda_version().major)

        if self.description is not None:
            critScales_xml.append(self.description.to_xml())
        if self.criterion is not None:
            critScales_xml.append(E.criterionID(self.criterion.id))
        if self.scales is not None:
            critScales_xml.append(self.scales.to_xml(reset_known_scales=False))
        else:
            critScales_xml.append(Scales().to_xml(reset_known_scales=False))
        return critScales_xml


class CriteriaScales(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaScales', 'criteria_scales_list',
                             cls, CriterionScales)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def get_criterion_scales(
        self, an_id: str = None, *, criterion_id=None, criterion=None
    ) -> CriterionScales:
        """returns the CriterionScale having the requested id"""
        if an_id is not None:
            for criterion_scales in self:
                if criterion_scales.id == an_id:
                    return criterion_scales
        if criterion_id is not None:
            for criterion_scales in self:
                if (
                    criterion_scales.criterion is not None
                    and criterion_scales.criterion.id == criterion_id
                ):
                    return criterion_scales
        if criterion is not None:
            for criterion_scales in self:
                if criterion_scales.criterion == criterion:
                    return criterion_scales
        return None

    def resolve_scale_references(self) -> list:
        """Resolves the scale references within this criteria scales.
        Returns the list of unresolved scales' references.

        """
        scales_ids = {}
        for scale in self:
            scales_ids.setdefault(scale.id, scale)
        for criterion_scales in self:
            for scale in criterion_scales.scales:
                if not isinstance(scale, ScaleReference):
                    scales_ids.setdefault(scale.id, scale)
        if None in scales_ids:
            del scales_ids[None]
        unresolved = []
        for criterion_scales in self:
            for idx, scale in enumerate(criterion_scales.scales):
                if isinstance(scale, ScaleReference):
                    refd_scale = scales_ids.get(scale.ref_id)
                    if refd_scale is not None:
                        criterion_scales.scales[idx] = refd_scale
                    else:
                        unresolved.append(scale)
        return unresolved

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './criterionScale')
        elif xmcda_version().major == 4:
            children = xfindall(element, './criterionScales')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for criterionScales in children:
            self.append(CriterionScales(criterionScales, xmcda))
        self.resolve_scale_references()

    def to_xml(self):
        E = utils.element_maker()
        cSs_xml = E.criteriaScales(utils.CommonAttributes_as_dict(self))
        if self.description is not None:
            cSs_xml.append(self.description.to_xml())
        scales_jar().clear()
        for criterionScale in self:
            cSs_xml.append(criterionScale.to_xml())
        return cSs_xml
