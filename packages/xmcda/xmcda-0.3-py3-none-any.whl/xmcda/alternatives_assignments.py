import xmcda

from . import utils
from .alternatives import Alternatives
from .categories import Categories
from .categories_sets import CategoriesSets
from .container import Container
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CategoriesInterval(CommonAttributes, HasDescription):
    '''
    A categories interval, used in alternative assignments.
    A valid CategoryInterval has at least one not-None bound
    '''

    lower_bound = upper_bound = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda is not None:
            categories = xmcda.categories
        else:
            categories = Categories()

        _x = xfind(element, './lowerBound')
        if _x is not None:
            self.lower_bound = categories[xfindtext(_x, './categoryID')]

        _x = xfind(element, './upperBound')
        if _x is not None:
            self.upper_bound = categories[xfindtext(_x, './categoryID')]

    def to_xml(self):
        EM = utils.element_maker()
        _xml = EM.categoriesInterval()
        if self.lower_bound is not None:
            _xml.append(EM.lowerBound(EM.categoryID(self.lower_bound.id)))
        if self.upper_bound is not None:
            _xml.append(EM.upperBound(EM.categoryID(self.upper_bound.id)))
        return _xml


class AlternativeAssignment(CommonAttributes, HasDescription):

    alternative = None
    category = categories_set = categories_interval = None
    values = ()

    def __init__(self, xml_element=None, xmcda=None, **kw):
        self.values = []
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda is not None:
            alternatives = xmcda.alternatives
            categories = xmcda.categories
            categories_sets = xmcda.categories_sets
        else:
            alternatives = Alternatives()
            categories = Categories()
            categories_sets = CategoriesSets()

        _x = xfind(element, './alternativeID')
        if _x is not None:
            self.alternative = alternatives[_x.text]

        _x = xfind(element, './categoryID')
        if _x is not None:
            self.category = categories[_x.text]

        _x = xfind(element, './categoriesSetID')
        if _x is not None:
            self.categories_set = categories_sets[_x.text]

        _x = xfind(element, './categoriesInterval')
        if _x is not None:
            self.categories_interval = CategoriesInterval(_x, xmcda)

        _x = xfind(element, './values')
        if _x is not None:
            self.values = Values(_x)

    def to_xml(self):
        EM = utils.element_maker()
        xml = EM.alternativeAssignment(utils.CommonAttributes_as_dict(self))
        if self.description is not None:
            xml.append(self.description.to_xml())
        if self.alternative is not None:
            xml.append(EM.alternativeID(self.alternative.id))
        if self.category is not None:
            xml.append(EM.categoryID(self.category.id))
        if self.categories_set is not None:
            xml.append(EM.categoriesSetID(self.categories_set.id))
        if self.categories_interval is not None:
            xml.append(self.categories_interval.to_xml())

        if self.values is not None and len(self.values) > 0:
            xml.append(self.values.to_xml())

        return xml


class AlternativesAssignments(Container, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('alternativesAssignments',
                             'alternatives_assignments_list',
                             cls, AlternativeAssignment)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        for aA_xml in xfindall(element, 'alternativeAssignment'):
            aA = AlternativeAssignment(aA_xml, xmcda=xmcda)
            self.append(aA)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for alternative_assignment in self:
            args.append(alternative_assignment.to_xml())
        alternatives_assignments = E.alternativesAssignments(*args, **d)
        return alternatives_assignments
