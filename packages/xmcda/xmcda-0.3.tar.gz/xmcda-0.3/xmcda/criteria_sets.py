import xmcda

from . import mark_creation, mixins, utils
from .container import Container
from .criteria import Criteria, Criterion
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CriteriaSets(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaSets', 'criteria_sets', cls,
                             CriteriaSet)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for criteria_set_xml in xfindall(element, './criteriaSet'):
            _id = CommonAttributes.get_id(criteria_set_xml)
            criterion = self[_id]
            criterion.merge_xml(criteria_set_xml, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for criteria_set in self:
            args.append(criteria_set.to_xml())
        criteria = E.criteriaSets(*args, **d)
        return criteria


@mark_creation
class CriteriaSet(mixins.Set, CommonAttributes, HasDescription):
    ''
    _element_klass = Criterion

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        criterion = (
            xmcda.criteria if xmcda is not None
            else Criteria())

        for element_xml in xfindall(element, './element'):
            # criterion -> values
            element = criterion[xfindtext(element_xml, 'criterionID')]
            v_xml = xfind(element_xml, './values')
            v = Values(v_xml) if v_xml is not None else None
            self[element] = v

    def to_xml(self):
        EM = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for element, values in self.items():
            elt = EM.element()
            elt.append(EM.criterionID(element.id))
            if values is not None and len(values) > 0:
                # <values> can be omitted, but it cannot be empty
                elt.append(values.to_xml())
            args.append(elt)
        return EM.criteriaSet(*args, **d)
