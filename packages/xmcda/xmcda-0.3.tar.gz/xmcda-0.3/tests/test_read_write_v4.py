# -*- coding: utf-8 -*-
import pytest

from xmcda.XMCDA import XMCDA


@pytest.mark.parametrize("load_from_file", (True, False))
class TestWriteXMCDA:
    def _test_read_write_xml(self, xmcda_file, load_from_file, tags=()):
        self.maxDiff = None
        from .utils import compact_xml, file_to_utf8, utf8_to_utf8

        with open(xmcda_file, "r") as f:
            source = f.read()
        source = compact_xml(source)
        if load_from_file:
            result = file_to_utf8(xmcda_file, tags=tags)
        else:
            result = utf8_to_utf8(source, XMCDA, tags=tags)
        assert source == result

    def test_alternativesValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/alternativesValues.xml',
                                  load_from_file, tags=('alternativesValues',))

    def test_criteriaValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/criteriaValues.xml',
                                  load_from_file, tags=('criteriaValues',))

    def test_categoriesValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/categoriesValues.xml',
                                  load_from_file, tags=('categoriesValues',))

    def test_criteriaSetsValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/criteriaSetsValues.xml',
                                  load_from_file,
                                  tags=('criteria', 'criteriaSets',
                                        'criteriaSetsValues'))

    def test_alternativesSetsValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/alternativesSetsValues.xml',
                                  load_from_file,
                                  tags=('alternatives',
                                        'alternativesSets',
                                        'alternativesSetsValues'))

    def test_categoriesSetsValues(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/categoriesSetsValues.xml',
                                  load_from_file,
                                  tags=('categories', 'categoriesSets',
                                        'categoriesSetsValues'))

    def test_criteriaFunctions(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/criteriaFunctions.xml',
                                  load_from_file, tags=('criteriaFunctions',))

    def test_criteriaThresholds(self, load_from_file):
        self._test_read_write_xml('tests/files/v4/criteriaThresholds.xml',
                                  load_from_file, tags=('criteriaThresholds',))

# à la place de element.findall('./criterionValue')
# element.xpath('./*[local-name()="criterionValue"]'
