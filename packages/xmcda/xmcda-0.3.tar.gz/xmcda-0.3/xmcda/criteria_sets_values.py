from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .criteria_sets import CriteriaSet, CriteriaSets
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CriteriaSetValues(CommonAttributes, HasDescription):

    criteria_set = values = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        criteria_sets = (
            xmcda.criteria_sets if xmcda is not None
            else CriteriaSets())

        criteria_set_id = xfindtext(element, './criteriaSetID')
        if criteria_set_id is not None:
            self.criteria_set = criteria_sets[criteria_set_id]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            criteria_set_value = E.criteriaSetValue(**attributes)
        elif xmcda_version().major == 4:
            criteria_set_value = E.criteriaSetValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            criteria_set_value.append(self.description.to_xml())
        if self.criteria_set is not None:
            xcriteriaSetID = E.criteriaSetID(self.criteria_set.id)
            criteria_set_value.append(xcriteriaSetID)
        if self.values is not None and len(self.values) > 0:
            criteria_set_value.append(self.values.to_xml())
        return criteria_set_value


class CriteriaSetsValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('criteriaSetsValues',
                       'criteria_sets_values_list',
                       cls, CriteriaSetValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './criteriaSetValue')
        elif xmcda_version().major == 4:
            children = xfindall(element, './criteriaSetValues')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for criteria_set_v in children:
            self.append(CriteriaSetValues(criteria_set_v, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        criteria_sets_values = E.criteriaSetsValues(**attributes)
        if self.description is not None:
            criteria_sets_values.append(self.description.to_xml())
        for criteria_set_value in self:
            criteria_sets_values.append(criteria_set_value.to_xml())
        return criteria_sets_values

    def __getitem__(self, index):
        '''
        Returns the CriteriaSetValue corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a CriteriaSet: the criteriaSet value for this
          criteriaSet is returned

        - a string: the criteriaSet value for the criteriaSet
          with this id is returned
        '''
        type_error = 'CriteriaSetsValue indices must be integers, CriteriaSet or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, CriteriaSet):
            for criteria_set_value in self:
                if criteria_set_value.criteria_set == index:
                    return criteria_set_value
            raise IndexError('No such criteriaSetValue')

        if isinstance(index, str):
            for criteria_set_value in self:
                if criteria_set_value.criteria_set.id == index:
                    return criteria_set_value
            raise IndexError('No such criteriaSetValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'CriteriaSetsValue indices must be integers, CriteriaSet or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, CriteriaSet):
            for idx, criteria_set_value in enumerate(self):
                if criteria_set_value.criteria_set == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such criteriaSetValue')

        if isinstance(index, str):
            for idx, criteria_set_value in enumerate(self):
                if criteria_set_value.criteria_set.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such criteriaSetValue')
        raise TypeError(type_error % type(index))
