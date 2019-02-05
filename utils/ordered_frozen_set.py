from collections import defaultdict


class OrderedFrozenSet(object):
    """
    FrozenSet with all elements stored in inserted order
    """

    def __init__(self, iterable=None):
        super().__init__()
        self._insert_list = []
        self._value_vis_set = set()
        iterable = iterable if iterable else []
        for value in iterable:
            if value not in self._value_vis_set:
                self._value_vis_set.add(value)
                self._insert_list.append(value)

    def copy(self):
        return OrderedFrozenSet(self)

    def difference(self, s):
        new_insert_list = []
        for value in self._insert_list:
            if value not in s:
                new_insert_list.append(value)
        return OrderedFrozenSet(new_insert_list)

    def intersection(self, s):
        new_insert_list = []
        for value in self._insert_list:
            if value in s:
                new_insert_list.append(value)
        return OrderedFrozenSet(new_insert_list)

    def isdisjoint(self, s):
        return len(self.intersection(s)) == 0

    def issubset(self, s):
        return len(self.intersection(s)) == len(self)

    def issuperset(self, s):
        return len(self.intersection(s)) == len(s)

    def symmetric_difference(self, s):
        new_insert_list = []
        cnt_map = defaultdict(int)
        for value in list(self) + list(s):
            cnt_map[value] += 1
        for value in list(self) + list(s):
            if cnt_map[value] == 1:
                new_insert_list.append(value)
        return OrderedFrozenSet(new_insert_list)

    def union(self, s):
        vis = set()
        new_insert_list = []
        for value in list(self) + list(s):
            if value not in vis:
                vis.add(value)
                new_insert_list.append(value)
        return OrderedFrozenSet(new_insert_list)

    def __iter__(self):
        return iter(self._insert_list)

    def __reversed__(self):
        return reversed(self._insert_list)

    def __and__(self, s):
        return self.intersection(s)

    def __contains__(self, y):
        return y in self._value_vis_set

    def __eq__(self, s):
        if not hasattr(s, "__len__") or len(self) == len(s):
            if isinstance(s, OrderedFrozenSet):
                return list(self) == list(s)
            else:
                return set(self) == set(s)
        else:
            return False

    def __ge__(self, s):
        return self.issuperset(s)

    def __gt__(self, s):
        return self.issuperset(s) and len(self) > len(s)

    def __hash__(self):
        # TODO very naive hash strategy now, rolling hash. Maybe something like murmurhash is a better choice?
        hash_result = 31
        for value in self._insert_list:
            hash_result = (hash_result * 43 + hash(value)) % 1000000007
        return hash_result

    def __len__(self):
        return len(self._insert_list)

    def __le__(self, s):
        return self.issubset(s)

    def __lt__(self, s):
        return self.issubset(s) and len(self) < len(s)

    # TODO
    # def __new__(*args, **kwargs):  pass

    # TODO
    # def __reduce__(self): pass

    def __ne__(self, s):
        return not (self == s)

    def __or__(self, s):
        return self.union(s)

    def __rand__(self, s):
        return s & self

    def __repr__(self):
        if self._insert_list:
            return "{%s}" % (", ".join(map(lambda item: str(item), self._insert_list)))
        else:
            return "%s()" % (self.__class__.__name__,)

    def __str__(self):
        return self.__repr__()

    def __ror__(self, s):
        return s | self

    def __rsub__(self, s):
        return s - self

    def __rxor__(self, s):
        return s ^ self

    def __sizeof__(self):
        # add two data structure's size together
        return self._value_vis_set.__sizeof__() + self._insert_list.__sizeof__()

    def __sub__(self, s):
        return self.difference(s)

    def __xor__(self, s):
        return self.symmetric_difference(s)
