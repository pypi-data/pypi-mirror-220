import pkgutil
from collections import namedtuple
from io import BytesIO
from warnings import warn

from lxml import etree

XMCDASchema = namedtuple('XMCDASchema', 'id url resource root_tag major')

__base_url = 'http://www.decision-deck.org/xmcda/_downloads'
XMCDA_3_0_0 = XMCDASchema('http://www.decision-deck.org/2013/XMCDA-3.0.0',
                          f'{__base_url}/XMCDA-3.0.0.xsd',
                          'xsd/XMCDA-3.0.0.xsd',
                          "XMCDA",
                          3)

XMCDA_3_0_1 = XMCDASchema('http://www.decision-deck.org/2016/XMCDA-3.0.1',
                          f'{__base_url}/XMCDA-3.0.1.xsd',
                          'xsd/XMCDA-3.0.1.xsd',
                          "XMCDA",
                          3)

XMCDA_3_0_2 = XMCDASchema('http://www.decision-deck.org/2018/XMCDA-3.0.2',
                          f'{__base_url}/XMCDA-3.0.2.xsd',
                          'xsd/XMCDA-3.0.2.xsd',
                          "XMCDA",
                          3)

XMCDA_3_1_0 = XMCDASchema('http://www.decision-deck.org/2018/XMCDA-3.1.0',
                          f'{__base_url}/XMCDA-3.1.0.xsd',
                          'xsd/XMCDA-3.1.0.xsd',
                          "XMCDA",
                          3)

XMCDA_3_1_1 = XMCDASchema('http://www.decision-deck.org/2019/XMCDA-3.1.1',
                          f'{__base_url}/XMCDA-3.1.1.xsd',
                          'xsd/XMCDA-3.1.1.xsd',
                          "XMCDA",
                          3)

XMCDA_4_0_0 = XMCDASchema('http://www.decision-deck.org/2021/XMCDA-4.0.0',
                          f'{__base_url}/XMCDA-4.0.0.xsd',
                          'xsd/XMCDA-4.0.0.xsd',
                          "xmcda",
                          4)
del __base_url


XMCDA_3_xsds = (
    XMCDA_3_1_1, XMCDA_3_1_0, XMCDA_3_0_2, XMCDA_3_0_1, XMCDA_3_0_0
)
XMCDA_4_xsds = (XMCDA_4_0_0,)
XMCDA_xsds = XMCDA_3_xsds + XMCDA_4_xsds


def _validate(xml, xmcda_schema):
    '''Helper method for validate().

    Validates a xml with the supplied XMCDASchema
    - xml: either an ElementTree or an Element object
    - xmcda_schema: a XMCDASchema object
    '''
    xsd = BytesIO(pkgutil.get_data('xmcda', xmcda_schema.resource))
    xmlschema_doc = etree.parse(xsd, etree.XMLParser(no_network=True))
    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema.validate(xml), xmlschema.error_log


def validate(xml, xmcda_schemas=XMCDA_xsds):
    '''Validates a xml against a set of XMCDA schemas

    - xml: either an ElementTree or an Element object.
    - xmcda_schemas: the schema or schemas against with the xml is
      validated. If omitted, the xml is validated against XMCDA v4
      schemas.
    '''
    if isinstance(xmcda_schemas, XMCDASchema):
        xmcda_schemas = (xmcda_schemas,)
    for xml_schema in xmcda_schemas:
        if _validate(xml, xml_schema)[0]:
            return True
    return False


def validateXMCDA(xml, xmcda_schemas=XMCDA_4_xsds):
    warn("validateXMCDA is deprecated, use validate() instead",
         DeprecationWarning, 2)
    return validate(xml, xmcda_schemas)


class AllTags:
    # all your tag are belong to us
    def __contains__(self, item):
        return True


ROOT_TAGS = ('alternatives',
             'alternativesSets',
             'criteria',
             'criteriaSets',
             'categories',
             'categoriesSets',

             'performanceTable',

             # data linked to alternatives

             'alternativesValues',
             'alternativesSetsValues',
             'alternativesLinearConstraints',
             'alternativesSetsLinearConstraints',
             'alternativesMatrix',
             'alternativesSetsMatrix',

             # data linked to criteria

             'criteriaFunctions',
             'criteriaScales',
             'criteriaThresholds',
             'criteriaValues',
             'criteriaSetsValues',
             'criteriaLinearConstraints',
             'criteriaSetsLinearConstraints',
             'criteriaMatrix',
             'criteriaSetsMatrix',

             # data linked to alternatives and criteria

             'alternativesCriteriaValues',

             # data linked to categories

             'categoriesProfiles',
             'alternativesAssignments',
             'categoriesValues',
             'categoriesSetsValues',
             'categoriesLinearConstraints',
             'categoriesSetsLinearConstraints',
             'categoriesMatrix',
             'categoriesSetsMatrix',

             # data linked to algorithms

             'programParameters',
             'programExecutionResult',
             )
