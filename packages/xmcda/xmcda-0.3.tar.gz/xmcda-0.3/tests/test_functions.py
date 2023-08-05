import xmcda
from xmcda.functions import (
    AffineFunction,
    ConstantFunction,
    DiscreteFunction,
    EndPoint,
    EndPointReference,
    Function,
    Functions,
    PiecewiseLinearFunction,
    Point,
    Segment,
)
from xmcda.value import Value, ValuedLabel

from .utils import XMCDATestCase, compact_xml, element_to_utf8


class TestPoint(XMCDATestCase):

    # --
    xml_point = '''
<point>
    <abscissa>
        <valuedLabel>
            <label>bad</label>
            <value>
                <integer>3</integer>
            </value>
        </valuedLabel>
    </abscissa>
    <ordinate>
        <real>1.2</real>
     </ordinate>
</point>'''

    def test_load_xml(self):
        point = Point(self.read_xml(TestPoint.xml_point))
        self.assertIsInstance(point, Point)
        self.assertIsInstance(point.abscissa, Value)
        self.assertIsInstance(point.ordinate, Value)

        self.assertIsInstance(point.abscissa.v, ValuedLabel)
        self.assertIsInstance(point.ordinate.v, float)

    def test_to_xml(self):
        self._test_to_xml(TestPoint.xml_point, Point)


class TestEndPoint(XMCDATestCase):
    'Used in piecewiseLinearFunction.segments'

    def tearDown(self):
        xmcda.reset_settings()

    def test_defaults(self):
        p = EndPoint()
        self.assertFalse(p.is_open)

    # --
    xml_endpoint_1 = '''
        <head open="true">
            <abscissa><integer>50</integer></abscissa>
            <ordinate><real>0.007</real></ordinate>
        </head>'''

    xml_endpoint_2a = '''
        <head>
            <abscissa><integer>50</integer></abscissa>
            <ordinate><real>0.007</real></ordinate>
        </head>'''

    xml_endpoint_2b = '''
        <head open="false">
            <abscissa><integer>50</integer></abscissa>
            <ordinate><real>0.007</real></ordinate>
        </head>'''

    xml_endpoint_3 = '''
        <tail>
            <abscissa><integer>50</integer></abscissa>
            <ordinate><real>0.007</real></ordinate>
        </tail>'''

    def test_load_xml_1(self):
        point = EndPoint(self.read_xml(TestEndPoint.xml_endpoint_1))
        self.assertIsInstance(point, EndPoint)
        self.assertIsInstance(point.abscissa, Value)
        self.assertIsInstance(point.ordinate, Value)

        self.assertTrue(point.is_open)
        self.assertEqual(point.abscissa.v, 50)
        self.assertEqual(point.ordinate.v, 0.007)

    def test_load_xml_2(self):
        point = EndPoint(self.read_xml(TestEndPoint.xml_endpoint_2a))
        self.assertIsInstance(point, EndPoint)
        self.assertIsInstance(point.abscissa, Value)
        self.assertIsInstance(point.ordinate, Value)

        self.assertFalse(point.is_open)
        self.assertEqual(point.abscissa.v, 50)
        self.assertEqual(point.ordinate.v, 0.007)

    def test_load_xml_3(self):
        point = EndPoint(self.read_xml(TestEndPoint.xml_endpoint_3))
        self.assertFalse(point.is_open)
        self.assertEqual(point.abscissa.v, 50)

    def test_to_xml_1(self):
        self._test_to_xml(TestEndPoint.xml_endpoint_1, EndPoint, 'head')
        self._test_to_xml(TestEndPoint.xml_endpoint_2a, EndPoint, 'head')
        xmcda.set_export_defaults(True)
        from .utils import compact_xml
        r = EndPoint(self.read_xml(TestEndPoint.xml_endpoint_2a))
        r = xmcda.utils.tostring(r.to_xml('head'))
        r = compact_xml(r)
        self.assertEqual(r, compact_xml(TestEndPoint.xml_endpoint_2b))

    def test_to_xml_3(self):
        self._test_to_xml(TestEndPoint.xml_endpoint_3, EndPoint, 'tail')

    # --
    def _test_to_xml(self, xml, _type, tag):
        # redefined because to_xml() requires the tag as an additional param.
        from .utils import compact_xml, utf8_to_element
        source = compact_xml(xml)

        end_point = utf8_to_element(xml, EndPoint)
        result = xmcda.utils.tostring(end_point.to_xml(tag))

        self.assertEqual(source, result)


class TestEndPointReference(XMCDATestCase):

    def test_1(self):
        pt = EndPoint()
        pt.abscissa = Value(1)
        pt.ordinate = Value(11.1)
        ref = EndPointReference(end_point=pt)
        self.assertEqual(ref.end_point, pt)
        self.assertIs(ref.end_point.abscissa, pt.abscissa)
        self.assertIs(ref.end_point.ordinate, pt.ordinate)

        pt.is_open = True
        ref.is_open = False
        self.assertTrue(pt.is_open)  # the two attributes are independent
        self.assertFalse(ref.is_open)

        # and any other attribute in the original point is proxied
        pt.any_attribute = []
        self.assertIs(ref.any_attribute, pt.any_attribute)


class TestConstantFunction(XMCDATestCase):

    xml_constant_function = '''
<function id="c" name="n" mcdaConcept="m">
    <constant>
        <integer>3210</integer>
    </constant>
</function>
'''

    def test_load_xml(self):
        func = Function.build(self.read_xml(self.xml_constant_function))
        self.assertIsInstance(func, ConstantFunction)
        self.assertIsNotNone(func.value)
        self.assertEqual(func.value.v, 3210)
        self.assertEqual(func.id, 'c')
        self.assertEqual(func.name, 'n')
        self.assertEqual(func.mcda_concept, 'm')

    def test_to_xml(self):
        self._test_to_xml(TestConstantFunction.xml_constant_function,
                          ConstantFunction)


class TestAffineFunction(XMCDATestCase):

    xml_affine_function = '''
<function id="c" name="n" mcdaConcept="m">
    <affine>
        <slope>
            <real>1.0</real>
        </slope>
        <intercept>
            <integer>2</integer>
        </intercept>
    </affine>
</function>
'''

    def test_load_xml(self):
        func = Function.build(self.read_xml(self.xml_affine_function))
        self.assertIsInstance(func, AffineFunction)
        self.assertEqual(func.slope.v, 1.0)
        self.assertEqual(func.intercept.v, 2)

    def test_to_xml(self):
        self._test_to_xml(self.xml_affine_function, AffineFunction)


class TestDiscreteFunction(XMCDATestCase):

    xml_discrete_function = '''
<function id="c" name="n" mcdaConcept="m">
    <discrete>
        <point>
            <abscissa>
                <valuedLabel>
                    <label>who's bad</label>
                    <value>
                        <integer>3</integer>
                    </value>
                </valuedLabel>
            </abscissa>
            <ordinate>
                <real>0.0</real>
            </ordinate>
        </point>
        <point>
            <abscissa>
                <valuedLabel>
                    <label>medium</label>
                    <value>
                        <integer>2</integer>
                    </value>
                </valuedLabel>
            </abscissa>
            <ordinate>
                <real>0.125</real>
            </ordinate>
        </point>
        <point>
            <abscissa>
                <valuedLabel>
                    <label>good</label>
                    <value>
                        <integer>1</integer>
                    </value>
                </valuedLabel>
            </abscissa>
            <ordinate>
                <real>1.0</real>
            </ordinate>
        </point>
    </discrete>
</function>

'''

    def test_load_xml(self):
        func = Function.build(self.read_xml(self.xml_discrete_function))
        self.assertIsInstance(func, DiscreteFunction)
        self.assertEqual(len(func.points), 3)

        self.assertIsInstance(func.points[0].abscissa.v, ValuedLabel)
        self.assertEqual(func.points[0].abscissa.v.label, "who's bad")
        self.assertEqual(func.points[0].ordinate.v, 0.0)

    def test_defaults(self):
        func = DiscreteFunction()
        self.assertIsInstance(func.points, list)
        self.assertEqual(len(func.points), 0)

    def test_to_xml(self):
        self._test_to_xml(self.xml_discrete_function, DiscreteFunction)


class TestSegment(XMCDATestCase):

    def test_defaults(self):
        s = Segment()
        self.assertIsNone(s.head)
        self.assertIsNone(s.tail)

    xml_1 = '''
            <segment>
                <head><!-- default: open="false" -->
                   <abscissa>
                       <integer>11</integer>
                   </abscissa>
                   <ordinate>
                       <real>111.0</real>
                   </ordinate>
                </head>
                <tail open="true">
                    <abscissa>
                        <integer>22</integer>
                    </abscissa>
                    <ordinate>
                        <integer>222</integer>
                    </ordinate>
                </tail>
            </segment>'''

    def test_merge_xml_1(self):
        s = Segment()
        xml = self.read_xml(TestSegment.xml_1)
        s.merge_xml(xml)
        self.assertIsNotNone(s.head)
        self.assertIsNotNone(s.tail)
        self.assertFalse(s.head.is_open)
        self.assertTrue(s.tail.is_open)


class TestPiecewiseLinearFunction(XMCDATestCase):

    xml_piecewise_linear_fct = '''
<function id="i" name="n" mcdaConcept="m">
    <piecewiseLinear>
        <segment>
            <head>
                <abscissa>
                    <real>50.0</real>
                </abscissa>
                <ordinate>
                    <real>0.0</real>
                </ordinate>
            </head>
            <tail open="true">
                <abscissa>
                    <real>100.0</real>
                </abscissa>
                <ordinate>
                    <real>0.125</real>
                </ordinate>
            </tail>
        </segment>
        <segment>
            <head>
                <abscissa>
                    <real>100.0</real>
                </abscissa>
                <ordinate>
                    <real>0.125</real>
                </ordinate>
            </head>
            <tail>
                <abscissa>
                    <real>200.0</real>
                </abscissa>
                <ordinate>
                    <real>1.0</real>
                </ordinate>
            </tail>
        </segment>
    </piecewiseLinear>
</function>
'''

    def test_load_xml(self):
        func = Function.build(self.read_xml(self.xml_piecewise_linear_fct))
        self.assertIsInstance(func, PiecewiseLinearFunction)
        self.assertEqual(func.id, 'i')
        self.assertEqual(func.name, 'n')
        self.assertEqual(func.mcda_concept, 'm')
        self.assertEqual(len(func.segments), 2)
        self.assertFalse(func.segments[0].head.is_open)
        self.assertTrue(func.segments[0].tail.is_open)
        self.assertFalse(func.segments[1].head.is_open)  # defaults

    def test_to_xml(self):
        self.maxDiff = None
        self._test_to_xml(self.xml_piecewise_linear_fct,
                          PiecewiseLinearFunction)

    xml_plf_with_empty_heads = '''
<function id="i" name="n" mcdaConcept="m">
    <piecewiseLinear>
        <segment>
            <head>
                <abscissa>
                    <integer>1</integer>
                </abscissa>
                <ordinate>
                    <integer>11</integer>
                </ordinate>
            </head>
            <tail open="true">
                <abscissa>
                    <integer>2</integer>
                </abscissa>
                <ordinate>
                    <integer>22</integer>
                </ordinate>
            </tail>
        </segment>
        <segment>
            <head/>
            <tail>
                <abscissa>
                    <integer>3</integer>
                </abscissa>
                <ordinate>
                    <integer>33</integer>
                </ordinate>
            </tail>
         </segment>
         <segment>
            <head open="true"/>
            <tail>
                <abscissa>
                    <integer>4</integer>
                </abscissa>
                <ordinate>
                    <integer>44</integer>
                </ordinate>
            </tail>
       </segment>
    </piecewiseLinear>
</function>
'''

    def test_load_xml_plf_with_empty_heads(self):
        func = Function.build(self.read_xml(self.xml_plf_with_empty_heads))
        self.assertIsInstance(func, PiecewiseLinearFunction)
        self.assertEqual(func.id, 'i')
        self.assertEqual(func.name, 'n')
        self.assertEqual(func.mcda_concept, 'm')
        self.assertEqual(len(func.segments), 3)
        self.assertFalse(func.segments[0].head.is_open)
        self.assertTrue(func.segments[0].tail.is_open)

        # is_open is independent in the reference
        self.assertFalse(func.segments[1].head.is_open)
        self.assertFalse(func.segments[1].tail.is_open)  # defaults

        self.assertTrue(func.segments[2].head.is_open)

        for p in (func.segments[1].head, func.segments[2].head):
            self.assertIsInstance(p, EndPointReference)
        self.assertIs(func.segments[0].tail, func.segments[1].head.end_point)
        self.assertIs(func.segments[1].tail, func.segments[2].head.end_point)

    def test_to_xml_2(self):
        self.maxDiff = None
        self._test_to_xml(self.xml_plf_with_empty_heads,
                          PiecewiseLinearFunction)

    xml_plf_expected_output_with_assignments = '''
<function id="i" name="n" mcdaConcept="m">
    <piecewiseLinear>
        <segment>
            <head>
                <abscissa>
                    <integer>1</integer>
                </abscissa>
                <ordinate>
                    <integer>11</integer>
                </ordinate>
            </head>
            <tail open="true">
                <abscissa>
                    <integer>2</integer>
                </abscissa>
                <ordinate>
                    <integer>22</integer>
                </ordinate>
            </tail>
        </segment>
        <segment>
            <head open="true"/>
            <tail>
                <abscissa>
                    <integer>3</integer>
                </abscissa>
                <ordinate>
                    <integer>33</integer>
                </ordinate>
            </tail>
         </segment>
         <segment>
            <head/>
            <tail>
                <abscissa>
                    <integer>4</integer>
                </abscissa>
                <ordinate>
                    <integer>44</integer>
                </ordinate>
            </tail>
       </segment>
    </piecewiseLinear>
</function>
'''

    def test_plf_output_with_assignment(self):
        """
        We test here tthat when a segment's tail is programmatically
        assigned to its successor's head, the XMDCA output is the same
        as when a EndPointReference is used
        """
        func = Function.build(self.read_xml(self.xml_plf_with_empty_heads))
        # no ref, just a plain assignment
        func.segments[1].head = func.segments[0].tail
        func.segments[2].head = func.segments[1].tail
        # check that this is saved
        # as xml_plf_expected_output_with_assignments
        self.assertEqual(
            compact_xml(self.xml_plf_expected_output_with_assignments),
            element_to_utf8(func)
        )


class TestFunction(XMCDATestCase):

    empty_xml = '<function/>'

    invalid_xml = '<function><invalid_tag/></function>'

    def test_build_failure(self):
        with self.assertRaises(ValueError):
            Function.build(self.read_xml(self.empty_xml))
        with self.assertRaises(ValueError):
            Function.build(self.read_xml(self.invalid_xml))

    def test_to_xml_failure(self):
        f = Function()
        with self.assertRaises(ValueError):
            f.to_xml()


class TestFunctions(XMCDATestCase):

    def test_init_with_kw(self):
        f = Functions(id='fs', attr=78)
        self.assertEqual(f.id, 'fs')
        self.assertEqual(f.attr, 78)

    xml = '<functions/>'

    def test_init(self):
        Functions(self.read_xml(self.xml))  # empty, should not raise
