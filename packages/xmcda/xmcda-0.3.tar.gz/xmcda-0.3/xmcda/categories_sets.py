import xmcda

from . import mark_creation, mixins, utils
from .categories import Categories, Category
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CategoriesSets(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('categoriesSets', 'categories_sets', cls,
                             CategoriesSet)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for categories_set_xml in xfindall(element, './categoriesSet'):
            _id = CommonAttributes.get_id(categories_set_xml)
            category = self[_id]
            category.merge_xml(categories_set_xml, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for categories_set in self:
            args.append(categories_set.to_xml())
        categories = E.categoriesSets(*args, **d)
        return categories


@mark_creation
class CategoriesSet(mixins.Set, CommonAttributes, HasDescription):
    ''
    _element_klass = Category

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        category = (
            xmcda.categories if xmcda is not None
            else Categories())

        for element_xml in xfindall(element, './element'):
            # category -> values
            element = category[xfindtext(element_xml, 'categoryID')]
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
            elt.append(EM.categoryID(element.id))
            if values is not None:
                elt.append(values.to_xml())
            args.append(elt)
        return EM.categoriesSet(*args, **d)
