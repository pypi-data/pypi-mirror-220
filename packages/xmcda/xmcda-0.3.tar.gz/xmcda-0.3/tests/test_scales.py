from xmcda.scales import (
    NominalScale,
    PreferenceDirection,
    QualitativeScale,
    QuantitativeScale,
    Scale,
    ScaleReference,
    Scales,
)

from .utils import XMCDATestCase, compact_xml


class TestPreferenceDirection(XMCDATestCase):

    def test_get(self):
        UNSET = PreferenceDirection.UNSET
        MIN = PreferenceDirection.MIN
        MAX = PreferenceDirection.MAX
        self.assertEqual(PreferenceDirection.get_from_xml('min'), MIN)
        self.assertEqual(PreferenceDirection.get_from_xml('MIN'), MIN)
        self.assertEqual(PreferenceDirection.get_from_xml('max'), MAX)
        self.assertEqual(PreferenceDirection.get_from_xml('MAX'), MAX)
        self.assertEqual(PreferenceDirection.get_from_xml(None), UNSET)
        self.assertRaises(KeyError, PreferenceDirection.get_from_xml, 'unset')
        self.assertRaises(KeyError, PreferenceDirection.get_from_xml, 'UNSET')
        self.assertRaises(KeyError, PreferenceDirection.get_from_xml, 'invalid')
        self.assertRaises(KeyError, PreferenceDirection.get_from_xml, 1)


class TestScale(XMCDATestCase):

    def test_init(self):
        scale = NominalScale(id="s1", name="s1n")
        self.assertEqual(scale.id, "s1")
        self.assertEqual(scale.name, "s1n")
        scale = QualitativeScale(id="s1", name="s1n")
        self.assertEqual(scale.id, "s1")
        self.assertEqual(scale.name, "s1n")
        scale = QuantitativeScale(id="s1", name="s1n")
        self.assertEqual(scale.id, "s1")
        self.assertEqual(scale.name, "s1n")

    xml_invalid = """
        <scale id="n1" name="n1n" mcdaConcept="n1m"/>
    """

    def test_invalid(self):
        xml_invalid = self.read_xml(self.xml_invalid)
        self.assertRaises(ValueError, Scale.build, xml_invalid)

    xml_nominal = '''
        <scale id="n1" name="n1n" mcdaConcept="n1m">
            <nominal>
                <labels>
                    <label>meuh</label>
                    <label>cuicui</label>
                    <label>kot-kodek</label>
                </labels>
            </nominal>
        </scale>
    '''

    def test_nominal_from_xml(self):
        xml = self.read_xml(self.xml_nominal)
        nominal = Scale.build(xml)

        self.assertIsInstance(nominal, NominalScale)
        self.assertEqual(nominal.id, 'n1')
        self.assertEqual(nominal.name, 'n1n')
        self.assertEqual(nominal.mcda_concept, 'n1m')
        self.assertEqual(len(nominal.labels), 3)
        self.assertEqual(nominal.labels[0], 'meuh')

    def test_nominal_to_xml(self):
        self._test_to_xml(self.xml_nominal, NominalScale)

    def test_nominal_bad_element(self):
        self.assertRaises(ValueError, NominalScale,
                          self.read_xml(self.xml_qualitative))
        self.assertRaises(ValueError, NominalScale,
                          self.read_xml(self.xml_quantitative))

    xml_qualitative = '''
        <scale id="ql1" name="ql1n" mcdaConcept="ql1m">
            <qualitative>
                <preferenceDirection>min</preferenceDirection>
                <valuedLabels>
                  <valuedLabel>
                    <label>one</label>
                    <value>
                      <integer>1</integer>
                    </value>
                  </valuedLabel>
                </valuedLabels>
             </qualitative>
        </scale>
    '''

    def test_qualitative_from_xml(self):
        xml = self.read_xml(self.xml_qualitative)
        qualitative = Scale.build(xml)

        self.assertIsInstance(qualitative, QualitativeScale)
        self.assertEqual(qualitative.id, 'ql1')
        self.assertEqual(qualitative.name, 'ql1n')
        self.assertEqual(qualitative.mcda_concept, 'ql1m')
        self.assertEqual(len(qualitative.valued_labels), 1)
        self.assertEqual(qualitative.valued_labels[0].label, 'one')
        self.assertEqual(qualitative.valued_labels[0].value.v, 1)

    def test_qualitative_to_xml(self):
        self._test_to_xml(self.xml_qualitative, QualitativeScale)

    def test_qualitative_bad_element(self):
        self.assertRaises(ValueError, QualitativeScale,
                          self.read_xml(self.xml_nominal))
        self.assertRaises(ValueError, QualitativeScale,
                          self.read_xml(self.xml_quantitative))

    # -- empty qualitative scale
    xml_empty_qualitative = '''
        <scale id="ql1" name="ql1n" mcdaConcept="ql1m">
            <qualitative/>
        </scale>
    '''

    def test_empty_qualitative_from_xml_(self):
        xml = self.read_xml(self.xml_empty_qualitative)
        qualitative = Scale.build(xml)
        self.assertEqual(qualitative.preference_direction,
                         PreferenceDirection.UNSET)

    def test_empty_qualitative_to_xml(self):
        self._test_to_xml(self.xml_empty_qualitative, QualitativeScale)

    # --
    xml_quantitative = '''
        <scale id="qt1" name="qt1n" mcdaConcept="qt1m">
            <quantitative>
                <preferenceDirection>min</preferenceDirection>
                <minimum><real>0.0</real></minimum>
                <maximum><real>100.0</real></maximum>
            </quantitative>
        </scale>
    '''

    def test_quantitative_from_xml(self):
        xml = self.read_xml(self.xml_quantitative)
        quantitative = Scale.build(xml)

        self.assertIsInstance(quantitative, QuantitativeScale)
        self.assertEqual(quantitative.id, 'qt1')
        self.assertEqual(quantitative.name, 'qt1n')
        self.assertEqual(quantitative.mcda_concept, 'qt1m')
        self.assertEqual(quantitative.preference_direction,
                         PreferenceDirection.MIN)
        self.assertEqual(quantitative.minimum.v, 0.0)
        self.assertEqual(quantitative.maximum.v, 100.0)

    def test_quantitative_to_xml(self):
        self._test_to_xml(self.xml_quantitative, QuantitativeScale)

    # -- empty quantitative scale
    xml_empty_quantitative = '''
        <scale id="qt1" name="qt1n" mcdaConcept="qt1m">
            <quantitative/>
        </scale>
    '''

    def test_empty_quantitative_from_xml(self):
        xml = self.read_xml(self.xml_empty_quantitative)
        quantitative = Scale.build(xml)
        self.assertEqual(quantitative.preference_direction,
                         PreferenceDirection.UNSET)

    def test_empty_quantitative_to_xml(self):
        self._test_to_xml(self.xml_empty_quantitative, QuantitativeScale)

    # --
    xml_quantitative_no_min_max = '''
        <scale id="qt1" name="qt1n" mcdaConcept="qt1m">>
            <quantitative>
                <preferenceDirection>min</preferenceDirection>
            </quantitative>
        </scale>
    '''

    def test_quantitative_no_min_max_from_xml(self):
        xml = self.read_xml(self.xml_quantitative_no_min_max)
        quantitative = Scale.build(xml)

        self.assertIsInstance(quantitative, QuantitativeScale)
        self.assertEqual(quantitative.id, 'qt1')
        self.assertEqual(quantitative.name, 'qt1n')
        self.assertEqual(quantitative.mcda_concept, 'qt1m')
        self.assertEqual(quantitative.preference_direction,
                         PreferenceDirection.MIN)
        self.assertEqual(quantitative.minimum, None)
        self.assertEqual(quantitative.maximum, None)

    def test_quantitative_bad_element(self):
        self.assertRaises(ValueError, QuantitativeScale,
                          self.read_xml(self.xml_nominal))
        self.assertRaises(ValueError, QuantitativeScale,
                          self.read_xml(self.xml_qualitative))


class TestScales(XMCDATestCase):

    def test_init(self):
        scales = Scales(id="s1", name="s1n")
        self.assertEqual(scales.id, "s1")
        self.assertEqual(scales.name, "s1n")

    xml_scales = '''
        <scales>
            <description><comment>cuicui</comment></description>
            <scale>
                <nominal>
                    <labels>
                        <label>piou-piou</label>
                    </labels>
                </nominal>
            </scale>
            <scale>
                <qualitative>
                    <preferenceDirection>min</preferenceDirection>
                </qualitative>
            </scale>
            <scale>
                <quantitative>
                    <preferenceDirection>min</preferenceDirection>
                </quantitative>
            </scale>
        </scales>
    '''

    def test_from_xml(self):
        scales = Scales(self.read_xml(self.xml_scales))

        self.assertEqual(scales.description.comment, 'cuicui')
        self.assertEqual(len(scales), 3)
        self.assertIsInstance(scales[0], NominalScale)
        self.assertIsInstance(scales[1], QualitativeScale)
        self.assertIsInstance(scales[2], QuantitativeScale)

    def test_to_xml(self):
        self._test_to_xml(self.xml_scales, Scales)


class TestScalesWithRefID(XMCDATestCase):
    """
    Test for scales being referenced by scaleID
    """

    xml_scales = """
        <scales>
            <scaleID>a_scale_id</scaleID>
            <scale id="a_scale_id">
                <nominal>
                    <labels>
                        <label>piou-piou</label>
                    </labels>
                </nominal>
            </scale>
            <scaleID>a_scale_id</scaleID>
            <scaleID>unknown_scale_id</scaleID>
        </scales>
    """
    xml_scales_equiv = """
        <scales>
            <scale id="a_scale_id">
                <nominal>
                    <labels>
                        <label>piou-piou</label>
                    </labels>
                </nominal>
            </scale>
            <scaleID>a_scale_id</scaleID>
            <scaleID>a_scale_id</scaleID>
            <scaleID>unknown_scale_id</scaleID>
        </scales>
    """

    def test_load_referenced_id(self):
        scales = Scales(self.read_xml(self.xml_scales))
        self.assertEqual(len(scales), 4)
        for scale in scales[:2]:
            self.assertIsInstance(scale, NominalScale)
        self.assertIs(scales[0], scales[1])
        self.assertIs(scales[2], scales[1])
        self.assertIsInstance(scales[3], ScaleReference)

    def test_to_xml(self):
        equivalent = compact_xml(self.xml_scales_equiv)
        self._test_to_xml(self.xml_scales, Scales, equivalent)
