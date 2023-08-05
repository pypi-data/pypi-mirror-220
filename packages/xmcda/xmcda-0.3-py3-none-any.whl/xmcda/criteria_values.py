from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .criteria import Criteria, Criterion
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CriterionValues(CommonAttributes, HasDescription):

    criterion = values = None

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

        criteria = \
            xmcda.criteria if xmcda is not None else Criteria()

        criterionID = xfindtext(element, './criterionID')
        if criterionID is not None:
            self.criterion = criteria[criterionID]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            criterion_values = E.criterionValue(**attributes)
        elif xmcda_version().major == 4:
            criterion_values = E.criterionValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            criterion_values.append(self.description.to_xml())
        if self.criterion is not None:
            criterion_values.append(E.criterionID(self.criterion.id))
        if self.values is not None and len(self.values) > 0:
            criterion_values.append(self.values.to_xml())
        return criterion_values


class CriteriaValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('criteriaValues', 'criteria_values_list', cls,
                       CriterionValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def criteria(self):
        return [criterion_values.criterion for criterion_values in self]

    def is_numeric(self):
        return all(map(CriterionValues.is_numeric, self))

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            for criterion_value in xfindall(element, './criterionValue'):
                self.append(CriterionValues(criterion_value, xmcda))
        elif xmcda_version().major == 4:
            for criterion_values in xfindall(element, './criterionValues'):
                self.append(CriterionValues(criterion_values, xmcda))
        else:
            raise NotSupportedVersionError(xmcda_version().major)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        criteria_values = E.criteriaValues(**attributes)
        if self.description is not None:
            criteria_values.append(self.description.to_xml())
        for criterion_values in self:
            criteria_values.append(criterion_values.to_xml())
        return criteria_values

    def __getitem__(self, index):
        '''
        Returns the CriterionValues corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a Criterion: the criterion value for this criterion is returned

        - a string: the criterion value for the criterion with this id is
        returned
        '''
        type_error = 'CriteriaValues indices must be integers, Criterion or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, Criterion):
            for criterionValue in self:
                if criterionValue.criterion == index:
                    return criterionValue
            raise IndexError('No such criterionValue')

        if isinstance(index, str):
            for criterionValue in self:
                if criterionValue.criterion.id == index:
                    return criterionValue
            raise IndexError('No such criterionValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'CriteriaValue indices must be integers, Criterion or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, Criterion):
            for idx, criterionValue in enumerate(self):
                if criterionValue.criterion == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such criterionValue')

        if isinstance(index, str):
            for idx, criterionValue in enumerate(self):
                if criterionValue.criterion.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such criterionValue')
        raise TypeError(type_error % type(index))
