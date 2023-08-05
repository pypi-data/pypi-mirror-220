class Set(dict):
    """This superclass of AlternativesSet, CriteriaSet and CategoriesSet
    maps its element to values.

    """
    def add(self, key, values=None):
        from ..value import Values
        if not isinstance(values, Values):
            values = Values(values)
        self[key] = values

    def get_element(self, element_id):
        try:
            return next(filter(lambda x: x.id == element_id, self))
        except StopIteration:
            return None

    def __getitem__(self, key):
        """Returns the value associated to the key.

        If the key is a string, the returned value is the one
        associate to the element of the set satisfying
        element.id==key, if it exists.

        """
        if isinstance(key, str):
            element = self.get_element(key)
            if element is None:
                raise KeyError
            return self[element]
        else:
            return super().__getitem__(key)

    def __setitem__(self, key, value):
        """
        Assigns a value to the element key.
        """
        from ..value import Values
        if value is not None and not isinstance(value, Values):
            value = Values(value)
        if isinstance(key, str):
            element = self.get_element(key)
            if element is None:
                raise KeyError(f'No element with id={key}')
            self[element] = value
            return

        if not isinstance(key, type(self)._element_klass):
            raise TypeError(f'Expected: {type(self)._element_klass.__name__}, '
                            f'got: {type(key).__name__}')
        else:
            return super().__setitem__(key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            element = self.get_element(key)
            if element is None:
                raise KeyError(f'No element with id={key}')
            del self[element]
        else:
            super().__delitem__(key)
    remove = __delitem__

    def __eq__(self, aSet):
        return id(self) == id(aSet)

    def __ne__(self, aSet):
        return id(self) != id(aSet)
