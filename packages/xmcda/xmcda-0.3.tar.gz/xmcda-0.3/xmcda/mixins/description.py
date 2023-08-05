from ..utils import xfind


class HasDescription:

    description = None

    def merge_xml(self, element):
        description = xfind(element, 'description')
        if description is not None:
            from ..description import Description
            self.description = Description(description)
