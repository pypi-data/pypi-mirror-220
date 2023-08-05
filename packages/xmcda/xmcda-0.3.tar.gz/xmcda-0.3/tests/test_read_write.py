# -*- coding: utf-8 -*-
from xmcda import set_version, version
from xmcda.schemas import XMCDA_3_1_1
from xmcda.XMCDA import XMCDA

from .utils import XMCDATestCase


class TestWriteXMCDA(XMCDATestCase):

    def setUp(self):
        self.current_version = version()
        set_version(XMCDA_3_1_1)

    def tearDown(self):
        set_version(self.current_version)

    def _test_read_write_xml(self, xmcda_file, _type=XMCDA, tags=()):
        self.maxDiff = None
        from .utils import compact_xml, utf8_to_utf8
        with open(xmcda_file, 'r') as f:
            source = f.read()
        source = compact_xml(source)
        result = utf8_to_utf8(source, _type, tags=tags)
        self.assertEqual(source, result)

    def test_alternativesValues(self):
        self._test_read_write_xml('tests/files/v3/alternativesValues.xml',
                                  tags=('alternativesValues',))

    def test_criteriaValues(self):
        self._test_read_write_xml('tests/files/v3/criteriaValues.xml',
                                  tags=('criteriaValues',))

    def test_alternativesSets(self):
        self._test_read_write_xml('tests/files/v3/alternativesSets.xml',
                                  tags=('alternativesSets',))

    def test_criteriaSets(self):
        self._test_read_write_xml('tests/files/v3/criteriaSets.xml',
                                  tags=('criteriaSets',))

    def test_alternativesMatrix(self):
        self._test_read_write_xml('tests/files/v3/alternativesMatrix.xml',
                                  tags=('alternativesMatrix',))

    def test_criteriaMatrix(self):
        self._test_read_write_xml('tests/files/v3/criteriaMatrix.xml',
                                  tags=('criteriaMatrix',))

    def test_categoriesMatrix(self):
        self._test_read_write_xml('tests/files/v3/categoriesMatrix.xml',
                                  tags=('categoriesMatrix',))

    def test_criteriaHierarchy(self):
        self._test_read_write_xml('tests/files/v3/criteriaHierarchy.xml',
                                  tags=('criteriaHierarchy',))

    def test_criteriaSetsHierarchy(self):
        self._test_read_write_xml('tests/files/v3/criteriaSetsHierarchy.xml',
                                  tags=('criteriaSetsHierarchy',))

    def test_criteriaSetsValues(self):
        self._test_read_write_xml('tests/files/v3/criteriaSetsValues.xml',
                                  tags=('criteria', 'criteriaSets',
                                        'criteriaSetsValues'))

    def test_alternativesSetsValues(self):
        self._test_read_write_xml('tests/files/v3/alternativesSetsValues.xml',
                                  tags=('alternatives',
                                        'alternativesSets',
                                        'alternativesSetsValues'))

    def test_categoriesSetsValues(self):
        self._test_read_write_xml('tests/files/v3/categoriesSetsValues.xml',
                                  tags=('categories', 'categoriesSets',
                                        'categoriesSetsValues'))

    def test_criteriaFunctions(self):
        self._test_read_write_xml('tests/files/v3/criteriaFunctions.xml',
                                  tags=('criteriaFunctions',))

    def test_criteriaThresholds(self):
        self._test_read_write_xml('tests/files/v3/criteriaThresholds.xml',
                                  tags=('criteriaThresholds',))

# à la place de element.findall('./criterionValue')
# element.xpath('./*[local-name()="criterionValue"]'
