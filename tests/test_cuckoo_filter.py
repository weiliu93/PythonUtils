import sys
import os
import random

sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from cuckoo_filter import CuckooFilter


def test_basic_add():
    filter = CuckooFilter()
    for i in range(10):
        filter.add(i)
    for _ in range(10):
        value = random.randint(0, 100)
        if value < 10:
            assert value in filter
        else:
            assert value not in filter
    assert len(filter) == 10


def test_add_duplicate_value():
    filter = CuckooFilter()
    filter.add("abc")
    filter.add("def")
    filter.add("abc")
    assert len(filter) == 2


def test_basic_remove():
    filter = CuckooFilter()
    for i in range(10):
        filter.add(i)
    for i in range(10):
        assert filter.remove(i) == True
        assert len(filter) == 10 - i - 1
    assert list(filter) == []


def test_remove_element_not_exists():
    filter = CuckooFilter()
    for i in range(10):
        filter.add(i)
    for i in range(20):
        filter.remove(i)
    assert list(filter) == []


def test_clear():
    filter = CuckooFilter()
    for _ in range(100):
        filter.add(random.randint(1, 100))
    filter.clear()
    assert len(filter) == 0

    for i in range(10):
        filter.add(i + 10)
    assert len(filter) == 10


def test_contains():
    filter = CuckooFilter(array_size = 1 << 16)
    s = set()
    for _ in range(1000):
        value = random.randint(1, 1000)
        if value in s:
            assert value in filter
        else:
            assert value not in filter
            s.add(value)
            filter.add(value)


def test_len():
    filter = CuckooFilter(array_size = 1 << 16)
    s = set()
    for _ in range(6000):
        value = random.randint(1, 100)
        filter.add(value)
        s.add(value)
    assert len(filter) == len(s)


def test_total_number_of_elements_never_exceeding_threshold():
    filter = CuckooFilter(bucket_size = 4, array_size = 1 << 4)
    # in order to guarantee almost all buckets are occupied
    for _ in range(20000):
        filter.add(random.randint(1, 10000))
    assert len(filter) <= (1 << 4) * 4


def test_real_scenario():
    filter = CuckooFilter(bucket_size = 4, array_size = 1 << 8, substitution_limit=100)
    s , cnt = set(), 0
    for _ in range(100000):
        op = random.randint(1, 10)
        value = random.randint(1, 1000)
        # add: 3, remove: 3, contains: 3, clear: 1
        if op <= 3:
            s.add(value)
            filter.add(value)
            if len(s) != len(filter):
                cnt += 1
        elif op <= 6:
            if value in s:
                s.remove(value)
            filter.remove(value)
            if len(s) != len(filter):
                cnt += 1
        elif op <= 9:
            if (value in s) != (value in filter):
                cnt += 1
        else:
            filter.clear()
            s.clear()
    assert cnt == 0


def test_self_defined_class_scenario():
    filter = CuckooFilter(bucket_size=4, array_size= 1 << 7, substitution_limit=100)
    s = set()
    cnt = 0
    for _ in range(100000):
        x , y = random.randint(1, 20), random.randint(1, 20)
        p = Point(x , y)
        # add: 4, remove: 3, get: 3
        op = random.randint(1, 10)
        if op <= 4:
            # add
            s.add(p)
            filter.add(p)
            if len(s) != len(filter):
                cnt += 1
        elif op <= 7:
            # remove
            if p in s:
                s.remove(p)
            filter.remove(p)
            if len(s) != len(filter):
                cnt += 1
        else:
            # get
            if (p in filter) != (p in s):
                cnt += 1
    assert cnt == 0


def test_add_too_much_data_to_cuckoo_filter():
    filter = CuckooFilter(bucket_size = 4, array_size = 16, substitution_limit=10)
    for i in range(64):
        filter.add(i)
    assert len(filter) == 64
    for i in range(64, 100, 1):
        assert not filter.add(i)


# testing class
class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return self.x * 31 + self.y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        else:
            return False