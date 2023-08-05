import os

from lxml import etree

from . import ValidationError, schemas, set_version, utils, version
from .alternatives import Alternatives
from .alternatives_assignments import AlternativesAssignments
from .alternatives_matrix import AlternativesMatrix
from .alternatives_sets import AlternativesSets
from .alternatives_sets_values import AlternativesSetsValues
from .alternatives_values import AlternativesValues
from .categories import Categories
from .categories_matrix import CategoriesMatrix
from .categories_profiles import CategoriesProfiles
from .categories_sets import CategoriesSets
from .categories_sets_values import CategoriesSetsValues
from .categories_values import CategoriesValues
from .criteria import Criteria
from .criteria_functions import CriteriaFunctions
from .criteria_hierarchy import CriteriaHierarchy
from .criteria_matrix import CriteriaMatrix
from .criteria_scales import CriteriaScales
from .criteria_sets import CriteriaSets
from .criteria_sets_hierarchy import CriteriaSetsHierarchy
from .criteria_sets_values import CriteriaSetsValues
from .criteria_thresholds import CriteriaThresholds
from .criteria_values import CriteriaValues
from .performance_table import PerformanceTable
from .program_execution_result import ProgramExecutionResult
from .program_parameters import ProgramParameters
from .utils import xfind, xfindall


def _get_tag(e):
    # the string, the class'tag_info.tag() is there is one,
    # or the class' name
    if type(e) is str:
        return e
    tag_info = getattr(e, 'tag_info', None)
    return tag_info().tag if tag_info is not None else e.__name__


def load(source, *, tags=(), validate=True):
    xmcda = XMCDA()
    return xmcda.load(source, tags=tags, validate=validate)


def fromstring(text, *, tags=(), validate=True):
    xmcda = XMCDA()
    return xmcda.fromstring(text, tags=tags, validate=validate)


class XMCDA:

    def __init__(self):
        self.alternatives = Alternatives()
        self.alternatives_sets = AlternativesSets()
        self.criteria = Criteria()
        self.criteria_sets = CriteriaSets()
        self.performance_tables = []
        self.categories = Categories()
        self.categories_sets = CategoriesSets()

        self.alternatives_assignments_list = []
        self.alternatives_matrix_list = []
        self.alternatives_values_list = []

        self.alternatives_sets_values_list = []

        self.criteria_functions_list = []
        self.criteria_hierarchy_list = []
        self.criteria_matrix_list = []
        self.criteria_scales_list = []
        self.criteria_thresholds_list = []
        self.criteria_values_list = []

        self.criteria_sets_hierarchy_list = []
        self.criteria_sets_values_list = []

        self.categories_matrix_list = []
        self.categories_profiles_list = []
        self.categories_values_list = []

        self.categories_sets_values_list = []

        self.program_parameters_list = []
        self.program_execution_results = []

    def merge_xml(self, element, tags=()):
        if type(tags) in (list, tuple) and len(tags) == 0:
            tags = schemas.AllTags()
        elif type(tags) is str:
            tags = (tags,)
        else:
            if type(tags) not in (list, tuple):
                tags = (tags,)

            tags = [_get_tag(e) for e in tags]

        def handle_element(klass, element=element, tags=tags):
            tag = klass.tag_info().tag
            if tag not in tags:
                return
            xml = xfind(element, tag)
            if xml is None:
                return
            xmcda_elements = getattr(self, klass.tag_info().attribute)
            xmcda_elements.merge_xml(xml)
            # later, if for some reason there is no no merge_xml(), we could
            # xmcda_elements.extend(klass(xml, xmcda=self))

        def handle_elements(klass, element=element, tags=tags):
            tag = klass.tag_info().tag
            if tag not in tags:
                return
            xmls = xfindall(element, tag)
            if xmls is None or len(xmls) == 0:
                return
            xmcda_elements = getattr(self, klass.tag_info().attribute)
            for xml in xmls:
                xmcda_elements.append(klass(xml, xmcda=self))

        handle_element(Alternatives)
        handle_element(AlternativesSets)
        handle_element(Criteria)
        handle_element(CriteriaSets)
        handle_elements(PerformanceTable)
        handle_element(Categories)
        handle_element(CategoriesSets)

        handle_elements(AlternativesAssignments)
        handle_elements(AlternativesMatrix)
        handle_elements(AlternativesValues)

        handle_elements(AlternativesSetsValues)

        handle_elements(CriteriaFunctions)
        handle_elements(CriteriaHierarchy)
        handle_elements(CriteriaMatrix)
        handle_elements(CriteriaValues)
        handle_elements(CriteriaScales)
        handle_elements(CriteriaThresholds)
        handle_elements(CriteriaSetsHierarchy)
        handle_elements(CriteriaSetsValues)

        handle_elements(CategoriesMatrix)
        handle_elements(CategoriesProfiles)
        handle_elements(CategoriesValues)

        handle_elements(CategoriesSetsValues)

        handle_elements(ProgramParameters)
        handle_elements(ProgramExecutionResult)

    def to_xml(self, schema=None, tags=()):
        if schema is None:
            schema = version()
        current = version()
        try:
            set_version(schema)
            return self._to_xml(schema, tags)
        finally:
            set_version(current)

    def _to_xml(self, schema, tags=()):
        args = []
        if type(tags) in (list, tuple) and len(tags) == 0:
            tags = schemas.AllTags()
        elif type(tags) is str:
            tags = (tags,)
        else:
            if type(tags) not in (list, tuple):
                tags = (tags,)
            tags = [_get_tag(e) for e in tags]

        def add_tag(tagname, tag, args=args, only_tags=tags):
            if tagname not in only_tags or tag is None:
                return
            if not isinstance(tag, list):
                # it is not a container, like program execution result
                args.append(tag.to_xml())
            elif len(tag) != 0:
                # it is a container, like criteria: do not write an empty tag
                args.append(tag.to_xml())

        def add_tags(tagname, tags, args=args, only_tags=tags):
            for tag in tags:
                add_tag(tagname, tag, args, only_tags)

        add_tag('alternatives', self.alternatives)
        add_tag('alternativesSets', self.alternatives_sets)
        add_tag('criteria', self.criteria)
        add_tag('criteriaSets', self.criteria_sets)
        add_tags('performanceTable', self.performance_tables)
        add_tag('categories', self.categories)
        add_tag('categoriesSets', self.categories_sets)

        add_tags('alternativesAssignments', self.alternatives_assignments_list)
        add_tags('alternativesMatrix', self.alternatives_matrix_list)
        add_tags('alternativesValues', self.alternatives_values_list)

        add_tags('alternativesSetsValues', self.alternatives_sets_values_list)

        add_tags('criteriaFunctions', self.criteria_functions_list)
        add_tags('criteriaHierarchy', self.criteria_hierarchy_list)
        add_tags('criteriaMatrix', self.criteria_matrix_list)
        add_tags('criteriaScales', self.criteria_scales_list)
        add_tags('criteriaThresholds', self.criteria_thresholds_list)
        add_tags('criteriaValues', self.criteria_values_list)

        add_tags('criteriaSetsHierarchy', self.criteria_sets_hierarchy_list)
        add_tags('criteriaSetsValues', self.criteria_sets_values_list)

        add_tags('categoriesMatrix', self.categories_matrix_list)
        add_tags('categoriesProfiles', self.categories_profiles_list)
        add_tags('categoriesValues', self.categories_values_list)

        add_tags('categoriesSetsValues', self.categories_sets_values_list)

        add_tags('programParameters', self.program_parameters_list)
        add_tags('programExecutionResult', self.program_execution_results)

        xmcda = getattr(utils.element_maker(schema), schema.root_tag)(*args)
        return xmcda

    def load(self, source, *, tags=(), validate=True):
        '''Loads and merges the content of a XMCDA source.

        :param source: a filename, a path, a file or a file-like object

        :param tags: if it is not empty, only the content
          corresponding to the supplied main tags is taken into
          account.  The tags can be either plain strings
          (e.g. 'alternatives") or classes (such as:
          xmcda.PerformanceTable)

        '''
        if source is None:
            raise ValueError("The 'file' cannot be None")  # noqa
        close_source = False
        if isinstance(source, os.PathLike):
            # lxml does not support Path-like objects
            source = open(source, 'rb')
            close_source = True
        try:
            elt_tree = etree.parse(source)
        finally:
            if close_source:
                source.close()
        if validate and not schemas.validate(elt_tree):
            raise ValidationError("Invalid XMCDA")
        self.merge_xml(elt_tree.getroot(), tags)
        return self

    def fromstring(self, text, *, tags=(), validate=True):
        '''Parses and merges an XMCDA document from a string.
        '''
        if text is None:
            raise ValueError("text cannot be None")  # noqa
        _x = etree.fromstring(text)
        if validate and not schemas.validate(_x):
            raise ValidationError("Invalid XMCDA")
        self.merge_xml(_x, tags)
        return self

    def write(self, binary_stream,
              xml_declaration=True, pretty_print=True,
              tags=(), schema=None):
        if schema is None:
            schema = version()
        if type(tags) is str:
            tags = (tags,)
        binary_stream.write(
            utils.tobytes(
                self.to_xml(tags=tags, schema=schema),
                xml_declaration=xml_declaration,
                pretty_print=pretty_print)
        )
