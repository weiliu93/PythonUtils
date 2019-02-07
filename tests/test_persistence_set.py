import sys
import os
import random

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from ordered_persistence_set import OrderedPersistenceSet



def test_add_element():

    s = OrderedPersistenceSet()
    assert list(s) == []

    s1 = s.add(100)
    assert list(s1) == [100]
    assert list(s) == []

    s2 = s1.add(7)
    assert list(s2) == [100, 7]
    assert list(s1) == [100]
    assert list(s) == []

    s3 = s1.add(200)
    assert list(s3) == [100, 200]
    assert list(s2) == [100, 7]
    assert list(s1) == [100]
    assert list(s) == []


def test_add_always_return_a_new_object():

    s = OrderedPersistenceSet()
    s1 = s.add(100)
    assert id(s) != id(s1)


def test_discard():

    s = OrderedPersistenceSet([1, 10, 6, 5])

    s1 = s.discard(10)
    assert list(s1) == [1, 6, 5]

    s2 = s.discard(5)
    assert list(s2) == [1, 10, 6]

    s3 = s1.discard(6)
    assert list(s3) == [1, 5]

    assert list(s) == [1, 10, 6, 5]


def test_discard_always_return_a_new_object_if_succeeded():

    s = OrderedPersistenceSet([1, 10, 4])
    s1 = s.discard(10)
    assert id(s) != id(s1)


def test_discard_return_original_object_if_failed():

    s = OrderedPersistenceSet([1, 4, 8])
    s1 = s.discard(20)
    assert id(s) == id(s1)


def test_remove():

    s = OrderedPersistenceSet([1, 4, 2])
    try:
        s.remove(3)
        assert False
    except:
        pass

    try:
        s1 = s.remove(4)
        assert list(s1) == [1, 2]
        assert list(s) == [1, 4, 2]
    except:
        assert False


def test_iter():

    s = OrderedPersistenceSet()
    value_list = []
    for i in range(1000):
        value = random.randint(1, 100)
        if value not in s:
            s = s.add(value)
            value_list.append(value)
    assert list(s) == value_list


def test_rev_iter():

    s = OrderedPersistenceSet()
    value_list = []
    for i in range(1000):
        value = random.randint(1, 100)
        if value not in s:
            s = s.add(value)
            value_list.append(value)
    value_list.reverse()
    assert list(reversed(s)) == value_list


def test_len():

    s = OrderedPersistenceSet()
    builtin_set = set()
    for i in range(1000):
        value = random.randint(1, 100)
        s = s.add(value)
        builtin_set.add(value)
    assert len(s) == len(builtin_set)


def test_contains():




    pass


def test_pop():



    pass


def test_eq():




    pass


def test_repr():




    pass


def test_clear():



    pass


def test_set_contains_no_dup_data():




    pass


def test_compared_with_builtin_set():



    pass