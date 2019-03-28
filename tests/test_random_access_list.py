import sys
import os
import random


sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from random_access_list import RandomAccessList


def test_random_access_list_cons():
    ral = RandomAccessList()
    for i in range(10):
        # [1 -> i + 1]
        ral = ral.cons(i + 1)
        assert list(ral) == [i + 1 - j for j in range(i + 1)]


def test_random_access_list_cons_is_immutable():
    ral = RandomAccessList()
    another = ral.cons(10)
    assert list(ral) == []
    assert list(another) == [10]
    assert id(ral) != id(another)


def test_random_access_list_head():
    ral = RandomAccessList()
    for i in range(10):
        ral = ral.cons(i + 1)
        assert list(ral.head()) == [i + 1]


def test_random_access_list_head_is_immutable():
    ral = RandomAccessList()
    for i in range(10):
        ral = ral.cons(i + 1)
    head = ral.head()
    assert list(head) == [10]
    assert list(ral) == [10 - i for i in range(10)]
    assert id(head) != id(ral)


def test_random_access_list_tail():
    ral = RandomAccessList()
    for i in range(10):
        ral = ral.cons(i + 1)
    tail = ral.tail()
    assert list(tail) == [9 - i for i in range(9)]


def test_random_access_list_tail_is_immutable():
    ral = RandomAccessList()
    for i in range(10):
        ral = ral.cons(i + 1)
    tail = ral.tail()
    assert list(tail) == [9 - i for i in range(9)]
    assert list(ral) == [10 - i for i in range(10)]
    assert id(tail) != id(ral)


def test_random_access_list_get():
    values = []
    ral = RandomAccessList()
    for i in range(100):
        values.append(random.randint(1, 10000))
        ral = ral.cons(values[-1])
    values.reverse()
    for i in range(100):
        assert values[i] == ral.get(i) and values[i] == ral[i]


def test_random_access_list_negative_index_get():
    ral = RandomAccessList()
    for i in range(100):
        ral = ral.cons(i + 1)
    # from 100 -> 1
    for i in range(1, 101, 1):
        assert ral.get(-i) == i
        assert ral[-i] == i


def test_random_access_list_size():
    ral = RandomAccessList()
    assert ral.size() == 0

    another = ral.cons(10)
    assert ral.size() == 0
    assert another.size() == 1

    ral = ral.cons(100)
    assert ral.size() == 1


def test_random_access_list_head_or_tail_nil_list():
    ral = RandomAccessList()
    try:
        ral.head()
        assert False
    except:
        pass
    try:
        ral.tail()
        assert False
    except:
        pass


def test_random_access_list_iter():
    ral = RandomAccessList()
    values = []
    for i in range(100):
        values.append(random.randint(1, 10000))
        ral = ral.cons(values[-1])
    values.reverse()
    list1 = list(iter(ral))
    list2 = list(iter(values))
    assert list1 == list2


def test_random_access_list_clear():
    ral = RandomAccessList()
    for i in range(10):
        ral = ral.cons(i + 1)
    clear_ral = ral.clear()
    assert list(clear_ral) == []
    assert list(ral) == [10 - i for i in range(10)]


def test_random_access_list_real_scenario():
    ral = RandomAccessList()
    values = []
    for _ in range(1000000):
        weight = random.randint(1, 10)
        # weight array: [5, 1, 1, 1, 2]
        if weight <= 5:
            # cons
            value = random.randint(1, 100)
            ral = ral.cons(value)
            values = [value] + values
        elif weight <= 6:
            # head
            assert len(ral) == len(values)
            if len(ral) > 0:
                values = values[:1]
                ral = ral.head()
        elif weight <= 7:
            # tail
            assert len(ral) == len(values)
            if len(ral) > 0:
                values = values[1:]
                ral = ral.tail()
        elif weight <= 8:
            # clear
            values.clear()
            ral = ral.clear()
        else:
            # get
            assert len(ral) == len(values)
            # if list is not empty
            if len(values) > 0:
                index = random.randint(0, len(values) - 1)
                assert values[index] == ral[index]
        assert list(ral) == values
        assert ral.size() == len(values)


def test_random_access_list_all_operations_are_immutable():
    ral = RandomAccessList()
    # ral to list result dict
    ral_result_dict, freeze_dict, cnt = {}, {}, 0
    for index in range(100):
        weight = random.randint(1, 10)
        # freeze current dict
        for key, prev_ral in ral_result_dict.items():
            freeze_dict[key] = list(prev_ral)
        # weight array: [5, 2, 2, 1]
        if weight <= 5:
            # cons
            value = random.randint(1, 100)
            ral = ral.cons(value)
            cnt += 1
            ral_result_dict[ral] = list(ral)
        elif weight <= 7:
            # head
            if len(ral) > 0:
                ral = ral.head()
                cnt += 1
                ral_result_dict[ral] = list(ral)
        elif weight <= 9:
            # tail
            if len(ral) > 0:
                ral = ral.tail()
                cnt += 1
                ral_result_dict[ral] = list(ral)
        else:
            # clear
            ral = ral.clear()
            cnt += 1
            ral_result_dict[ral] = list(ral)
        # every actions create a new RAL object
        assert len(ral_result_dict) == cnt
        # it means all random access lists haven't been modified after current update
        for key, prev_ral in ral_result_dict.items():
            if key in freeze_dict:
                assert list(prev_ral) == freeze_dict[key]
