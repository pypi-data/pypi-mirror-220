import xmcda

from . import mark_creation, mixins, utils
from .alternatives import Alternative, Alternatives
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class AlternativesSets(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('alternativesSets', 'alternatives_sets', cls,
                             AlternativesSet)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for alternatives_set_xml in xfindall(element, './alternativesSet'):
            _id = CommonAttributes.get_id(alternatives_set_xml)
            alternative = self[_id]
            alternative.merge_xml(alternatives_set_xml, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for alternatives_set in self:
            args.append(alternatives_set.to_xml())
        alternatives = E.alternativesSets(*args, **d)
        return alternatives


@mark_creation
class AlternativesSet(mixins.Set, CommonAttributes, HasDescription):
    ''
    _element_klass = Alternative

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        alternative = (
            xmcda.alternatives if xmcda is not None
            else Alternatives())

        for element_xml in xfindall(element, './element'):
            # alternative -> values
            element = alternative[xfindtext(element_xml, 'alternativeID')]
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
            elt.append(EM.alternativeID(element.id))
            if values is not None:
                elt.append(values.to_xml())
            args.append(elt)
        return EM.alternativesSet(*args, **d)
