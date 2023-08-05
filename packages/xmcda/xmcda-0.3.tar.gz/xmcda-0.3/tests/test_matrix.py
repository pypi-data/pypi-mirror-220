from xmcda.mixins.matrix import Matrix

from .utils import XMCDATestCase


class Cell:
    def __init__(self, anID):
        self.id = anID

    def __repr__(self):  # pragma: no cover
        return f'Cell({self.id})'


class TestMatrix(XMCDATestCase):

    def test_matrix(self):
        m = Matrix()
        cells = c1, c2, c3, c4 = [Cell(x) for x in ('c1', 'c2', 'c3', 'c4')]

        for i in range(3):
            for j in range(1, 4):
                m[cells[i]][cells[j]] = f'{i+1}{j+1}'

        # Accessing cells
        self.assertEqual(m[c2][c3], '23')
        self.assertEqual(m['c2'][c3], '23')
        self.assertEqual(m[c2]['c3'], '23')
        self.assertEqual(m['c2']['c3'], '23')

        with self.assertRaises(KeyError):
            m[c2]['unknown']
        with self.assertRaises(KeyError):
            m['unknown']['c2']

        # rows and columns
        self.assertSequenceEqual(list(m.rows()), [c1, c2, c3])
        self.assertSequenceEqual(list(m.columns()), [c2, c3, c4])

        # deleting cells
        del m[c2][c3]
        with self.assertRaises(KeyError):
            m[c2][c3]
        with self.assertRaises(KeyError):
            m[c2]['c3']
        with self.assertRaises(KeyError):
            m['c2'][c3]

        # assigning cella
        def check_23(x, y, delete, assignmentFails):
            if delete:
                try: del m[c2][c3]  # noqa
                except Exception: pass  # noqa
            if assignmentFails:
                with self.assertRaises(ValueError):
                    m[x][y] = '23'
                return
            else:
                m[x][y] = '23'
            self.assertEqual(m[c2][c3], '23')
            self.assertEqual(m[c2][c3], '23')

        check_23(c2, c3, False, False)
        check_23('c2', c3, False, False)
        check_23(c2, 'c3', False, False)
        check_23('c2', 'c3', False, False)

        check_23(c2, c3, True, False)
        check_23('c2', c3, True, False)
        check_23(c2, 'c3', True, True)  # c3 cannot be found
        check_23('c2', 'c3', True, True)  # id.
