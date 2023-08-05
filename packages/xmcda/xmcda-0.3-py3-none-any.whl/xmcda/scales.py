import threading
from enum import Enum

from lxml.etree import QName

from . import utils
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext
from .value import Value, ValuedLabel

__local = threading.local()
__local.scales_jar = set()  # see scales_jar() for details


def scales_jar():
    """Returns a set local to a set to store scales.

    For example, this is used when serializing scales into XMCDA, so
    that the same scale is not written again and again, but only once
    with further occurences being serialized as references instead
    (<scaleID>).
    """
    return __local.scales_jar


class PreferenceDirection(Enum):
    UNSET = 0
    MIN = 1
    MAX = 2

    @staticmethod
    def get_from_xml(preference_direction: str) -> 'PreferenceDirection':
        """Return the requested PreferenceDirection enum.

        Specifically the method returns:

        - UNSET if the parameter is None

        - MIN (resp. MAX) if the parameter case-insensitively equals
          to "MIN" (resp. "MAX")

        In all other case, `KeyError` is raised (including strings
        'unset' or 'UNSET' which are invalid xml values for the
        preference direction).
        """
        pref_dir = preference_direction
        if pref_dir is None:
            return PreferenceDirection.UNSET
        if isinstance(pref_dir, str) and pref_dir.upper() == 'UNSET':
            raise KeyError(pref_dir)
        try:
            return PreferenceDirection[pref_dir.upper()]
        except Exception:
            import sys
            raise KeyError(pref_dir).with_traceback(sys.exc_info()[2])


class Scale(CommonAttributes):

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)

    @staticmethod
    def build(xml_element):
        if QName(xml_element).localname == "scaleID":
            return ScaleReference(xml_element.text)
        if xfind(xml_element, './nominal') is not None:
            return NominalScale(xml_element)
        if xfind(xml_element, './qualitative') is not None:
            return QualitativeScale(xml_element)
        if xfind(xml_element, './quantitative') is not None:
            return QuantitativeScale(xml_element)
        raise ValueError(
            "Invalid xml element, cannot build a scale when neither nominal, "
            "qualitative or quantitative is found"
        )


class ScaleReference(Scale):

    def __init__(self, ref_id: str):
        self.ref_id = ref_id

    def to_xml(self):
        E = utils.element_maker()
        return E.scaleID(self.ref_id)


class NominalScale(Scale):

    labels = ()

    def __init__(self, xml_element=None, **kw):
        self.labels = []
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        super().merge_xml(element)
        nominal_element = xfind(element, './nominal')
        if nominal_element is None:
            raise ValueError('Parameter element has no child <nominal/>')

        for label in xfindall(nominal_element, './labels/label'):
            self.labels.append(label.text)

    def to_xml(self):
        E = utils.element_maker()
        element = E.scale(utils.CommonAttributes_as_dict(self))
        nominal = E.nominal()
        labels = [E.label(label) for label in self.labels]
        labels = E.labels(*labels)
        nominal.append(labels)
        element.append(nominal)
        return element


class QualitativeScale(Scale):

    preference_direction = PreferenceDirection.UNSET
    valued_labels = ()

    def __init__(self, xml_element=None, **kw):
        self.valued_labels = []
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        super().merge_xml(element)
        qualitative_elt = xfind(element, './qualitative')
        if qualitative_elt is None:
            raise ValueError('Parameter element has no child <qualitative/>')

        _prefDir_xpath = './qualitative/preferenceDirection'
        self.preference_direction = \
            PreferenceDirection.get_from_xml(xfindtext(element, _prefDir_xpath))

        valued_labels = xfindall(qualitative_elt, './valuedLabels/valuedLabel')
        for valued_label in valued_labels:
            self.valued_labels.append(ValuedLabel(valued_label))

    def to_xml(self):
        E = utils.element_maker()
        element = E.scale(utils.CommonAttributes_as_dict(self))
        qualitative = E.qualitative()
        if (
            self.preference_direction is not None
            and self.preference_direction != PreferenceDirection.UNSET
        ):
            pref_dir = self.preference_direction.name.lower()
            qualitative.append(E.preferenceDirection(pref_dir))
        valued_labels = [vlabel.to_xml() for vlabel in self.valued_labels]
        if len(valued_labels) > 0:
            valued_labels = E.valuedLabels(*valued_labels)
            qualitative.append(valued_labels)
        element.append(qualitative)
        return element


class QuantitativeScale(Scale):

    preference_direction = PreferenceDirection.UNSET
    minimum = maximum = None

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        super().merge_xml(element)
        quantitative_element = xfind(element, './quantitative')
        if quantitative_element is None:
            raise ValueError('Parameter element has no child <quantitative/>')

        xpref = xfindtext(element, './quantitative/preferenceDirection')
        self.preference_direction = PreferenceDirection.get_from_xml(xpref)

        minimum = xfind(quantitative_element, './minimum')
        if minimum is not None:
            self.minimum = Value(minimum)
        maximum = xfind(quantitative_element, './maximum')
        if maximum is not None:
            self.maximum = Value(maximum)

    def to_xml(self):
        E = utils.element_maker()
        element = E.scale(utils.CommonAttributes_as_dict(self))
        quantitative = E.quantitative()
        if (
            self.preference_direction is not None
            and self.preference_direction != PreferenceDirection.UNSET
        ):
            pref_dir = self.preference_direction.name.lower()
            quantitative.append(E.preferenceDirection(pref_dir))
        if self.minimum is not None:
            quantitative.append(self.minimum.to_xml('minimum'))
        if self.maximum is not None:
            quantitative.append(self.maximum.to_xml('maximum'))
        element.append(quantitative)
        return element


class Scales(list, HasDescription):

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        HasDescription.merge_xml(self, element)

        for scale in element.xpath("*[name()='scale']|*[name()='scaleID']"):
            self.append(Scale.build(scale))

        # Handle referencing scales
        self.handle_scale_references()

    def handle_scale_references(self) -> list:
        scales_ids = {}
        for scale in self:
            scales_ids.setdefault(scale.id, scale)

        orphans = []
        for idx, scale in enumerate(self):
            if isinstance(scale, ScaleReference):
                refd_scale = scales_ids.get(scale.ref_id)
                if refd_scale is not None:
                    self[idx] = refd_scale
                else:
                    orphans.append(scale)
        return orphans

    def to_xml(self, *, reset_known_scales: bool = True):
        E = utils.element_maker()
        xscales = E.scales()
        if self.description is not None:
            xscales.append(self.description.to_xml())
        known_scales = scales_jar()
        for scale in self:
            if scale in known_scales:
                xscales.append(ScaleReference(scale.id).to_xml())
            else:
                xscales.append(scale.to_xml())
                known_scales.add(scale)
        return xscales
