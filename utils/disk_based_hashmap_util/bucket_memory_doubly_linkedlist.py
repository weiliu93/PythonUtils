from pympler import asizeof

from doubly_linkedlist import DoublyLinkedList
from bucket import BucketObject


class BucketMemoryDoublyLinkedList(DoublyLinkedList):
    """Doubly Linked List wrapper, add memory usage monitor extension. Only work for BucketObject"""

    def __init__(self):
        super().__init__()
        self._total_memory_usage = 0

    @property
    def memory_usage(self):
        return self._total_memory_usage

    def remove(self, list_node):
        if super().remove(list_node):
            bucket_object = list_node.value
            assert isinstance(bucket_object, BucketObject)
            self._total_memory_usage -= asizeof.asizeof(bucket_object.value)
            return True
        else:
            return False

    def clear(self):
        super().clear()
        self._total_memory_usage = 0

    def _insert_after(self, target_node, list_node):
        if super()._insert_after(target_node, list_node):
            bucket_object = list_node.value
            assert isinstance(bucket_object, BucketObject)
            self._total_memory_usage += asizeof.asizeof(bucket_object.value)
            return True
        else:
            return False
