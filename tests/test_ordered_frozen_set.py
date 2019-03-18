import sys
import os
import random

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from ordered_frozen_set import OrderedFrozenSet


def test_set_iter():

    array, vis = [], set()
    for _ in range(1000):
        value = random.randint(1, 1000000)
        while value in vis:
            value = random.randint(1, 1000000)
        vis.add(value)
        array.append(value)
    s = OrderedFrozenSet(array)
    assert list(s) == array


def test_set_rev_iter():

    array, vis = [], set()
    for _ in range(1000):
        value = random.randint(1, 1000000)
        while value in vis:
            value = random.randint(1, 1000000)
        vis.add(value)
        array.append(value)
    s = OrderedFrozenSet(array)
    array.reverse()
    assert list(reversed(s)) == list(array)


def test_ordered_frozen_set_difference():

    set1 = OrderedFrozenSet([1, 2, 3])
    set2 = OrderedFrozenSet([1, 10, 3, 5])
    assert set1.difference(set2) == OrderedFrozenSet([2])
    assert set1 - set2 == OrderedFrozenSet([2])


def test_ordered_frozen_set_intersection():

    set1 = OrderedFrozenSet([1, 10, 4, 2, 3])
    set2 = OrderedFrozenSet([10, 3, 2, 8])
    # same order in set1
    assert set1.intersection(set2) == OrderedFrozenSet([10, 2, 3])
    assert set1 & set2 == OrderedFrozenSet([10, 2, 3])


def test_ordered_frozen_set_union():

    set1 = OrderedFrozenSet([1, 10, 4, 2])
    set2 = OrderedFrozenSet([10, 20, 3, 4])

    assert set1.union(set2) == OrderedFrozenSet([1, 10, 4, 2, 20, 3])
    assert set1 | set2 == OrderedFrozenSet([1, 10, 4, 2, 20, 3])


def test_ordered_frozen_set_symmetric_difference():

    set1 = OrderedFrozenSet([1, 3, 5, 10, 4])
    set2 = OrderedFrozenSet([20, 5, 3, 8])

    assert set1.symmetric_difference(set2) == OrderedFrozenSet([1, 10, 4, 20, 8])
    assert set1 ^ set2 == OrderedFrozenSet([1, 10, 4, 20, 8])


def test_disjoint():

    set1 = OrderedFrozenSet([1, 10, 4])
    set2 = OrderedFrozenSet([9, 3, 2])

    assert set1.isdisjoint(set2)

    set1 = OrderedFrozenSet([1, 10, 3])
    set2 = OrderedFrozenSet([3, 10])

    assert set1.isdisjoint(set2) == False


def test_issubset():

    set1 = OrderedFrozenSet([1, 10, 3])
    set2 = OrderedFrozenSet([1, 10, 3, 4])
    assert set1.issubset(set2)

    set1 = OrderedFrozenSet([1, 5])
    set2 = OrderedFrozenSet([1, 6, 3])
    assert set1.issubset(set2) == False


def test_is_superset():

    set1 = OrderedFrozenSet([1, 10, 4])
    set2 = OrderedFrozenSet([10, 1])
    assert set1.issuperset(set2)

    set1 = OrderedFrozenSet([1, 4, 6])
    set2 = OrderedFrozenSet([4, 8])
    assert set1.issuperset(set2) == False


def test_contains():

    s = OrderedFrozenSet([1, 10, 5, 3])
    value_list = list(s)

    for i in range(1, 11, 1):
        assert (i in s) == (i in value_list)


def test_eq_and_nq():

    s1 = OrderedFrozenSet([1, 10, 3])
    s2 = OrderedFrozenSet([10, 3, 1])
    assert (s1 == s2) == False
    assert (s1 != s2) == True

    s1 = OrderedFrozenSet([1, 10, 2])
    s2 = OrderedFrozenSet([1, 10, 2])
    assert s1 == s2
    assert (s1 != s2) == False


def test_len():

    value_list = []
    for _ in range(10000):
        value_list.append(random.randint(1, 1000000))

    s1 = frozenset(value_list)
    s2 = OrderedFrozenSet(value_list)
    assert len(s1) == len(s2)


def test_hash():

    value_list1 = [1, 10, 3, 4]
    value_list2 = [1, 10, 3, 4]

    s1 = OrderedFrozenSet(value_list1)
    s2 = OrderedFrozenSet(value_list2)
    assert hash(s1) == hash(s2)

    value_list1 = [1, 10, 3]
    value_list2 = [1, 4, 3]

    s1 = OrderedFrozenSet(value_list1)
    s2 = OrderedFrozenSet(value_list2)
    assert hash(s1) != hash(s2)

    value_list1 = [1, 4, 2]
    value_list2 = [1, 2, 4]
    s1 = OrderedFrozenSet(value_list1)
    s2 = OrderedFrozenSet(value_list2)
    assert sorted(list(s1)) == sorted(list(s2))
    assert hash(s1) != hash(s2)


def test_immutable():

    s = OrderedFrozenSet()
    update_ops = ["add", "update", "extend", "append", "pop"]
    for op in update_ops:
        assert hasattr(s, op) == False


def test_ordered_frozen_set_basic_functionality():

    value_list = []
    for _ in range(1000000):
        value_list.append(random.randint(1, 100000))

    s1 = OrderedFrozenSet(value_list)
    s2 = frozenset(value_list)

    assert sorted(list(s1)) == sorted(list(s2))
