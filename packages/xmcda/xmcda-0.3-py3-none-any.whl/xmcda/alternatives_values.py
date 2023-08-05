from xmcda import TagInfo

from . import NotSupportedVersionError, utils
from . import version as xmcda_version
from .alternatives import Alternative, Alternatives
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Values


class AlternativeValues(CommonAttributes, HasDescription):

    alternative = values = None

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

        alternatives = \
            xmcda.alternatives if xmcda is not None else Alternatives()

        alternativeID = xfindtext(element, './alternativeID')
        if alternativeID is not None:
            self.alternative = alternatives[alternativeID]

        values = xfind(element, './values')
        if values is not None:
            self.values = Values(values)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        if xmcda_version().major == 3:
            alternative_values = E.alternativeValue(**attributes)
        elif xmcda_version().major == 4:
            alternative_values = E.alternativeValues(**attributes)
        else:
            raise NotSupportedVersionError(xmcda_version().major)
        if self.description is not None:
            alternative_values.append(self.description.to_xml())
        if self.alternative is not None:
            alternative_values.append(E.alternativeID(self.alternative.id))
        if self.values is not None and len(self.values) > 0:
            alternative_values.append(self.values.to_xml())
        return alternative_values


class AlternativesValues(list, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('alternativesValues', 'alternatives_values_list', cls,
                       AlternativeValues)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def alternatives(self):
        return [alternative_values.alternative for alternative_values in self]

    def is_numeric(self):
        return all(map(AlternativeValues.is_numeric, self))

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        if xmcda_version().major == 3:
            for alternative_value in xfindall(element, './alternativeValue'):
                self.append(AlternativeValues(alternative_value, xmcda))
        elif xmcda_version().major == 4:
            for alternative_values in xfindall(element, './alternativeValues'):
                self.append(AlternativeValues(alternative_values, xmcda))
        else:
            raise NotSupportedVersionError(xmcda_version().major)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        alternatives_values = E.alternativesValues(**attributes)
        if self.description is not None:
            alternatives_values.append(self.description.to_xml())
        for alternative_values in self:
            alternatives_values.append(alternative_values.to_xml())
        return alternatives_values

    def __getitem__(self, index):
        '''
        Returns the AlternativeValues corresponding to the index.
        Parameter index can be:
        - an integer: the index of the element to get from the list,
        - a Alternative: the alternative value for this alternative is returned

        - a string: the alternative value for the alternative with this id is
        returned
        '''
        type_error = 'AlternativesValues indices must be integers, Alternative or string, not %s'  # noqa

        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__getitem__(index)

        if isinstance(index, Alternative):
            for alternativeValue in self:
                if alternativeValue.alternative == index:
                    return alternativeValue
            raise IndexError('No such alternativeValue')

        if isinstance(index, str):
            for alternativeValue in self:
                if alternativeValue.alternative.id == index:
                    return alternativeValue
            raise IndexError('No such alternativeValue')

        raise TypeError(type_error % type(index))

    def __setitem__(self, index, value):
        type_error = 'AlternativesValue indices must be integers, Alternative or string, not %s'  # noqa
        if index is None:
            raise TypeError(type_error % 'NoneType')

        if isinstance(index, int):
            return super().__setitem__(index, value)

        if isinstance(index, Alternative):
            for idx, alternativeValue in enumerate(self):
                if alternativeValue.alternative == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such alternativeValue')

        if isinstance(index, str):
            for idx, alternativeValue in enumerate(self):
                if alternativeValue.alternative.id == index:
                    return super().__setitem__(idx, value)
            raise IndexError('No such alternativeValue')
        raise TypeError(type_error % type(index))
