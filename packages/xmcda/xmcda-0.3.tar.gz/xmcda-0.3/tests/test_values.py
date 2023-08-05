from xmcda.value import (
    NA,
    FuzzyNumber,
    Interval,
    Rational,
    Value,
    ValuedLabel,
    Values,
    _NAType,
)

from .utils import XMCDATestCase


class TestValues(XMCDATestCase):

    def values(self, xml_as_string):
        xml = self.read_xml(xml_as_string)
        return Values(xml)

    xml_values = '''
            <values>
                <value>
                    <real>1.0</real>
                </value>
                <value>
                    <NA/>
                </value>
                <value>
                    <rational>
                        <numerator>2</numerator>
                        <denominator>3</denominator>
                    </rational>
                </value>
            </values>'''

    def test_load_xml(self):
        values = self.values(TestValues.xml_values)
        self.assertEqual(len(values), 3)
        # respect xml ordering
        self.assertIsInstance(values[0].v, float)
        self.assertEqual(values[1].v, NA)
        self.assertIsInstance(values[2].v, Rational)

    def check_init_with_raw_value(self, raw_value, raw_type):
        values = Values(raw_value)
        self.assertEqual(len(values), 1)
        self.assertIsInstance(values[0], Value)
        self.assertIsInstance(values[0].v, type(raw_value))
        self.assertIsInstance(values[0].v, raw_type)
        self.assertEqual(values[0].v, raw_value)

    def test_init(self):
        # init with xml element is tested in every test using self.values()
        # hence there is no need to test that one here
        self.check_init_with_raw_value(1, int)
        self.check_init_with_raw_value(1.2, float)
        self.check_init_with_raw_value(Interval(), Interval)
        self.check_init_with_raw_value(Rational(), Rational)
        self.check_init_with_raw_value('label', str)
        self.check_init_with_raw_value(ValuedLabel(), ValuedLabel)
        self.check_init_with_raw_value(True, bool)
        self.check_init_with_raw_value(NA, _NAType)
        self.check_init_with_raw_value(FuzzyNumber(), FuzzyNumber)

        values = Values(Value(12))
        self.assertEqual(len(values), 1)
        self.assertIsInstance(values[0], Value)
        self.assertEqual(values[0].v, 12)

        with self.assertRaises(ValueError):
            Values({})

    def _build_values(self):
        strictly_numerical = [1, 3.14, Rational(1, 2)]
        numerical = strictly_numerical + ['12345.6789']
        non_numerical_str = strictly_numerical + ['dead parrot']
        non_numerical_NA = strictly_numerical + [NA]

        def build_values(raw_values):
            values = Values()
            for raw_value in raw_values:
                values.append(Value(raw_value))
            return values

        return (
            build_values(strictly_numerical),
            build_values(numerical),
            build_values(non_numerical_str),
            build_values(non_numerical_NA),
        )

    def test_is_numeric(self):
        (strictly_numerical, numerical,
         non_numerical_str, non_numerical_NA) = self._build_values()
        self.assertTrue(strictly_numerical.is_numeric())
        self.assertTrue(strictly_numerical.is_numeric(True))

        self.assertTrue(numerical.is_numeric())
        self.assertFalse(numerical.is_numeric(True))

        self.assertFalse(non_numerical_str.is_numeric())
        self.assertFalse(non_numerical_str.is_numeric(True))

        self.assertFalse(non_numerical_NA.is_numeric())
        self.assertFalse(non_numerical_NA.is_numeric(True))

    def test_as_float(self):
        (strictly_numerical, numerical,
         non_numerical_str, non_numerical_NA) = self._build_values()

        strictly_numerical.as_float()
        numerical.as_float()
        self.assertRaises(ValueError, non_numerical_str.as_float)
        self.assertRaises(TypeError, non_numerical_NA.as_float)

    def test_v_property(self):
        values = Values()
        values.v = 1
        self.assertEqual(len(values), 1)
        self.assertIsInstance(values[0], Value)

        del values.v
        self.assertEqual(len(values), 0)
        self.assertIsNone(values.v)

        values.append(Value(1))
        values.append(Value(2.2))
        with self.assertRaises(ValueError):
            values.v

        values.v = None
        self.assertEqual(len(values), 0)
        self.assertIsNone(values.v)
