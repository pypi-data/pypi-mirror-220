from collections import OrderedDict


class Matrix(OrderedDict):
    '''Matrix of common attributes'''

    def __init__(self):
        pass

    def rows(self):
        return self.keys()

    def columns(self):
        columns = []
        for column in self.values():
            [columns.append(item) for item in column.keys()
             if item not in columns]
        return columns

    def __getitem__(self, item):
        if type(item) is str:
            item = self._get_item(item)
            if item is None:
                raise KeyError
        try:
            return super().__getitem__(item)
        except KeyError:
            self[item] = MatrixColumn()
            return self[item]

    def _get_item(self, row_id):
        for r in self.keys():
            if r.id == row_id:
                return r
        return None


class MatrixColumn(OrderedDict):

    def __getitem__(self, item):
        if type(item) is str:
            item = self._get_item(item)
            if item is None:
                raise KeyError
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        if type(key) is str:
            key = self._get_item(key)
        if key is None:
            raise ValueError("Error, no such cell with key {value}")
        super().__setitem__(key, value)

    def _get_item(self, _id):
        for c in self.keys():
            if c.id == _id:
                return c
        return None
