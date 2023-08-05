import xmcda

from . import mark_creation, utils
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfindall, xfindtext


class Criteria(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteria', 'criteria', cls, Criterion)

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return next(filter(lambda x: x.id == key, self))
            except StopIteration as e:
                if not xmcda.create_on_access('criterion'):
                    raise IndexError from e
                criterion = Criterion(id=key)
                self.append(criterion)
                return criterion
        else:
            return super().__getitem__(key)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for criterion_xml in xfindall(element, 'criterion'):
            _id = CommonAttributes.get_id(criterion_xml)
            criterion = self[_id]
            criterion.merge_xml(criterion_xml)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for criterion in self:
            args.append(criterion.to_xml())
        criteria = E.criteria(*args, **d)
        return criteria


@mark_creation
class Criterion(CommonAttributes, HasDescription):
    """
    id, name, mcda_concept
    description
    active
    """
    _active = True

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = True if active is None else bool(active)

    def __str__(self):
        s = "Criterion("
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

        active = xfindtext(element, 'active')
        if active is not None:
            self.active = utils.xml_boolean(active)

    def to_xml(self):
        include_defaults = xmcda.export_defaults()
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        if include_defaults or not self.active:
            args.append(E.active('true' if self.active else 'false'))
        criterion = utils.element_maker().criterion(*args, **d)
        return criterion

    @staticmethod
    def build(element, xmcda=None):
        return Criterion(element)
