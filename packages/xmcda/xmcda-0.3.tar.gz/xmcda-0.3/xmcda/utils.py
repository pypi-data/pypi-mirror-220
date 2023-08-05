from lxml import etree
from lxml.builder import ElementMaker as EM
from lxml.etree import QName


def xml_boolean(string):
    return string.lower() in ('true', '1')


def boolean_to_xml(_bool):
    return 'true' if _bool else 'false'


def CommonAttributes_as_dict(obj, suppressNone=True):
    d = {}
    if obj.id is not None or not suppressNone:
        d['id'] = obj.id
    if obj.name is not None or not suppressNone:
        d['name'] = obj.name
    if obj.mcda_concept is not None or not suppressNone:
        d['mcdaConcept'] = obj.mcda_concept
    return d


def element_maker(schema=None):
    if schema is None:
        return EM()
    namespace = schema.id
    if schema.major == 4:
        return EM(namespace=namespace, nsmap={None: namespace})
    return EM(namespace=namespace, nsmap={'xmcda': namespace})


def tostring(element, pretty_print=False):
    # kw: e.g. pretty_print=True, xml_declaration=True, encoding='utf-8'
    # cf. http://lxml.de/api/lxml.etree-module.html#tostring
    # NB: Serialisation to unicode must not request an XML declaration
    return etree.tostring(element,
                          encoding='unicode',
                          xml_declaration=False,
                          pretty_print=pretty_print)


def tobytes(element,
            encoding='utf-8', xml_declaration=True, pretty_print=True):
    return etree.tostring(element,
                          encoding=encoding,
                          xml_declaration=xml_declaration,
                          pretty_print=pretty_print)


def xfind(element, match):
    e = xfindall(element, match)
    return e[0] if len(e) > 0 else None


def xfindall(element, match):
    elts = element.findall(match)
    if len(elts) == 0 and hasattr(element, 'nsmap'):
        # search in the element's namespace
        # we do not use element.xpath() because empty namespace prefix is
        # not supported in XPath, and it may be the case here, i.e.:
        # element.nsmap == {None: a_namespace})
        elts = element.findall(match, namespaces=element.nsmap)
    return elts


def xfindtext(element, match):
    text = element.findtext(match)
    if text is None:
        # Same as in xfindall, above
        text = element.findtext(match, namespaces=element.nsmap)
    return text


def local_name_for_tag(tag):
    return QName(tag).localname
