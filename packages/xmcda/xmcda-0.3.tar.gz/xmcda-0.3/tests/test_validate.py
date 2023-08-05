# -*- coding: utf-8 -*-
import warnings

import pytest
from lxml import etree

from xmcda import schemas

_v3dir = "tests/files/v3"
_v4dir = "tests/files/v4"


files_schemas = (
    (f"{_v3dir}/sample-xmcda-3.1.1.xml", schemas.XMCDA_3_1_1),
    (f"{_v4dir}/alternativesValues.xml", schemas.XMCDA_4_0_0),
)


def _read(source):
    return etree.parse(source)


@pytest.mark.parametrize("a_file, a_schema", files_schemas)
def test__validate_against_a_specific_schema(a_file, a_schema):
    xmcda = _read(open(a_file, "rb"))
    ret, error = schemas._validate(xmcda, a_schema)
    assert ret, error


@pytest.mark.parametrize("a_file, a_schema", files_schemas)
def test_validate_against_a_specific_schema(a_file, a_schema):
    xmcda = _read(open(a_file, "rb"))
    assert schemas.validate(xmcda, a_schema)


@pytest.mark.parametrize("a_file, a_schema", files_schemas)
def test_validateXMCDA_against_a_specific_schema(a_file, a_schema):
    xmcda = _read(open(a_file, "rb"))
    with warnings.catch_warnings(record=True) as w:
        assert schemas.validateXMCDA(xmcda, a_schema)
        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated" in str(w[-1].message)


@pytest.mark.parametrize("a_file, a_schema", files_schemas)
def test_validate(a_file, a_schema):
    xmcda = _read(open(a_file, "rb"))
    assert schemas.validate(xmcda)


def test_validate_invalid():
    invalid = _read(open(f"{_v3dir}/sample-invalid-XMCDA.xml", "rb"))
    assert not schemas.validate(invalid, schemas.XMCDA_3_xsds)
    invalid = _read(open(f"{_v4dir}/invalid.xml", "rb"))
    assert not schemas.validate(invalid, schemas.XMCDA_4_xsds)
