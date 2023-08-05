import xmcda

from . import mark_creation, utils
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfindall, xfindtext


class Categories(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('categories', 'categories', cls, Category)

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for category_xml in xfindall(element, 'category'):
            _id = CommonAttributes.get_id(category_xml)
            c = self[_id]
            c.merge_xml(category_xml)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for category in self:
            args.append(category.to_xml())
        categories = E.categories(*args, **d)
        return categories


@mark_creation
class Category(CommonAttributes, HasDescription):
    ''

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
        s = "Category("
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

        return self

    def to_xml(self):
        include_defaults = xmcda.export_defaults()
        EM = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        if include_defaults or not self.active:
            args.append(EM.active('true' if self.active else 'false'))
        category = EM.category(*args, **d)
        return category
