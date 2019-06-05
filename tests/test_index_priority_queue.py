import sys
import os
import random


sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from index_priority_queue import IndexPriorityQueue



def test_basic_priority_queue_functionalities():
    queue = IndexPriorityQueue(init_data = [10, 5, 3 , 6 , 100])
    sorted_array = [3, 5, 6, 10, 100]
    while not queue.empty():
        assert queue.pop() == sorted_array.pop(0)
    assert len(queue) == 0


def test_priority_queue_heap_sort():
    init_data = [random.randint(1, 100000000) for _ in range(1000)]
    sorted_array = sorted(init_data)
    queue_output_array = []
    queue = IndexPriorityQueue()
    for data in init_data:
        queue.add(data)
    while not queue.empty():
        queue_output_array.append(queue.pop())
    assert sorted_array == queue_output_array


def test_priority_queue_add_duplicate_data():
    queue = IndexPriorityQueue()
    for idx in range(10):
        queue.add(24)
        assert len(queue) == idx + 1
    total = 10
    while not queue.empty():
        assert len(queue) == total
        queue.pop()
        total -= 1


def test_priority_queue_peek_or_pop_when_empty():
    queue = IndexPriorityQueue()
    try:
        queue.peek()
        assert False
    except:
        pass
    try:
        queue.pop()
        assert False
    except:
        pass


def test_priority_queue_remove():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(6)
    queue.add(6)
    queue.add(3)
    queue.add(20)

    assert queue.remove(6) == True
    assert queue.remove(6) == True
    assert queue.remove(6) == False

    assert queue.pop() == 3
    assert queue.pop() == 10
    assert queue.pop() == 20


def test_remove_not_existing_data():
    queue = IndexPriorityQueue()
    queue.add(10)
    assert queue.remove(100) == False


def test_priority_queue_clear():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(100)
    queue.add(70)
    queue.clear()
    assert len(queue) == 0


def test_priority_queue_len():
    queue = IndexPriorityQueue()
    queue.add(1)
    # duplicate elements exist
    queue.add(2)
    queue.add(2)
    assert len(queue) == 3


def test_priority_queue_iter():
    queue = IndexPriorityQueue()
    values = []
    for _ in range(10):
        random_value = random.randint(1, 1000)
        values.append(random_value)
        queue.add(random_value)
    values.sort()
    assert values == sorted(list(queue))


def test_priority_queue_empty():
    queue = IndexPriorityQueue()
    assert queue.empty() == True

    queue.add(10)
    assert queue.empty() == False


def test_priority_queue_empty_check():
    queue = IndexPriorityQueue()
    assert queue.empty() == True

    queue.add(10)
    queue.add(100)
    assert queue.empty() == False


def test_priority_queue_peek_and_pop_return_same_result():
    queue = IndexPriorityQueue([1, 10, 4 , 5 , 2])
    while not queue.empty():
        assert queue.peek() == queue.pop()


def test_priority_queue_peek_will_not_remove_data():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(20)

    assert len(queue) == 2
    assert queue.peek() == 10

    assert len(queue) == 2
    assert queue.peek() == 10

    assert len(queue) == 2


def test_priority_queue_pop_will_remove_data():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(20)

    assert len(queue) == 2
    assert queue.pop() == 10

    assert len(queue) == 1
    assert queue.pop() == 20

    assert len(queue) == 0


def test_priority_queue_update_data_and_minimum_changed():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(20)

    assert queue.peek() == 10
    queue.update(20, 5)
    assert queue.peek() == 5


def test_priority_queue_update_data_not_exists():
    queue = IndexPriorityQueue()
    try:
        queue.update(10, 20)
        assert False
    except:
        pass


def test_priority_queue_update_data_multi_times():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(20)
    queue.add(30)
    queue.add(40)

    # 10, 20, 30, 40
    assert queue.peek() == 10

    # 8, 10, 30, 40
    queue.update(20, 8)
    assert queue.peek() == 8

    # 3, 8, 10, 30
    queue.update(40, 3)
    assert queue.peek() == 3

    # 8, 10, 12, 30
    queue.update(3, 12)
    assert queue.peek() == 8

    # 10, 12, 30, 40
    queue.update(8, 40)
    assert queue.peek() == 10


def test_real_scenario():
    ops = ["add", "peek", "pop", "remove", "update"]

    compared_array = []
    queue = IndexPriorityQueue()

    for _ in range(1000000):
        op = random.choice(ops)
        if op == "add":
            value = random.randint(1, 300)
            compared_array.append(value)
            compared_array.sort()
            queue.add(value)
        elif op == "peek":
            if compared_array:
                assert queue.peek() == compared_array[0]
        elif op == "pop":
            if compared_array:
                assert compared_array.pop(0) == queue.pop()
        elif op == "remove":
            value = random.randint(1, 300)
            if value in compared_array:
                assert queue.remove(value) == True
                compared_array.remove(value)
                compared_array.sort()
            else:
                assert queue.remove(value) == False
        elif op == "update":
            if compared_array:
                value = random.choice(compared_array)
                new_value = random.randint(1, 300)
                compared_array.remove(value)
                compared_array.append(new_value)
                compared_array.sort()
                queue.update(value, new_value)
        # compare two data structure
        assert compared_array == sorted(list(queue))


def test_index_priority_queue_built_on_existing_array():
    array = [random.randint(1, 10000) for _ in range(1000)]
    sorted_array = sorted(array)

    queue = IndexPriorityQueue(init_data = array)
    while not queue.empty() and queue.pop() == sorted_array.pop(0):
        pass

    assert len(queue) == 0 and len(sorted_array) == 0
