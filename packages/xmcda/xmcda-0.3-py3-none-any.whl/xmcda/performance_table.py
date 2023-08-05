from xmcda import TagInfo

from . import utils
from .alternatives import Alternative, Alternatives
from .criteria import Criteria, Criterion
from .mixins import CommonAttributes, HasDescription
from .utils import xfind, xfindall
from .value import Values


class Row(dict):
    'ligne de criterion: value'
    def __getitem__(self, criterion):
        if isinstance(criterion, str):
            try:
                criterion = next(filter(lambda c: c.id == criterion, self))
            except StopIteration:
                raise KeyError("Unknown criterion with id: %s" % criterion)

        _value = super().__getitem__(criterion)
        if _value is not None and len(_value) == 1:
            return _value[0].v
        return _value

    def __delitem__(self, criterion):
        if isinstance(criterion, str):  # criterion identified by its id
            try:
                criterion = next(filter(lambda c: c.id == criterion, self))
            except StopIteration:
                raise KeyError("Unknown criterion with id: %s" % criterion)

        super().__delitem__(criterion)

    def __setitem__(self, criterion, value):
        ''
        if value is None:
            value = Values()
        if isinstance(criterion, str):  # search by id
            try:
                criterion = next(filter(lambda c: c.id == criterion, self))
            except StopIteration:
                raise KeyError(f"Unknown criterion with id: {criterion}")
        elif not isinstance(criterion, Criterion):
            # for p[a][c] behave like PerfTable.__getitem__(): raise
            # KeyError if this is neither a string or a criterion
            raise KeyError(f"Invalid criterion: {criterion}")

        if type(value) is Values:
            return super().__setitem__(criterion, value)
        return super().__setitem__(criterion, Values(value))

    def to_xml(self):
        '''Builds the list of <performance> xml element for this row.
        '''
        E = utils.element_maker()
        if len(self) == 0:
            return []  # pragma: no cover

        xml_row = []

        for criterion, vs in self.items():
            crit_id = E.criterionID(criterion.id)
            values = vs.to_xml()
            xml_row.append(E.performance(crit_id, values))
        # return liste de performances
        return xml_row


class PerformanceTable(dict, CommonAttributes, HasDescription):

    # Implementation note: the stability of the iteration order on
    # alternatives() and criteria() depends on dict keeping insertion
    # order.

    @classmethod
    def tag_info(cls):
        # contained_class should not be set here, simply to prevent using it:
        # it is useles in this context
        return TagInfo('performanceTable', 'performance_tables', cls,
                       contained_class=None)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def alternatives(self):
        """Returns the alternatives declared in this performance table.

        The iteration order is guaranteed to be stable both in a
        process and between different executions, given that the
        performance is built the same way (aither by loading a XMCDA
        file, bienf programmatically built, etc.).  This is important
        because the result numerical operations based on the
        performance table's content may vary depending on the
        operation order.

        """
        # Implementation note: the stability of the iteration depends on dict
        # keeping insertion order
        return self.keys()

    def criteria(self):
        """Returns the criteria declared in this performance table.

        The iteration order is guaranteed to be stable both in a
        process and between different executions, given that the
        performance is built the same way (aither by loading a XMCDA
        file, bienf programmatically built, etc.).  This is important
        because the result numerical operations based on the
        performance table's content may vary depending on the
        operation order.

        """
        # Implementation note: the stability of the iteration depends on dict
        # keeping insertion order
        criteria = []
        for row in self.values():
            [criteria.append(c) for c in row.keys() if c not in criteria]
        return tuple(criteria)

    def get(self, alternative, criterion):
        '''Return the values associated to the altnative and criterion.
        Raises KeyError'''
        # get completely override dict.get(): get(key, default) has no
        # meaning for a performance table
        if alternative not in self:
            raise KeyError(alternative, criterion)

        row = super().get(alternative)
        if criterion not in row:
            raise KeyError(alternative, criterion)
        return row.get(criterion)

    def set(self, alternative, criterion, value):
        _row = self.setdefault(alternative, Row())
        _row[criterion] = value  # CHECK Values!?!

    def __getitem__(self, attr):
        if isinstance(attr, Alternative):
            return super().setdefault(attr, Row())
        if isinstance(attr, str):  # search by id
            try:
                alt = next(filter(lambda a: a.id == attr, self))
                return super().setdefault(alt, Row())
            except StopIteration:
                raise KeyError("Unknown alternative with id: %s" % attr)
        raise KeyError(f"Invalid alternative: ({attr})")

    @staticmethod
    def build(element, xmcda=None):
        p = PerformanceTable()
        p.merge_xml(element, xmcda)
        return p

    def as_float(self):
        for a in self.alternatives():
            for v in self[a].values():
                v.as_float()

    def has_missing_values(self):
        _len = 0
        for a in self.alternatives():
            # do not create anything: use dict.__getitem__ instead of self's
            _len += len(dict.__getitem__(self, a))
        return _len != len(self.alternatives()) * len(self.criteria())

    def is_numeric(self, strict=False):
        '''
        Check if the stored values are (strictly) numeric
        '''
        for a in self.alternatives():
            for v in self[a].values():
                if not v.is_numeric(strict):
                    return False
        return True

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        rows = xfindall(element, 'alternativePerformances')

        if xmcda is not None:
            alternatives = xmcda.alternatives
            criteria = xmcda.criteria
        else:
            alternatives = Alternatives()
            criteria = Criteria()

        for row in rows:
            alternativeID = xfind(row, './alternativeID').text
            alternative = alternatives[alternativeID]

            for column in xfindall(row, './performance'):
                criteriaID = xfind(column, './criterionID').text
                criterion = criteria[criteriaID]

                values = Values(xfind(column, './values'))

                self[alternative][criterion] = values

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)

        args = []
        if self.description is not None:
            args.append(self.description.to_xml())

        for alternative in self.alternatives():
            row = self[alternative]
            if row is None:  # does not happen --just an extra precaution
                continue  # pragma: no cover

            row_xml = row.to_xml()
            if len(row_xml) == 0:
                continue

            alt_id = E.alternativeID(alternative.id)
            _ = E.alternativePerformances(alt_id, *row_xml)
            args.append(_)

        performance_table = E.performanceTable(*args, **d)

        return performance_table
