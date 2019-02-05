import sys
import os
import random

from collections import OrderedDict

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from ordered_set import OrderedSet


def test_ordered_set_basic_functionality():

    s = OrderedSet()
    for i in range(10):
        s.add(i + 1)

    assert len(s) == 10
    for i in range(10):
        assert s.pop() == i + 1

    s.add(10)
    s.add(20)
    s.add(50)
    s.add(100)
    s.remove(20)

    target_list = [10, 50, 100]
    assert list(s) == target_list


def test_ordered_set_duplicate_add():

    s = OrderedSet()
    s.add(10)
    s.add(20)
    s.add(10)
    assert len(s) == 2
    assert list(s) == [10, 20]


def test_ordered_set_discard():

    s = OrderedSet()
    s.add(10)
    s.discard(100)
    s.discard(10)
    s.discard(10)

    assert list(s) == []


def test_ordered_set_iter():

    s = OrderedSet()
    for i in range(1, 6, 1):
        s.add(i)
    assert list(s) == [1, 2, 3, 4, 5]

    vis = set()
    s.clear()
    values = []
    for i in range(1000000):
        value = random.randint(1, 100000000)
        while value in vis:
            value = random.randint(1, 100000000)
        vis.add(value)
        values.append(value)
        s.add(value)
    assert list(s) == values


def test_ordered_set_clear():

    s = OrderedSet()
    for i in range(10000):
        s.add(i)
    assert len(s) == 10000

    s.clear()

    for i in range(100):
        s.add(i)
    assert len(s) == 100


def test_ordered_set_clear_then_clean_again():

    s = OrderedSet()
    for i in range(10):
        s.add(i)
    s.clear()
    assert len(s) == 0

    s.clear()
    assert len(s) == 0


def test_ordered_set_reverse():

    vis = set()
    s = OrderedSet()
    values = []
    for _ in range(1000000):
        value = random.randint(1, 1000000)
        while value in vis:
            value = random.randint(1, 1000000)
        vis.add(value)
        values.append(value)
        s.add(value)
    values.reverse()
    reverse_s = reversed(s)
    assert list(reverse_s) == values


def test_add_and_pop():

    s = OrderedSet()
    for i in range(100):
        s.add(i + 1)
    assert list(s) == [i + 1 for i in range(100)]

    for i in range(100):
        assert s.pop() == i + 1


def test_compared_with_ordereddict():

    d = OrderedDict()
    s = OrderedSet()

    ops = ['add', 'discard', 'clear', 'pop']
    for i in range(100000):
        op_index = random.randint(0, 3)
        op = ops[op_index]

        if op == 'add':
            value = random.randint(- 1000000000, 1000000000)
            s.add(value)
            d[value] = value
        elif op == 'discard':
            value = random.randint(- 1000000000, 1000000000)
            s.discard(value)
            d.pop(value, None)
        elif op == 'clear':
            d.clear()
            s.clear()
        elif op == 'pop':
            assert len(s) == len(d)
            if len(s) > 0:
                # pop is valid
                value1 = s.pop()
                first_key = list(d.keys())[0]
                value2 = d.pop(first_key)
                assert value1 == value2

        # check if two collection are same
        assert list(s) == list(d.keys())


def test_pop_from_empty_set():

    s = OrderedSet()
    try:
        s.pop()
        assert False
    except Exception as e:
        assert isinstance(e, KeyError)


def test_init_set_with_some_data():

    s = OrderedSet([1 , 9 , 7 , 3])
    assert len(s) == 4
    assert list(s) == [1, 9, 7, 3]


def test_use_default_init():

    s = OrderedSet()
    assert len(s) == 0


def test_set_has_no_duplicate_data():

    s = OrderedSet()
    for i in range(1000000):
        s.add(random.randint(- 1000000000, 1000000000))
    vis = set()
    while s:
        value = s.pop()
        assert value not in vis
        vis.add(value)


def test_contains():

    vis = set()
    s = OrderedSet()

    ops = ['add', 'contains', 'discard']
    for i in range(1000):
        op_index = random.randint(0, 2)
        op = ops[op_index]
        if op == 'add':
            value = random.randint(- 1000000, 1000000)
            vis.add(value)
            s.add(value)
        elif op == 'contains':
            value = random.randint(- 1000000, 1000000)
            assert (value in vis) == (value in s)
        else:
            value = random.randint(- 1000000, 1000000)
            s.discard(value)
            vis.discard(value)
        assert sorted(list(vis)) == sorted(list(s))


def test_discard():

    vis = set()
    s = OrderedSet()

    ops = ['add', 'discard']
    for i in range(1000):
        op_index = random.randint(0, 1)
        op = ops[op_index]
        if op == 'add':
            value = random.randint(- 1000, 1000)
            vis.add(value)
            s.add(value)
        else:
            value = random.randint(- 1000, 1000)
            s.discard(value)
            vis.discard(value)
        assert sorted(list(vis)) == sorted(list(s))


def test_len():

    s = OrderedSet()
    vis = set()
    for i in range(100000):
        value = random.randint(1, 1000)
        vis.add(value)
        s.add(value)
    assert len(s) == len(vis)


def test_equal():

    s1 = OrderedSet([1, 2, 3, 4])
    s2 = OrderedSet([1, 2, 3, 4])
    assert s1 == s2

    s2 = OrderedSet([1, 2, 4, 3])
    assert s1 != s2

    s = set([1, 4, 3, 2])
    assert s1 == s

    s2 = OrderedSet([1, 2, 3])
    assert s1 != s2

    value_list = [4, 3, 2, 1]
    assert s1 == value_list


def test_str():

    s = OrderedSet([1, 5, 3])
    assert str(s) == '{1, 5, 3}'

    s = OrderedSet()
    assert str(s) == 'OrderedSet()'


def test_repr():

    s = OrderedSet([1, 5, 3])
    assert repr(s) == '{1, 5, 3}'

    s = OrderedSet()
    assert str(s) == 'OrderedSet()'


def test_chunk_num_double():

    s = OrderedSet()
    for i in range(100):
        s.add(i)
    assert s._total_chunk == 4


def test_chunk_num_shrink():

    s = OrderedSet()
    for i in range(1000):
        s.add(i)
    # current total number of free nodes is 1024
    assert s._total_chunk == 32

    for i in range(800):
        s.pop()
    # now the total number of free nodes is 512
    assert s._total_chunk == 16


def test_chunk_num_double_then_shrink():

    s = OrderedSet()
    for i in range(1000):
        s.add(i)
    assert s._total_chunk == 32

    for i in range(800):
        s.pop()
    assert s._total_chunk == 16

    for i in range(1000):
        s.add(i + 2000)
    assert s._total_chunk == 64


def test_list_size_is_valid():

    def get_list_size(s):
        node = s._head
        ans = 0
        while node.next != None:
            node = node.next
            ans += 1
        return ans

    def get_free_list_size(s):
        node = s._free_head
        ans = 0
        while node.next != None:
            node = node.next
            ans += 1
        return ans

    s = OrderedSet()
    ops = ['add', 'pop', 'discard']
    for i in range(1000000):
        op = ops[random.randint(0, 2)]
        if op == 'add':
            value = random.randint(1, 1000)
            s.add(value)
        elif op == 'pop':
            if len(s) > 0:
                s.pop()
        else:
            value = random.randint(1, 1000)
            s.discard(value)
        assert len(s) == get_list_size(s)
        assert get_list_size(s) + get_free_list_size(s) == s._total_chunk * OrderedSet.CHUNK_SIZE