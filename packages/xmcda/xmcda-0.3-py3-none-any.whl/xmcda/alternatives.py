import xmcda

from . import mark_creation, utils
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfindall, xfindtext


class Alternatives(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('alternatives', 'alternatives', cls, Alternative)

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for alternative_xml in xfindall(element, 'alternative'):
            _id = CommonAttributes.get_id(alternative_xml)
            alternative = self[_id]
            alternative.merge_xml(alternative_xml)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for alternative in self:
            args.append(alternative.to_xml())
        alternatives = E.alternatives(*args, **d)
        return alternatives


@mark_creation
class Alternative(CommonAttributes, HasDescription):
    """
    id, name, mcda_concept
    description
    type
    active
    """
    _is_real = True
    _active = True

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def is_real(self):
        return self._is_real

    @is_real.setter
    def is_real(self, is_real):
        self._is_real = True if is_real is None else bool(is_real)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = True if active is None else bool(active)

    def __str__(self):
        s = "Alternative("
        s += f"id='{self.id}', " if self.id is not None else ''
        s += f"name='{self.name}', " if self.name is not None else ''
        s += (
            f"mcda_concept='{self.mcda_concept}', "
            if self.mcda_concept is not None
            else ''
        )
        if s[-1] == ' ':
            s = s[:-2]
        s += ')'
        return s

    def __repr__(self):
        # add id(self) to distinguish two instances having the same attributes
        return f'<{str(self)} at {hex(id(self))}>'

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        is_real = xfindtext(element, 'type')
        if is_real is not None:
            self.is_real = (is_real == 'real')

        active = xfindtext(element, 'active')
        if active is not None:
            self.active = utils.xml_boolean(active)

        return self

    def to_xml(self):
        include_defaults = xmcda.export_defaults()
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        if include_defaults or not self.is_real:
            args.append(E.type('real' if self.is_real else 'fictive'))
        if include_defaults or not self.active:
            args.append(E.active('true' if self.active else 'false'))
        alternative = utils.element_maker().alternative(*args, **d)
        return alternative


'''
with open('performanceTable.xml', 'rb') as xml_file:
    parser=etree.XMLParser()
    # #root=etree.parse(xml_file, parser=parser)
    # for event, element in etree.iterparse(xml_file):
    #     print("%s, %4s, %s" % (event, element.tag, element.text))
    root=etree.parse(xml_file, parser=parser).getroot()
    alts,crits,perfTable=root.getchildren()
    a0=alts[0]
    a=Alternative()
    a.from_xml(a0)
'''
