import xmcda


class Container(list):

    def append(self, x):  # pragma: no cover  too simple
        return super().append(x)

    def extend(self, iterable):  # pragma: no cover  too simple
        return super().extend(iterable)

    def insert(self, x):  # pragma: no cover  too simple
        return super().insert(x)

    def remove(self, x):
        if isinstance(x, str):
            try:
                self.remove(next(filter(lambda o: o.id == x, self)))
            except StopIteration as e:
                raise ValueError("no such element") from e
        else:
            return super().remove(x)

    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return next(filter(lambda x: x.id == key, self))
            except StopIteration as e:
                if not xmcda.create_on_access(self.tag_info().contained_class):
                    raise IndexError from e
                obj = self.tag_info().contained_class(id=key)
                self.append(obj)
                return obj
        else:
            return super().__getitem__(key)

    def __contains__(self, item) -> bool:
        """Tells if `item` is in the container.

        If `item` is a string, an object `o` such as `o.id==item` is searched
        """
        # don't use __getitem__, we do not want to instantiate any object here
        if isinstance(item, str):
            try:
                next(filter(lambda x: x.id == item, self))
                return True
            except StopIteration:
                return False
        else:
            return super().__contains__(item)
