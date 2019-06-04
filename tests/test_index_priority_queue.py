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


def test_priority_queue_clear():
    queue = IndexPriorityQueue()
    queue.add(10)
    queue.add(100)
    queue.add(70)
    queue.clear()
    assert len(queue) == 0


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


def test_real_scenario():


    pass