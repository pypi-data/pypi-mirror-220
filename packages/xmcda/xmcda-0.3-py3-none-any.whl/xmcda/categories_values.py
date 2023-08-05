from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .categories import Categories, Category
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CategoryValues(CommonAttributes, HasDescription):

    category = values = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def is_numeric(self):
        return self.values.is_numeric()

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        categories = \
            xmcda.categories if xmcda is not None else Categories()

        categoryID = xfindtext(element, './categoryID')
        if categoryID is not None:
            self.category = categories[categoryID]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            category_values = E.categoryValue(**attributes)
        elif xmcda_version().major == 4:
            category_values = E.categoryValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            category_values.append(self.description.to_xml())
        if self.category is not None:
            category_values.append(E.categoryID(self.category.id))
        if self.values is not None and len(self.values) > 0:
            category_values.append(self.values.to_xml())
        return category_values


class CategoriesValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('categoriesValues', 'categories_values_list', cls,
                       CategoryValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def categories(self):
        return [category_values.category for category_values in self]

    def is_numeric(self):
        return all(map(CategoryValues.is_numeric, self))

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            for category_value in xfindall(element, './categoryValue'):
                self.append(CategoryValues(category_value, xmcda))
        elif xmcda_version().major == 4:
            for category_values in xfindall(element, './categoryValues'):
                self.append(CategoryValues(category_values, xmcda))
        else:
            raise NotSupportedVersionError(xmcda_version().major)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        categories_values = E.categoriesValues(**attributes)
        if self.description is not None:
            categories_values.append(self.description.to_xml())
        for category_values in self:
            categories_values.append(category_values.to_xml())
        return categories_values

    def __getitem__(self, index):
        '''
        Returns the CategoryValues corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a Category: the category value for this category is returned

        - a string: the category value for the category with this id is
        returned
        '''
        type_error = 'CategoriesValues indices must be integers, Category or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, Category):
            for categoryValue in self:
                if categoryValue.category == index:
                    return categoryValue
            raise IndexError('No such categoryValue')

        if isinstance(index, str):
            for categoryValue in self:
                if categoryValue.category.id == index:
                    return categoryValue
            raise IndexError('No such categoryValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'CategoriesValue indices must be integers, Category or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, Category):
            for idx, categoryValue in enumerate(self):
                if categoryValue.category == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such categoryValue')

        if isinstance(index, str):
            for idx, categoryValue in enumerate(self):
                if categoryValue.category.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such categoryValue')
        raise TypeError(type_error % type(index))
