from enum import Enum

from . import utils
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall


class Threshold(CommonAttributes):

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)

    @staticmethod
    def build(xml_element):
        if xfind(xml_element, './constant') is not None:
            return ConstantThreshold(xml_element)
        if xfind(xml_element, './affine') is not None:
            return AffineThreshold(xml_element)
        raise ValueError('Invalid element: affine or constant is required')


class ConstantThreshold(Threshold):

    value = None

    def __init__(self, xml_element=None, **kw):
        super().__init__(xml_element, **kw)

    def merge_xml(self, element):
        super().merge_xml(element)
        from .value import Value
        self.value = Value(xfind(element, 'constant'))

    def to_xml(self):
        E = utils.element_maker()
        element = E.threshold(utils.CommonAttributes_as_dict(self))
        element.append(self.value.to_xml(tag='constant'))
        return element


class Type(Enum):
    DIRECT = 1
    INVERSE = 2

    @staticmethod
    def get(prefDir_str):
        if prefDir_str is None:
            raise KeyError(None)
        return Type[prefDir_str.upper()]


class AffineThreshold(Threshold):
    type = Type.DIRECT
    slope = intercept = 0

    def __init__(self, xml_element=None, **kw):
        super().__init__(xml_element, **kw)

    def merge_xml(self, element):
        super().merge_xml(element)
        from .value import Value

        element = xfind(element, 'affine')

        _type = xfind(element, 'type')
        if _type is not None:
            self.type = Type.get(_type.text)
        self.slope = Value(xfind(element, 'slope'))
        self.intercept = Value(xfind(element, 'intercept'))

    def to_xml(self):
        E = utils.element_maker()
        element = E.threshold(utils.CommonAttributes_as_dict(self))
        element.append(E.affine(E.type(self.type.name.lower()),
                                self.slope.to_xml('slope'),
                                self.intercept.to_xml('intercept')))
        return element


class Thresholds(list, HasDescription):

    def __init__(self, xml_element=None):
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        HasDescription.merge_xml(self, element)

        for scale in xfindall(element, './threshold'):
            self.append(Threshold.build(scale))

    def to_xml(self):
        E = utils.element_maker()
        thresholds = E.thresholds()
        if self.description is not None:
            thresholds.append(self.description.to_xml())
        for threshold in self:
            thresholds.append(threshold.to_xml())
        return thresholds
