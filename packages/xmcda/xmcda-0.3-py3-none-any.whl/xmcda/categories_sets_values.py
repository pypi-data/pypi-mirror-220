from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .categories_sets import CategoriesSet, CategoriesSets
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CategoriesSetValues(CommonAttributes, HasDescription):

    categories_set = values = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        categories_sets = (
            xmcda.categories_sets if xmcda is not None
            else CategoriesSets())

        categories_set_id = xfindtext(element, './categoriesSetID')
        if categories_set_id is not None:
            self.categories_set = categories_sets[categories_set_id]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            categories_set_value = E.categoriesSetValue(**attributes)
        elif xmcda_version().major == 4:
            categories_set_value = E.categoriesSetValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            categories_set_value.append(self.description.to_xml())
        if self.categories_set is not None:
            xcategoriesSetID = E.categoriesSetID(self.categories_set.id)
            categories_set_value.append(xcategoriesSetID)
        if self.values is not None and len(self.values) > 0:
            categories_set_value.append(self.values.to_xml())
        return categories_set_value


class CategoriesSetsValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('categoriesSetsValues',
                       'categories_sets_values_list',
                       cls, CategoriesSetValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './categoriesSetValue')
        elif xmcda_version().major == 4:
            children = xfindall(element, './categoriesSetValues')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for categories_set_v in children:
            self.append(CategoriesSetValues(categories_set_v, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        categories_sets_values = E.categoriesSetsValues(**attributes)
        if self.description is not None:
            categories_sets_values.append(self.description.to_xml())
        for categories_set_value in self:
            categories_sets_values.append(categories_set_value.to_xml())
        return categories_sets_values

    def __getitem__(self, index):
        '''
        Returns the CategoriesSetValue corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a CategoriesSet: the categoriesSet value for this
          categoriesSet is returned

        - a string: the categoriesSet value for the categoriesSet
          with this id is returned
        '''
        type_error = 'CategoriesSetsValue indices must be integers, CategoriesSet or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, CategoriesSet):
            for categories_set_value in self:
                if categories_set_value.categories_set == index:
                    return categories_set_value
            raise IndexError('No such categoriesSetValue')

        if isinstance(index, str):
            for categories_set_value in self:
                if categories_set_value.categories_set.id == index:
                    return categories_set_value
            raise IndexError('No such categoriesSetValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'CategoriesSetsValue indices must be integers, CategoriesSet or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, CategoriesSet):
            for idx, categories_set_value in enumerate(self):
                if categories_set_value.categories_set == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such categoriesSetValue')

        if isinstance(index, str):
            for idx, categories_set_value in enumerate(self):
                if categories_set_value.categories_set.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such categoriesSetValue')
        raise TypeError(type_error % type(index))
