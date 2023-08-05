import xmcda

from . import utils
from .criteria import Criteria, Criterion
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall, xfindtext


class Node(list):

    criterion = None

    @staticmethod
    def read_nodes(element, xmcda=None):
        '''merge a <nodes/> XML element'''
        nodes = []
        for xml_node in xfindall(element, './node'):
            nodes.append(Node(xml_element=xml_node, xmcda=xmcda))
        return nodes

    def __init__(self, criterion=None, xml_element=None, xmcda=None):
        self.criterion = criterion
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)

    def nodes(self):
        yield self
        for node in self:
            yield from node.nodes()

    def get_node(self, criterion):
        '''Return the node for the supplied criterion.  The parameter can be
        either a Criterion, or a criterion's id.
        '''
        for node in self:
            if node.criterion == criterion or node.criterion.id == criterion:
                return node
            try:
                return node.get_node(criterion)
            except ValueError:
                pass
        raise ValueError

    def remove_node(self, criterion):
        '''Traverse the hierarchy and remove the node for the supplied
        criterion.  The parameter can be either a Node, a Criterion, or
        a criterion's id.
        '''
        c = criterion
        for node in self:
            if node == c or node.criterion == c or node.criterion.id == c:
                self.remove(node)
                return
            try:
                node.remove_node(c)
                return
            except ValueError:
                pass
        raise ValueError

    def append(self, node):
        if type(node) is Criterion:
            super().append(Node(criterion=node))
        else:
            super().append(node)

    def remove(self, node):
        if type(node) is Criterion:
            super().remove(Node(criterion=node))
        else:
            super().remove(node)

    def __contains__(self, node):
        if type(node) is Criterion:
            return super().__contains__(Node(node))
        return super().__contains__(node)

    def __eq__(self, node):
        if not isinstance(node, Node):
            return False
        return self.criterion == node.criterion and super().__eq__(node)

    def __ne__(self, node):
        return not self == node

    def __str__(self, show_node=True):
        s = 'Node(' if show_node else ''

        is_hierarchy = self.criterion is None
        s += str(self.criterion) if not is_hierarchy else ''
        if len(self):
            if is_hierarchy:
                s += '['
            else:
                s += ': ['
            for child in self:
                s += child.__str__(show_node=False)+', '
            s = s[:-2] + ']'
        s += ')' if show_node else ''
        return s

    def merge_xml(self, element, xmcda=None):
        criteria = (xmcda.criteria if xmcda is not None
                    else Criteria())

        criterionID = xfindtext(element, './criterionID')
        if criterionID is not None:
            self.criterion = criteria[criterionID]

        nodes = xfind(element, './nodes')
        if nodes is not None:
            self.extend(self.read_nodes(nodes, xmcda))

    def to_xml(self):
        E = utils.element_maker()

        children = []

        criterion_id = (self.criterion.id if self.criterion is not None
                        else None)
        # criterion__id is not None: to_xml() is not called on the
        # hierarchies themselves but on their children, where a
        # criterionID is mandatory
        children.append(E.criterionID(criterion_id))

        nodes = []
        for node in self:
            nodes.append(node.to_xml())

        if nodes:
            children.append(E.nodes(*nodes))
        return E.node(*children)


class CriteriaHierarchy(Node, CommonAttributes, HasDescription):
    '''
    list of root nodes
    '''
    @classmethod
    def tag_info(cls):
        return xmcda.TagInfo('criteriaHierarchy',
                             'criteria_hierarchy_list', cls,
                             CriteriaHierarchy)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def nodes(self):
        '''Return the list of nodes in the hierarchy.  The order of the nodes
        is defined by an depth-first traversal of the hierarchy.
        '''
        for node in self:
            yield from node.nodes()

    def __str__(self):
        s = "CriteriaHierarchy("
        s += f"id='{self.id}', " if self.id is not None else ''
        s += f"name='{self.name}', " if self.name is not None else ''
        s += (
            f"mcda_concept='{self.mcda_concept}', "
            if self.mcda_concept is not None
            else ''
        )
        if len(self):  # pragma: no cover
            s += super().__str__(show_node=False)
        else:
            s += '<empty>'
        s += ')'
        return s

    # XML
    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        super().merge_xml(element, xmcda)

    def to_xml(self):
        E = utils.element_maker()
        attributes = utils.CommonAttributes_as_dict(self)
        criteria_hierarchy = E.criteriaHierarchy(**attributes)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())

        nodes = []
        for node in self:
            nodes.append(node.to_xml())
        args.append(E.nodes(*nodes))

        criteria_hierarchy = E.criteriaHierarchy(*args, **attributes)
        return criteria_hierarchy
