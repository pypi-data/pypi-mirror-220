from xmcda import TagInfo

from . import utils
from .categories import Categories
from .mixins import CommonAttributes, HasDescription
from .mixins.matrix import Matrix
from .utils import xfind, xfindall, xfindtext
from .value import Values


class CategoriesMatrix(Matrix, CommonAttributes, HasDescription):

    @classmethod
    def tag_info(cls):
        return TagInfo('categoriesMatrix', 'categories_matrix_list',
                       cls, None)

    def __init__(self, xml_element=None, xmcda=None, **kw):
        if xml_element is not None:
            self.merge_xml(xml_element, xmcda)
        for k, v in kw.items():
            setattr(self, k, v)

    def get_category(self, category_id):
        """Returns the category defined in this matrix (either in a row or a
        column).

        """
        categories = (
            o for s in (self.rows(), self.columns()) for o in s
            if o.id == category_id
        )
        try:
            return next(categories)
        except StopIteration:
            return None

    def merge_xml(self, element, xmcda=None):
        CommonAttributes.merge_xml(self, element)
        HasDescription.merge_xml(self, element)

        categories = (
            xmcda.categories if xmcda is not None
            else Categories())

        for row in xfindall(element, './row'):
            row_alt = categories[xfindtext(row, 'categoryID')]
            for column in xfindall(row, './column'):
                column_alt = categories[xfindtext(column, 'categoryID')]
                v_xml = xfind(column, './values')
                v = Values(v_xml) if v_xml is not None else None
                self[row_alt][column_alt] = v

    def to_xml(self):
        E = utils.element_maker()
        d = utils.CommonAttributes_as_dict(self)
        args = []
        if self.description is not None:
            args.append(self.description.to_xml())

        for row in self.keys():
            row_xml = E.row(E.categoryID(row.id))
            cols_xml = []
            for column in self[row]:
                values = self[row][column].to_xml()
                column_xml = E.column()
                column_xml.append(E.categoryID(column.id))
                column_xml.append(values)
                cols_xml.append(column_xml)
            row_xml.extend(cols_xml)
            args.append(row_xml)

        matrix = E.categoriesMatrix(*args, **d)
        return matrix
