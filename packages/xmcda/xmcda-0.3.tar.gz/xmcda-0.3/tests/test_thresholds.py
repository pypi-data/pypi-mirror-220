from xmcda.thresholds import (
    AffineThreshold,
    ConstantThreshold,
    Threshold,
    Thresholds,
    Type,
)

from .utils import XMCDATestCase


class TestType(XMCDATestCase):

    def test_get(self):
        self.assertRaises(KeyError, Type.get, None)


class TestThreshold(XMCDATestCase):

    xml_empty = """<threshold/>"""

    def test_build_xml_empty(self):
        with self.assertRaises(ValueError):
            Threshold.build(self.read_xml(self.xml_empty))


class TestConstantThreshold(XMCDATestCase):

    xml_constant_threshold = '''
<threshold id="t" name="n" mcdaConcept="m">
    <constant>
        <integer>3210</integer>
    </constant>
</threshold>
'''

    def test_init_with_values(self):
        threshold = ConstantThreshold(id="constant", attr="misc")
        self.assertEqual(threshold.id, "constant")
        self.assertEqual(threshold.attr, "misc")

    def test_load_xml(self):
        threshold = Threshold.build(self.read_xml(self.xml_constant_threshold))
        self.assertIsInstance(threshold, ConstantThreshold)
        self.assertEqual(threshold.id, 't')
        self.assertEqual(threshold.name, 'n')
        self.assertEqual(threshold.mcda_concept, 'm')
        self.assertIsNotNone(threshold.value)
        self.assertEqual(threshold.value.v, 3210)

    def test_to_xml(self):
        self._test_to_xml(TestConstantThreshold.xml_constant_threshold,
                          ConstantThreshold)


class TestAffineThreshold(XMCDATestCase):

    xml_affine_no_type = '''
<threshold id="c" name="n" mcdaConcept="m">
    <affine>
        <slope>
            <real>1.0</real>
        </slope>
        <intercept>
            <integer>2</integer>
        </intercept>
    </affine>
</threshold>
'''

    xml_affine_with_type = '''
<threshold id="c" name="n" mcdaConcept="m">
    <affine>
        <type>inverse</type>
        <slope>
            <real>1.0</real>
        </slope>
        <intercept>
            <integer>2</integer>
        </intercept>
    </affine>
</threshold>
'''

    def test_init_with_values(self):
        threshold = AffineThreshold(id="affine", attr="misc.")
        self.assertEqual(threshold.id, "affine")
        self.assertEqual(threshold.attr, "misc.")

    def test_load_xml(self):
        threshold = Threshold.build(self.read_xml(self.xml_affine_no_type))
        self.assertIsInstance(threshold, AffineThreshold)
        self.assertEqual(threshold.type, Type.DIRECT)
        self.assertEqual(threshold.slope.v, 1.0)
        self.assertEqual(threshold.intercept.v, 2)

        threshold = Threshold.build(self.read_xml(self.xml_affine_with_type))
        self.assertIsInstance(threshold, AffineThreshold)
        self.assertEqual(threshold.type, Type.INVERSE)
        self.assertEqual(threshold.slope.v, 1.0)
        self.assertEqual(threshold.intercept.v, 2)

    def test_to_xml(self):
        self._test_to_xml(self.xml_affine_with_type, AffineThreshold)


class TestThresholds(XMCDATestCase):
    "NB: Most tests are in test_xxx_thresholds"

    def test_init_no_arg(self):
        thresholds = Thresholds()
        self.assertEqual(len(thresholds), 0)

    def test_init_does_not_accept_args(self):
        with self.assertRaises(TypeError):
            Thresholds(id='thresholds')
        thresholds = Thresholds()
        self.assertEqual(len(thresholds), 0)
