import xmcda

from . import utils
from .criteria_sets import CriteriaSets
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext


class Node(list):

    @staticmethod
    def read_nodes(element, xmcda=None):
        '''merge a <nodes/> XML element'''
        nodes = []
        for xml_node in xfindall(element, './node'):
            nodes.append(Node(xml_node, xmcda))
        return nodes

    def __init__(self, xml_element, xmcda):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)

    def merge_xml(self, element, xmcda=None):
        criteria_sets = (
            xmcda.criteria_sets if xmcda is not None
            else CriteriaSets())

        criteriaSetID = xfindtext(element, './criteriaSetID')
        if criteriaSetID is not None:
            self.criteria_set = criteria_sets[criteriaSetID]

        nodes = xfind(element, './nodes')
        if nodes is not None:
            self.extend(self.read_nodes(nodes, xmcda))

    def to_xml(self):
        E = utils.element_maker()

        children = []
        criteria_set_id = (
            self.criteria_set.id if self.criteria_set is not None else None
        )
        # criteria_set_id is not None: to_xml() is not called on the
        # hierarchies themselves but on their children, where a
        # criteriaSetID is mandatory
        children.append(E.criteriaSetID(criteria_set_id))

        nodes = []
        for node in self:
            nodes.append(node.to_xml())

        if nodes:
            children.append(E.nodes(*nodes))
        return E.node(*children)


class CriteriaSetsHierarchy(Node, CommonAttributes, HasDescription):
    '''
    list of root nodes
    '''
    nodes = None
    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaSetsHierarchy',
                             'criteria_sets_hierarchy_list', cls,
                             CriteriaSetsHierarchy)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        super().__init__(None, None)
        self.nodes = []
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        super().merge_xml(element, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        criteria_sets_hierarchy = E.criteriaSetsHierarchy(**attributes)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())

        nodes = []
        for node in self:
            nodes.append(node.to_xml())
        args.append(E.nodes(*nodes))

        criteria_sets_hierarchy = E.criteriaSetsHierarchy(*args, **attributes)
        return criteria_sets_hierarchy
