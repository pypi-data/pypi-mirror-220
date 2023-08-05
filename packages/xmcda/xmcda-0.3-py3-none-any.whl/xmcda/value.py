from lxml import etree

from . import utils
from .functions import PiecewiseLinearFunction
from .mixins import CommonAttributes
from .utils import xfind, xfindall

_marker = []


class Interval:
    lower_bound = upper_bound = None
    is_lower_closed = is_upper_closed = True

    def __init__(self, arg1=_marker, arg2=_marker):
        if arg2 is _marker:
            if arg1 is not _marker:
                self.merge_xml(arg1)
        else:
            self.lower_bound = arg1
            self.upper_bound = arg2

    def merge_xml(self, element):
        lower = xfind(element, 'lowerBound')
        if lower is not None:
            # the type 'intervalBound' is an extension of the type 'value'
            self.lower_bound = Value(lower)
            _open = lower.get('open')
            if _open is not None:
                self.is_lower_closed = not utils.xml_boolean(_open)
        upper = xfind(element, 'upperBound')
        if upper is not None:
            self.upper_bound = Value(upper)
            _open = upper.get('open')
            if _open is not None:
                self.is_upper_closed = not utils.xml_boolean(_open)

    def _bound_to_xml(self, bound, is_closed):
        if bound is None:
            return (), None

        import xmcda
        include_defaults = xmcda.export_defaults()
        d = {}
        if include_defaults:
            d['open'] = utils.boolean_to_xml(not is_closed)
        elif not is_closed:
            d['open'] = utils.boolean_to_xml(not is_closed)
        return [bound.to_xml().getchildren()[0]], d

    def __str__(self):
        s = '[' if self.is_lower_closed else ']'
        s += (str(self.lower_bound) if self.lower_bound is not None
              else '*')
        s += ', '
        s += (str(self.upper_bound) if self.upper_bound is not None
              else '*')
        s += ']' if self.is_upper_closed else '['
        return s

    def to_xml(self):
        E = utils.element_maker()

        args = []

        a, d = self._bound_to_xml(self.lower_bound, self.is_lower_closed)
        if d is not None:
            args.append(E.lowerBound(*a, **d))

        a, d = self._bound_to_xml(self.upper_bound, self.is_upper_closed)
        if d is not None:
            args.append(E.upperBound(*a, **d))

        interval = E.interval(*args)
        return interval


class Rational:
    numerator = denominator = 0

    def __init__(self, arg1=_marker, arg2=_marker):
        if arg2 is _marker:
            if arg1 is not _marker:
                self.merge_xml(arg1)
        else:
            self.numerator = arg1
            self.denominator = arg2

    def to_float(self):
        if self.denominator == 0:
            if self.numerator == 0:
                return float('nan')
            import math
            sign_n = math.copysign(1, self.numerator)
            # for the moment being the sign of the denominator has no
            # importance (it is always positive) since there exists no -0 in
            # integer values
            sign_d = math.copysign(1, self.denominator)
            return float('inf') * sign_n * sign_d
        return self.numerator / self.denominator

    def merge_xml(self, element):
        self.numerator = int(xfind(element, 'numerator').text)
        self.denominator = int(xfind(element, 'denominator').text)

    def __str__(self):
        return f'{self.numerator}/{self.denominator}'

    def to_xml(self):
        E = utils.element_maker()

        return E.rational(E.numerator(str(self.numerator)),
                          E.denominator(str(self.denominator)))


class ValuedLabel:
    label = value = 0

    def __init__(self, arg1=_marker, arg2=_marker):
        if arg2 is _marker:
            if arg1 is not _marker:
                self.merge_xml(arg1)
        else:
            self.label = arg1
            self.value = Value(arg2)

    def merge_xml(self, element, xmcda=None):
        self.label = xfind(element, 'label').text
        self.value = Value(xfind(element, 'value'))

    def __str__(self):
        return f'{self.label}:{self.value}'

    def to_xml(self):
        E = utils.element_maker()
        return E.valuedLabel(E.label(self.label),
                             self.value.to_xml())


class _NAType:
    '''The class for NA. It should not be used elsewhere than in this
    module: use the NA value instead
    '''
    # The singleton pattern is not enforced, it seems out of proportion
    def __str__(cls):
        return 'N/A'

    def to_xml(self):
        return utils.element_maker().NA()


NA = _NAType()
"The value representing <NA/>"


class FuzzyNumber(PiecewiseLinearFunction):
    def __init__(self, xml_element=None):
        super().__init__(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)

    def to_xml(self):
        E = utils.element_maker()
        kw = utils.CommonAttributes_as_dict(self)
        # we do not need the <function> root tag, only its child:
        # we /are/ a PiecewiseLinearFunction
        return E.fuzzyNumber(xfind(super().to_xml(), './piecewiseLinear'),
                             **kw)


value_types = (int, float, Interval, Rational, str, ValuedLabel,
               bool, _NAType, FuzzyNumber)

value_tags = {
    'integer':     lambda e: int(e.text),                # noqa:E272
    'real':        lambda e: float(e.text),              # noqa:E272
    'interval':    lambda e: Interval(e),                # noqa:E272
    'rational':    lambda e: Rational(e),                # noqa:E272
    'label':       lambda e: e.text if e.text is not None else '',  # noqa
    'valuedLabel': lambda e: ValuedLabel(e),
    'boolean':     lambda e: utils.xml_boolean(e.text),  # noqa:E272
    'NA':          lambda e=None: NA,                    # noqa:E272
    'fuzzyNumber': lambda e: FuzzyNumber(e),
}

__E = utils.element_maker()
value_to_xml = {
    int:         lambda v, E=__E:  E.integer(str(v)),          # noqa:E272
    float:       lambda v, E=__E:  E.real(str(v)),             # noqa:E272
    Interval:    lambda v:         v.to_xml(),                 # noqa:E272
    Rational:    lambda v:         v.to_xml(),                 # noqa:E272
    str:         lambda v, E=__E:  E.label(v),                 # noqa:E272
    ValuedLabel: lambda v:         v.to_xml(),
    bool:        lambda v, E=__E:  E.boolean(utils.boolean_to_xml(v)), # noqa:272
    NA:          lambda v:         v.to_xml(),                 # noqa:E272
    FuzzyNumber: lambda v:         v.to_xml(),                 # noqa:E272
}
del __E


def value_for_element(element):
    '''
    Builds the value (int, float, Interval, etc) for the supplied xml element
    Raises ValueError if the element's tag is not registered.
    '''
    # get the tag w/o its namespace
    # e.g. '{http://www.decision-deck.org/2019/XMCDA-3.1.1}integer'
    tag = utils.local_name_for_tag(element.tag)
    try:
        func = value_tags[tag]
    except KeyError:
        raise ValueError(f'bad tag: {element.tag}')
    return func(element)


class Value(CommonAttributes):
    '''
    The container for XMCDA values,
    '''
    _v = None

    def __init__(self, value=NA, **kw):
        '''
        value
        - an acceptable raw value
        - lxml.etree._Element

        If an XML element and keywaords are both supplied, the latter
        override any value read from the XML ; for example, if <value>
        has an attribute name and the method is called with a
        parameter 'name', the Value is initialised with the parameter
        'name' 's value.

        '''
        if isinstance(value, etree._Element):
            self.merge_xml(value)
            for k, v in kw.items():
                setattr(self, k, v)
            return
        for k, v in kw.items():
            setattr(self, k, v)
        self.v = value  # see the property v, below

    def as_float(self):
        to_float = getattr(self.v, 'to_float', None)
        if to_float is not None:
            self.v = to_float()
        else:
            self.v = float(self.v)

    def is_numeric(self, strict=False):
        if type(self.v) in (int, float, Rational):
            return True
        if not strict and type(self.v) is str:
            try:
                float(self.v)
                return True
            except ValueError:
                pass
        return False

    def _get_v(self):
        return self._v

    def _set_v(self, value):
        if type(value) not in value_types:
            raise ValueError(f'Invalid value with type {type(value)}')
        self._v = value

    v = property(_get_v, _set_v)

    def __str__(self):  # pragma: no cover There are tests for str(self.v)&repr
        if self.id is None and self.name is None and self.mcda_concept is None:
            return str(self.v)
        else:
            return repr(self)

    def __repr__(self):
        s = 'Value('
        s += f'id={self.id!r}, ' if self.id is not None else ''
        s += f'name={self.name!r}, ' if self.name is not None else ''
        s += (
            f'mcda_concept={self.mcda_concept!r}, '
            if self.mcda_concept is not None
            else ''
        )
        if s[-1] == ' ':
            s = s[:-2] + ', '
        s += str(self.v) + ')'
        return s

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)

        children = element.getchildren()
        if len(children) == 0:
            return

        child = element.getchildren()[0]
        self.v = value_for_element(child)

    def to_xml(self, tag='value'):
        '''Default is 'value' but it can be 'abscissa' or 'ordinate'''
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        _type = NA if self.v is NA else type(self.v)
        return getattr(E, tag)(value_to_xml[_type](self.v), **attributes)


class Values(list):
    '''
    '''
    def __init__(self, value=None):
        if value is None:
            return
        if isinstance(value, etree._Element):
            self.merge_xml(value)
        elif type(value) is Value:
            self.append(value)
        else:
            self.append(Value(value))

    def as_float(self):
        '''Convert all values into floats.

        It may raise ValueError or TypeError depending on the first
        element in the list which cannot be converted, just like
        float(x) does.

        '''
        for value in self:
            value.as_float()

    def is_numeric(self, strict=False):
        for value in self:
            if not value.is_numeric(strict):
                return False
        return True

    def merge_xml(self, element):
        for xml_value in xfindall(element, './value'):
            self.append(Value(xml_value))

    def to_xml(self):
        x = utils.element_maker().values
        x = x(*[v.to_xml() for v in self])
        return x

    def _get_v(self):
        if len(self) == 0:
            return None
        if len(self) != 1:
            raise ValueError(f'Undefined when Values() has {len(self)} Value')
        return self[0].v

    def _set_v(self, value):
        if value is None:
            self.clear()
        else:
            # do not clear before building the value because it may fail
            value = Value(value)
            self.clear()
            self.append(value)

    def _del_v(self):
        self.clear()

    v = property(_get_v, _set_v, _del_v)
