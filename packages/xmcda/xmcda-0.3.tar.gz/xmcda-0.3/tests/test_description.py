from xmcda.description import Bibliography, Description

from .utils import XMCDATestCase, compact_xml, utf8_to_utf8


class TestBibliography(XMCDATestCase):

    xml_1 = '''
      <bibliography id="bib id" name="bib name" mcdaConcept="bib mcdaConcept">
          <description>
              <author>bib-desc-author</author>
          </description>
          <bibEntry>bib entry 1</bibEntry>
          <bibEntry>bib entry 2</bibEntry>
          <bibEntry>bib entry 3</bibEntry>
      </bibliography>'''

    def test_init(self):
        bib = Bibliography()

        # Do NOT share the same list!
        self.assertFalse(bib.bib_entries is Bibliography().bib_entries)

    def test_load_xml(self):
        element = self.read_xml(TestBibliography.xml_1)

        bib = Bibliography(element)

        self.assertEqual(bib.id, 'bib id')
        self.assertEqual(bib.name, 'bib name')
        self.assertEqual(bib.mcda_concept, 'bib mcdaConcept')
        self.assertIsNotNone(bib.description)
        self.assertIsInstance(bib.description, Description)
        self.assertEqual(len(bib.bib_entries), 3)

    def test_to_xml(self):
        source = compact_xml(TestBibliography.xml_1)
        result = utf8_to_utf8(TestBibliography.xml_1, Bibliography)
        self.assertEqual(source, result)

    # empty bib
    xml_empty = "<bibliography/>"

    def test_load_xml_empty(self):
        element = self.read_xml(TestBibliography.xml_empty)
        bib = Bibliography(element)
        self.assertIsNone(bib.id)
        self.assertIsNone(bib.name)
        self.assertIsNone(bib.mcda_concept)
        self.assertIsNone(bib.description)

    def test_to_xml_empty(self):
        source = compact_xml(TestBibliography.xml_empty)
        result = utf8_to_utf8(TestBibliography.xml_empty, Bibliography)
        self.assertEqual(source, result)


class TestDescription(XMCDATestCase):

    xml_1 = '''
<description>
        <author>desc author</author>
        <comment>alternatives1 comment</comment>
        <keyword>kw1</keyword>
        <keyword>kw2</keyword>
        <keyword>kw3</keyword>
        <bibliography id="db id" name="db name" mcdaConcept="db mcdaConcept">
                <description>
                        <author>desc-bib-desc-author</author>
                </description>
                <bibEntry>bib entry 1</bibEntry>
                <bibEntry>bib entry 2</bibEntry>
                <bibEntry>bib entry 3</bibEntry>
        </bibliography>
        <creationDate>2013-09-05T15:50:12+02:00</creationDate>
        <lastModificationDate>2014-09-05T15:50:33+02:00</lastModificationDate>
</description>
'''

    def test_init(self):
        desc = Description()
        self.assertEqual(len(desc.authors), 0)
        self.assertIsNone(desc.comment)
        self.assertEqual(len(desc.keywords), 0)
        self.assertIsNone(desc.bibliography, 0)
        self.assertIsNone(desc.creation_date)
        self.assertIsNone(desc.last_modification_date)

    def test_load_xml(self):
        xml = self.read_xml(TestDescription.xml_1)

        desc = Description(xml)

        self.assertEqual(len(desc.authors), 1)
        self.assertEqual(desc.authors[0], 'desc author')
        self.assertEqual(desc.comment, 'alternatives1 comment')
        self.assertTrue(len(desc.keywords) == 3 and 'kw1' in desc.keywords
                        and 'kw2' in desc.keywords and 'kw3' in desc.keywords)
        self.assertIsNotNone(desc.bibliography)
        self.assertEqual(desc.bibliography.id, 'db id')
        self.assertEqual(desc.bibliography.name, 'db name')
        self.assertEqual(desc.bibliography.mcda_concept, 'db mcdaConcept')
        self.assertIsNotNone(desc.bibliography.description)
        self.assertEqual(desc.bibliography.description.authors[0],
                         'desc-bib-desc-author')
        self.assertEqual(3, len(desc.bibliography.bib_entries))
        self.assertIsNotNone(desc.creation_date)
        self.assertEqual(desc.creation_date.year, 2013)
        self.assertIsNotNone(desc.last_modification_date)
        self.assertEqual(desc.last_modification_date.year, 2014)

    def test_to_xml(self):
        source = compact_xml(TestDescription.xml_1)
        result = utf8_to_utf8(TestDescription.xml_1, Description)
        self.assertEqual(source, result)
