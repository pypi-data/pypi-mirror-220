from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .alternatives_sets import AlternativesSet, AlternativesSets
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class AlternativesSetValues(CommonAttributes, HasDescription):

    alternatives_set = values = None

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        alternatives_sets = (
            xmcda.alternatives_sets if xmcda is not None
            else AlternativesSets())

        alternatives_set_id = xfindtext(element, './alternativesSetID')
        if alternatives_set_id is not None:
            self.alternatives_set = alternatives_sets[alternatives_set_id]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            alternatives_set_value = E.alternativesSetValue(**attributes)
        elif xmcda_version().major == 4:
            alternatives_set_value = E.alternativesSetValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            alternatives_set_value.append(self.description.to_xml())
        if self.alternatives_set is not None:
            xalternativesSetID = E.alternativesSetID(self.alternatives_set.id)
            alternatives_set_value.append(xalternativesSetID)
        if self.values is not None and len(self.values) > 0:
            alternatives_set_value.append(self.values.to_xml())
        return alternatives_set_value


class AlternativesSetsValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('alternativesSetsValues',
                       'alternatives_sets_values_list',
                       cls, AlternativesSetValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            children = xfindall(element, './alternativesSetValue')
        elif xmcda_version().major == 4:
            children = xfindall(element, './alternativesSetValues')
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        for alternatives_set_v in children:
            self.append(AlternativesSetValues(alternatives_set_v, xmcda))

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        alternatives_sets_values = E.alternativesSetsValues(**attributes)
        if self.description is not None:
            alternatives_sets_values.append(self.description.to_xml())
        for alternatives_set_value in self:
            alternatives_sets_values.append(alternatives_set_value.to_xml())
        return alternatives_sets_values

    def __getitem__(self, index):
        '''
        Returns the AlternativesSetValue corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a AlternativesSet: the alternativesSet value for this
          alternativesSet is returned

        - a string: the alternativesSet value for the alternativesSet
          with this id is returned
        '''
        type_error = 'AlternativesSetsValue indices must be integers, AlternativesSet or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, AlternativesSet):
            for alternatives_set_value in self:
                if alternatives_set_value.alternatives_set == index:
                    return alternatives_set_value
            raise IndexError('No such alternativesSetValue')

        if isinstance(index, str):
            for alternatives_set_value in self:
                if alternatives_set_value.alternatives_set.id == index:
                    return alternatives_set_value
            raise IndexError('No such alternativesSetValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'AlternativesSetsValue indices must be integers, AlternativesSet or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, AlternativesSet):
            for idx, alternatives_set_value in enumerate(self):
                if alternatives_set_value.alternatives_set == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such alternativesSetValue')

        if isinstance(index, str):
            for idx, alternatives_set_value in enumerate(self):
                if alternatives_set_value.alternatives_set.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such alternativesSetValue')
        raise TypeError(type_error % type(index))
