import dateutil.parser

from . import utils
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext


class Bibliography(CommonAttributes, HasDescription):

    def __init__(self, xml_element=None):
        super().__init__()
        self.bib_entries = []
        if xml_element is not None:
            self.merge_xml(xml_element)

    def merge_xml(self, element):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)
        for bib_entry in xfindall(element, 'bibEntry'):
            self.bib_entries.append(bib_entry.text)

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())
        for bib_entry in self.bib_entries:
            args.append(E.bibEntry(bib_entry))
        return E.bibliography(*args, **d)


class Description:
    authors = []
    comment = None
    keywords = []
    bibliography = None
    creation_date = None
    last_modification_date = None

    def __init__(self, xml_element=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element):
        self.authors = [e.text for e in xfindall(element, 'author')]
        self.comment = xfindtext(element, 'comment')
        self.keywords = [e.text for e in xfindall(element, 'keyword')]
        if xfind(element, 'bibliography') is not None:
            self.bibliography = Bibliography(xfind(element, 'bibliography'))

        # dates: RFC 3339 datetime strings / ISO 8601
        _d = xfind(element, 'creationDate')
        if _d is not None:
            self.creation_date = dateutil.parser.parse(_d.text)

        _d = xfind(element, 'lastModificationDate')
        if _d is not None:
            self.last_modification_date = dateutil.parser.parse(_d.text)

    def to_xml(self):
        E = utils.element_maker()
        args = []
        args.extend([E.author(author) for author in self.authors])

        if self.comment is not None:
            args.append(E.comment(self.comment))

        args.extend([E.keyword(keyword) for keyword in self.keywords])

        if self.bibliography is not None:
            args.append(self.bibliography.to_xml())

        if self.creation_date is not None:
            args.append(E.creationDate(self.creation_date.isoformat()))

        if self.last_modification_date is not None:
            args.append(
                E.lastModificationDate(self.last_modification_date.isoformat())
            )
        return E.description(*args)
