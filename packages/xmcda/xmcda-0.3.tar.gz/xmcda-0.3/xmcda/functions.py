'''
Defines the classes used by functions in XMCDA v3.
'''
from . import utils as U
from .mixins import CommonAttributes
from .utils import xfind, xfindall

# from .value import Value  # commented out to avoid circular dependency


class Point:
    abscissa = ordinate = None

    def __init__(self, xml_element=None, abscissa=None, ordinate=None):
        self.abscissa = abscissa
        self.ordinate = ordinate
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        from .value import Value
        self.abscissa = Value(xfind(element, 'abscissa'))
        self.ordinate = Value(xfind(element, 'ordinate'))

    def to_xml(self):
        E = U.element_maker()
        return E.point(self.abscissa.to_xml('abscissa'),
                       self.ordinate.to_xml('ordinate'))


class EndPoint(Point):
    is_open = False
    abscissa = ordinate = None

    def __init__(self, xml_element=None):
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)
        self.is_open = U.xml_boolean(element.get('open', 'false'))

    def to_xml(self, tag):
        E = U.element_maker()
        import xmcda
        kw = {}
        if xmcda.export_defaults() or self.is_open:
            kw['open'] = U.boolean_to_xml(self.is_open)

        return getattr(E, tag)(self.abscissa.to_xml('abscissa'),
                               self.ordinate.to_xml('ordinate'),
                               **kw)


class EndPointReference(EndPoint):
    end_point = None
    is_open = False

    def __init__(self, xml_element=None, end_point=None):
        if xml_element is not None:
            self.merge_xml(xml_element)
        self.end_point = end_point

    def merge_xml(self, element):
        self.is_open = U.xml_boolean(element.get('open', 'false'))

    def to_xml(self, tag):
        E = U.element_maker()
        import xmcda
        kw = {}
        if xmcda.export_defaults() or self.is_open:
            kw['open'] = U.boolean_to_xml(self.is_open)
        return getattr(E, tag)(**kw)

    def __getattr__(self, attr):
        return getattr(self.end_point, attr)


class Segment:
    head = tail = None

    def __init__(self, xml_element=None):
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        head = xfind(element, 'head')
        if not len(head):
            self.head = EndPointReference(xfind(element, 'head'))
        else:
            self.head = EndPoint(xfind(element, 'head'))
        self.tail = EndPoint(xfind(element, 'tail'))

    def to_xml(self):
        E = U.element_maker()
        return E.segment(self.head.to_xml('head'), self.tail.to_xml('tail'))


class Function(CommonAttributes):

    @staticmethod
    def build(element):
        if xfind(element, 'constant') is not None:
            return ConstantFunction(element)

        if xfind(element, 'affine') is not None:
            return AffineFunction(element)

        if xfind(element, 'discrete') is not None:
            return DiscreteFunction(element)

        if xfind(element, 'piecewiseLinear') is not None:
            return PiecewiseLinearFunction(element)

        msg = (
            "Could not find any of the required child: constant, affine, "
            "discrete or piecewiseLinear"
        )
        raise ValueError(msg)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)

    def to_xml(self):
        E = U.element_maker()
        attributes = U.CommonAttributes_as_dict(self)
        func = E.function
        if isinstance(self, ConstantFunction):
            constant = self.value.to_xml('constant')
            return func(constant, **attributes)
        if isinstance(self, AffineFunction):
            return func(E.affine(self.slope.to_xml('slope'),
                                 self.intercept.to_xml('intercept')),
                        **attributes)
        if isinstance(self, DiscreteFunction):
            return func(E.discrete(*(p.to_xml() for p in self.points)),
                        **attributes)
        # NB: PiecewiseLinearFunction handles itself
        raise ValueError("Function object cannot be serialised")


class ConstantFunction(Function):

    value = None

    def __init__(self, xml_element=None):
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)
        from .value import Value
        self.value = Value(xfind(element, 'constant'))


class AffineFunction(Function):
    slope = intercept = 0

    def __init__(self, xml_element=None):
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)
        from .value import Value
        element = xfind(element, 'affine')
        self.slope = Value(xfind(element, 'slope'))
        self.intercept = Value(xfind(element, 'intercept'))


class DiscreteFunction(Function):

    def __init__(self, xml_element=None):
        self.points = []
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)
        element = xfind(element, 'discrete')
        for p in xfindall(element, 'point'):
            self.points.append(Point(p))


class PiecewiseLinearFunction(Function):

    def __init__(self, xml_element=None):
        self.segments = []
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        super().merge_xml(element)
        element = xfind(element, 'piecewiseLinear')
        for p in xfindall(element, 'segment'):
            self.segments.append(Segment(p))
        for idx, segment in enumerate(self.segments[1:]):
            if isinstance(segment.head, EndPointReference):
                segment.head.end_point = self.segments[idx].tail

    def to_xml(self):
        E = U.element_maker()
        attributes = U.CommonAttributes_as_dict(self)

        segments = list(self.segments)
        prev_tail = self.segments[0].tail if len(self.segments) != 0 else None
        for idx, segment in enumerate(segments[1:]):
            if prev_tail is not None and segment.head is prev_tail:
                segments[idx+1] = Segment()
                segments[idx+1].head = EndPointReference(end_point=segment.head)
                segments[idx+1].tail = segment.tail
                segments[idx+1].head.is_open = segment.head.is_open
            prev_tail = segment.tail
        children = (s.to_xml() for s in segments)
        return E.function(E.piecewiseLinear(*children), **attributes)


class Functions(list):
    # modeled after Scales or Thresholds
    # These two ones have a description but <functions> has none.  Still,
    # we model it the same way to be consistent
    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        # no description in the schema (for now?)
        for function in xfindall(element, './function'):
            self.append(Function.build(function))

    def to_xml(self):
        E = U.element_maker()
        functions = E.functions()
        for function in self:
            functions.append(function.to_xml())
        return functions
