class CommonAttributes:
    id = name = mcda_concept = None

    def merge_xml(self, element):
        self.id = element.get('id')
        self.name = element.get('name')
        self.mcda_concept = element.get('mcdaConcept')

    @staticmethod
    def get_id(element):
        return element.get('id')
