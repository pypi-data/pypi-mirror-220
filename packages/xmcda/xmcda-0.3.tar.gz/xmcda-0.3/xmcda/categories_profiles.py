from enum import Enum

import xmcda

from . import utils
from .alternatives import Alternatives
from .categories import Categories
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class Profile:

    alternative = values = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        if xmcda is None:
            alternatives = Alternatives()
        else:
            alternatives = xmcda.alternatives

        alternative_id = xfindtext(element, './alternativeID')
        if alternative_id is not None:
            self.alternative = alternatives[alternative_id]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self, tag):
        E = utils.element_maker()
        profile = getattr(E, tag)()
        if self.alternative is not None:
            profile.append(E.alternativeID(self.alternative.id))

        if self.values is not None and len(self.values) > 0:
            profile.append(self.values.to_xml())

        return profile


class CategoryProfile(CommonAttributes, HasDescription):

    class Type(Enum):
        BOUNDING = 1
        CENTRAL = 2

        @classmethod
        def get(cls, type_as_str):
            if type_as_str is None:
                raise KeyError(None)
            try:
                return cls[type_as_str.upper()]
            except Exception as e:
                raise KeyError(e)

    category = None
    central_profile = lower_bound = upper_bound = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        categories = xmcda.categories if xmcda is not None else Categories()

        _c = xfind(element, 'categoryID')
        if _c is not None:
            self.category = categories[_c.text]

        _e = xfind(element, './bounding/lowerBound')
        if _e is not None:
            self.lower_bound = Profile(_e, xmcda)

        _e = xfind(element, './bounding/upperBound')
        if _e is not None:
            self.upper_bound = Profile(_e, xmcda)

        _e = xfind(element, './central')
        if _e is not None:
            self.central_profile = Profile(_e, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        category_profile = E.categoryProfile(**attributes)

        if self.description is not None:
            category_profile.append(self.description.to_xml())

        if self.category is not None:
            category_profile.append(E.categoryID(self.category.id))

        bounding = E.bounding()
        if self.lower_bound is not None:
            bounding.append(self.lower_bound.to_xml('lowerBound'))
        if self.upper_bound is not None:
            bounding.append(self.upper_bound.to_xml('upperBound'))

        if self.upper_bound is not None or self.lower_bound is not None:
            category_profile.append(bounding)

        if self.central_profile is not None:
            category_profile.append(self.central_profile.to_xml('central'))

        return category_profile


class CategoriesProfiles(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('categoriesProfiles',
                             'categories_profiles_list',
                             cls, CategoryProfile)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for cprofile in xfindall(element, './categoryProfile'):
            self.append(CategoryProfile(cprofile, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        profiles = E.categoriesProfiles(utils.CommonAttributes_as_dict(self))
        if self.description is not None:
            profiles.append(self.description.to_xml())
        for category_profile in self:
            profiles.append(category_profile.to_xml())
        return profiles
