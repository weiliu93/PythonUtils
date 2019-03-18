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

    s1 = OrderedPersistenceSet()
    s2 = set()

    for _ in range(10000):
        value = random.randint(1, 500)
        assert (value in s1) == (value in s2)
        s1 = s1.add(value)
        s2.add(value)

    assert sorted(list(s1)) == sorted(list(s2))


def test_pop():

    value_list = []
    for _ in range(1000):
        value = random.randint(1, 100)
        if value not in value_list:
            value_list.append(value)

    s = OrderedPersistenceSet(value_list)
    assert list(s) == value_list

    pop_value_list = []
    while len(s) > 0:
        pop_s, pop_value = s.pop()
        pop_value_list.append(pop_value)
        s = pop_s
    assert pop_value_list == value_list
    assert list(s) == []


def test_pop_from_empty_set():

    s = OrderedPersistenceSet()
    try:
        s.pop()
        assert False
    except:
        pass


def test_eq():

    s1 = OrderedPersistenceSet([1, 4, 2])
    s2 = OrderedPersistenceSet([1, 4, 2])
    assert s1 == s2

    s2 = OrderedPersistenceSet([1, 2, 4])
    assert s1 != s2

    s2 = {1, 4, 2}
    assert s1 == s2

    s2 = {1, 4, 3}
    assert s1 != s2


def test_clear():

    s = OrderedPersistenceSet()
    s1 = s.clear()

    assert id(s) == id(s1)

    s = OrderedPersistenceSet([1, 3])
    s2 = s.clear()

    assert id(s) != id(s2)


def test_set_contains_no_dup_data():

    s = OrderedPersistenceSet()
    for _ in range(10000):
        s.add(random.randint(1, 500))
    value_list = list(s)
    value_set = set()
    for value in value_list:
        assert value not in value_set
        value_set.add(value)


def test_compared_with_builtin_set():
    def get_linked_list_length(list_node):
        ans = 0
        while list_node.next:
            ans += 1
            list_node = list_node.next
        return ans

    ops = ["add", "pop", "discard", "clear"]
    s = OrderedPersistenceSet()
    value_list = []
    for _ in range(100000):
        value = random.randint(1, 200)
        op = ops[random.randint(0, 3)]
        if op == "add":
            s = s.add(value)
            if value not in value_list:
                value_list.append(value)
        elif op == "pop":
            value1, value2 = None, None
            if len(s) > 0:
                s, value1 = s.pop()
            if len(value_list) > 0:
                value2 = value_list.pop(0)
            assert value1 == value2
        elif op == "discard":
            value = random.randint(1, 200)
            s = s.discard(value)
            if value in value_list:
                value_list.remove(value)
        else:
            s = s.clear()
            value_list.clear()
        assert list(s) == value_list

        len1, len2, len3 = len(s), len(s._value_dict), get_linked_list_length(s._head)
        assert len1 == len2 and len2 == len3


def test_backend_data_structure_length():
    def get_linked_list_length(list_node):
        ans = 0
        while list_node.next:
            ans += 1
            list_node = list_node.next
        return ans

    s = OrderedPersistenceSet()
    for _ in range(100000):
        value = random.randint(1, 1000)
        s = s.add(value)
        len1, len2, len3 = len(s), len(s._value_dict), get_linked_list_length(s._head)
        assert len1 == len2 and len2 == len3


def test_repr():

    s = OrderedPersistenceSet()
    assert repr(s) == "OrderedPersistenceSet()"

    s = OrderedPersistenceSet([1, 10, 4])
    assert repr(s) == "{1, 10, 4}"
