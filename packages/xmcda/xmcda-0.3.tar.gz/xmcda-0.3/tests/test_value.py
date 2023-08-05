from lxml import etree

import xmcda
from xmcda.value import (
    NA,
    FuzzyNumber,
    Interval,
    Rational,
    Value,
    ValuedLabel,
    _NAType,
)

from .utils import XMCDATestCase


class TestValue(XMCDATestCase):

    def tearDown(self):
        # restore defaults
        xmcda.reset_settings()

    def value(self, xml_as_string):
        xml = etree.fromstring(xml_as_string)
        return Value(xml)

    def check_as_float_is_float(self, value, f):
        "Apply as_float() to the supplied value and check that it is a float"
        value.as_float()
        self.assertIsInstance(value.v, float)
        self.assertEqual(value.v, f)

    # --
    def test_init(self):
        # init with xml element is tested in every test using self.value()
        # hence there is no need to test that one
        self.assertIsInstance(Value(1).v, int)
        self.assertIsInstance(Value(1.2).v, float)
        self.assertIsInstance(Value('label').v, str)
        self.assertIsInstance(Value(True).v, bool)
        self.assertIsInstance(Value(Rational()).v, Rational)
        self.assertIsInstance(Value(NA).v, _NAType)
        # ok  that's probably enough, now check an invalid type
        with self.assertRaises(ValueError):
            Value({})
        with self.assertRaises(ValueError):
            Value(None)

    xml_integer_value = '<value id="v1" name="n1"><integer>7</integer></value>'

    def test_init_with_args(self):
        v = Value(1, id='v1', name='n1', mcda_concept='mc1')
        self.assertEqual(v.id, 'v1')
        self.assertEqual(v.name, 'n1')
        self.assertEqual(v.mcda_concept, 'mc1')

        # (the following implies test_load_xml_integer())
        # Supplied attribute overrides the one read from xml
        v = Value(self.read_xml(self.xml_integer_value), id='my_id')
        self.assertEqual(v.id, 'my_id')
        self.assertEqual(v.name, 'n1')
        self.assertEqual(v.mcda_concept, None)

    xml_invalid = '<value><invalid>7</invalid></value>'

    def test_invalid_element(self):
        self.assertRaises(ValueError, self.value, TestValue.xml_invalid)

    xml_empty = '<value></value>'

    def test_empty_element(self):
        from .utils import utf8_to_utf8
        self.assertEqual(self.xml_NA, utf8_to_utf8(self.xml_empty, Value))

    def test_repr(self):
        v = Value(1.0)
        self.assertEqual(repr(v), 'Value(1.0)')
        v = Value(1.0, id='v1', name='n1', mcda_concept='mc1')
        self.assertEqual(
            repr(v), "Value(id='v1', name='n1', mcda_concept='mc1', 1.0)"
        )

    # --
    xml_integer = '<value><integer>7</integer></value>'

    def test_load_xml_integer(self):
        value = self.value(TestValue.xml_integer)
        self.assertEqual(value.v, 7)
        self.assertTrue(value.is_numeric())

    def test_to_xml_integer(self):
        self._test_to_xml(TestValue.xml_integer, Value)

    # --
    xml_integer_attrs = '''
<value id="v1" name="n1" mcdaConcept="m1">
  <integer>77</integer>
</value>'''

    def test_load_xml_integer_with_attributes(self):
        value = self.value(TestValue.xml_integer_attrs)
        self.assertEqual(value.v, 77)
        self.assertEqual(value.id, 'v1')
        self.assertEqual(value.name, 'n1')
        self.assertEqual(value.mcda_concept, 'm1')
        self.assertTrue(value.is_numeric())

    def test_to_xml_integer_attrs(self):
        self._test_to_xml(TestValue.xml_integer_attrs, Value)

    def test_integer_as_float(self):
        self.check_as_float_is_float(Value(7), 7.0)

    # --
    xml_real = '<value><real>70.5</real></value>'

    def test_load_xml_real(self):
        value = self.value(TestValue.xml_real)
        self.assertEqual(value.v, 70.5)
        self.assertTrue(value.is_numeric())

    def test_to_xml_real(self):
        self._test_to_xml(TestValue.xml_integer_attrs, Value)

    def test_real_as_float(self):
        self.check_as_float_is_float(Value(123.0), 123.0)

    # --
    xml_interval = '''
 <value>
    <interval>
        <lowerBound open="false">
            <integer>2</integer>
        </lowerBound>
        <upperBound open="true">
            <integer>3</integer>
        </upperBound>
    </interval>
 </value>'''

    def test_interval_init(self):
        value = Interval(12, 34)
        self.assertEqual(value.lower_bound, 12)
        self.assertEqual(value.upper_bound, 34)

    def test_interval(self):
        value = self.value(TestValue.xml_interval)
        interval = value.v
        self.assertIsInstance(interval, Interval)

        self.assertTrue(interval.is_lower_closed)
        self.assertIsInstance(interval.lower_bound, Value)
        self.assertEqual(interval.lower_bound.v, 2)

        self.assertFalse(interval.is_upper_closed)
        self.assertIsInstance(interval.upper_bound, Value)
        self.assertEqual(interval.upper_bound.v, 3)

        self.assertFalse(value.is_numeric())
        self.assertEqual(str(interval), '[2, 3[')

    def test_to_xml_interval(self):
        xmcda.set_export_defaults(True)
        self._test_to_xml(TestValue.xml_interval, Value)

    # same one
    xml_interval_no_defaults = '''
 <value>
    <interval>
        <lowerBound>
            <integer>2</integer>
        </lowerBound>
        <upperBound open="true">
            <integer>3</integer>
        </upperBound>
    </interval>
 </value>'''

    def test_to_xml_interval_defaults(self):
        xmcda.set_export_defaults(False)
        self._test_to_xml(TestValue.xml_interval_no_defaults, Value)

    xml_interval_default = '''
 <value>
    <interval>
        <!-- the default value for the attribute 'open': 'false'-->
        <lowerBound>
            <integer>2</integer>
        </lowerBound>
        <upperBound>
            <integer>3</integer>
        </upperBound>
    </interval>
 </value>'''

    def test_interval_default(self):
        value = self.value(TestValue.xml_interval_default)
        interval = value.v
        self.assertTrue(interval.is_lower_closed)
        self.assertTrue(interval.is_upper_closed)
        self.assertEqual(str(interval), '[2, 3]')

    def test_to_xml_interval_default(self):
        self._test_to_xml(TestValue.xml_interval_default, Value)

    # --
    xml_interval_no_upper_bound = '''
<value>
    <interval>
        <lowerBound open="false">
            <integer>22</integer>
        </lowerBound>
        <!-- no upper bound -->
    </interval>
</value>'''

    def test_interval_no_upper_bound(self):
        value = self.value(TestValue.xml_interval_no_upper_bound)
        interval = value.v
        self.assertIsInstance(interval, Interval)

        self.assertTrue(interval.is_lower_closed)
        self.assertIsInstance(interval.lower_bound, Value)
        self.assertEqual(interval.lower_bound.v, 22)

        self.assertIsNone(interval.upper_bound)
        self.assertEqual(str(interval), '[22, *]')

    def test_to_xml_no_upper_bound(self):
        xmcda.set_export_defaults(True)
        self._test_to_xml(TestValue.xml_interval_no_upper_bound, Value)

    # --
    xml_interval_no_lower_bound = '''
<value>
    <interval>
        <!-- no lower bound -->
        <upperBound open="false">
            <integer>33</integer>
        </upperBound>
    </interval>
</value>'''

    def test_interval_no_lower_bound(self):
        value = self.value(TestValue.xml_interval_no_lower_bound)
        interval = value.v
        self.assertIsInstance(value.v, Interval)

        self.assertIsNone(interval.lower_bound)

        self.assertTrue(interval.is_upper_closed)
        self.assertIsInstance(interval.upper_bound, Value)
        self.assertEqual(interval.upper_bound.v, 33)
        self.assertEqual(str(interval), '[*, 33]')

    def test_to_xml_no_lower_bound(self):
        xmcda.set_export_defaults(True)
        self._test_to_xml(TestValue.xml_interval_no_lower_bound, Value)

    def test_interval_as_float(self):
        with self.assertRaises(TypeError):
            self.check_as_float_is_float(Value(Interval(1, 2)), 0)

    # --
    xml_rational = '''
<value>
    <rational>
        <numerator>5</numerator>
        <denominator>55</denominator>
    </rational>
</value>
'''

    def test_rational_init(self):
        value = Rational(23, 54)
        self.assertEqual(value.numerator, 23)
        self.assertEqual(value.denominator, 54)

    def test_rational_defaults(self):
        self.assertEqual(Rational().numerator, 0)
        self.assertEqual(Rational().denominator, 0)

    def test_rational(self):
        value = self.value(TestValue.xml_rational)

        rational = value.v
        self.assertIsInstance(rational, Rational)

        self.assertEqual(rational.numerator, 5)
        self.assertEqual(rational.denominator, 55)

        self.assertTrue(value.is_numeric())

    def test_rational_str(self):
        value = Rational(23, 54)
        self.assertEqual(str(value), '23/54')

    def test_to_xml_rational(self):
        self._test_to_xml(TestValue.xml_rational, Value)

    def test_rational_to_float(self):
        inf = float('inf')
        self.assertEqual(Rational(10, 2).to_float(), 5.0)
        self.assertEqual(Rational(10, 0).to_float(), +inf)
        self.assertEqual(Rational(-1, 0).to_float(), -inf)
        import math
        self.assertTrue(math.isnan(Rational(0, 0).to_float()))

    def test_rational_as_float(self):
        self.check_as_float_is_float(Value(Rational(10, 2)), 5.0)

    # --
    xml_label = '<value><label>meuh</label></value>'
    xml_empty_label = '<value><label></label></value>'

    def test_label(self):
        value = self.value(TestValue.xml_label)
        self.assertIsInstance(value.v, str)
        self.assertEqual(value.v, 'meuh')
        self.assertFalse(value.is_numeric())

        value = self.value(TestValue.xml_empty_label)
        self.assertIsInstance(value.v, str)
        self.assertEqual(value.v, '')
        self.assertFalse(value.is_numeric())

    def test_to_xml_label(self):
        self._test_to_xml(TestValue.xml_label, Value)
        self._test_to_xml(TestValue.xml_empty_label, Value)

    # --
    xml_valued_label = '''
<value>
    <valuedLabel>
        <label>the label</label>
        <value>
            <integer>88</integer>
        </value>
    </valuedLabel>
</value>
'''

    def test_valued_label_init(self):
        value = ValuedLabel('a label', 2.34)
        self.assertEqual(value.label, 'a label')
        self.assertIsInstance(value.value, Value)
        self.assertEqual(value.value.v, 2.34)

    def test_valued_label(self):
        value = self.value(TestValue.xml_valued_label)
        vlabel = value.v
        self.assertIsInstance(vlabel, ValuedLabel)
        self.assertEqual(vlabel.label, 'the label')
        self.assertIsInstance(vlabel.value, Value)
        self.assertEqual(vlabel.value.v, 88)
        self.assertFalse(value.is_numeric())
        str(value)  # should not raise

    def test_to_xml_valued_label(self):
        self._test_to_xml(TestValue.xml_valued_label, Value)

    def test_valued_label_str(self):
        value = ValuedLabel('a label', 2.34)
        self.assertEqual(str(value), 'a label:2.34')

    def test_valued_label_as_float(self):
        with self.assertRaises(TypeError):
            self.check_as_float_is_float(Value(ValuedLabel('l', 2)), 0)

    # --
    xml_boolean = '<value><boolean>false</boolean></value>'

    def test_boolean(self):
        value = self.value(TestValue.xml_boolean)
        self.assertFalse(value.v)
        self.assertFalse(value.is_numeric())

    def test_to_xml_boolean(self):
        self._test_to_xml(TestValue.xml_boolean, Value)

    def test_boolean_as_float(self):
        self.check_as_float_is_float(Value(True), 1.0)

    # --
    xml_NA = '<value><NA/></value>'

    def test_NA(self):
        assert isinstance(NA, _NAType)

        value = self.value(TestValue.xml_NA)
        self.assertEqual(value.v, NA)
        self.assertFalse(value.is_numeric())

    def test_to_xml_NA(self):
        self._test_to_xml(TestValue.xml_NA, Value)

    def test_NA_str(self):
        value = NA
        self.assertEqual(str(value), 'N/A')

    def test_NA_as_float(self):
        with self.assertRaises(TypeError):
            self.check_as_float_is_float(Value(NA), 0)

    # --
    # Omit default head/tail is_open='false', so that to_xml can be tested
    # w/ xmcda.export defaults:=False
    #
    # Making sure that the unmarshalling of endpoints from xml is correct
    # wrt. the expected default value for the attribute 'is_open' is done
    # separately, cf. test_functions.py: TestEndPoint.test_defaults()
    #
    xml_fuzzy_number = '''
<value>
    <fuzzyNumber id="f01" name="nf01" mcdaConcept="mf01">
        <piecewiseLinear>
            <segment>
                    <head>
                       <abscissa>
                           <integer>7</integer>
                       </abscissa>
                       <ordinate>
                           <real>77.0</real>
                       </ordinate>
                    </head>
                    <tail open="true">
                        <abscissa>
                            <integer>8</integer>
                        </abscissa>
                        <ordinate>
                            <integer>88</integer>
                        </ordinate>
                    </tail>
            </segment>
            <segment>
                <head>
                    <abscissa>
                        <integer>9</integer>
                    </abscissa>
                    <ordinate>
                        <integer>99</integer>
                    </ordinate>
                </head>
                <tail>
                    <abscissa>
                        <integer>999</integer>
                    </abscissa>
                    <ordinate>
                        <integer>9999</integer>
                    </ordinate>
                </tail>
            </segment>
        </piecewiseLinear>
    </fuzzyNumber>
</value>
'''

    def test_fuzzy_number(self):
        value = self.value(TestValue.xml_fuzzy_number)
        fuzzy = value.v
        self.assertIsInstance(fuzzy, FuzzyNumber)
        self.assertEqual(fuzzy.id, 'f01')
        self.assertEqual(fuzzy.name, 'nf01')
        self.assertEqual(fuzzy.mcda_concept, 'mf01')

        self.assertEqual(len(fuzzy.segments), 2)
        segment_1 = fuzzy.segments[0]
        self.assertFalse(segment_1.head.is_open)
        self.assertEqual(segment_1.head.abscissa.v, 7)
        self.assertEqual(segment_1.head.ordinate.v, 77.0)
        self.assertTrue(segment_1.tail.is_open)
        self.assertEqual(segment_1.tail.abscissa.v, 8)
        self.assertEqual(segment_1.tail.ordinate.v, 88)

        self.assertFalse(value.is_numeric())

    def test_to_xml_fuzzy_number(self):
        xmcda.set_export_defaults(False)
        self._test_to_xml(TestValue.xml_fuzzy_number, Value)

    def test_fuzzy_number_str(self):
        value = self.value(TestValue.xml_fuzzy_number)
        self.assertTrue(
            str(value).startswith('<xmcda.value.FuzzyNumber object at ')
        )

    def test_fuzzy_number_as_float(self):
        value = self.value(TestValue.xml_fuzzy_number)
        with self.assertRaises(TypeError):
            self.check_as_float_is_float(value, 0)
