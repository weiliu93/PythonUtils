from collections import MutableSet


class OrderedSet(MutableSet):
    """
    Set without duplicate elements, keep all elements in inserted order
    """

    class DoubleLinkedListNode(object):

        __slots__ = ["key", "prev", "next"]

        def __init__(self, *, key=None, prev=None, next=None):
            self.key = key
            self.prev = prev
            self.next = next

    CHUNK_SIZE = 32

    def __init__(self, iterable=None):
        self._head = self._tail = self.DoubleLinkedListNode()
        # here free linkedlist was regarded as a single linkedlist
        self._free_head = self.DoubleLinkedListNode()
        # allocate buffer pool first
        self._allocate_free_nodes(self.CHUNK_SIZE)
        self._total_chunk = 1
        # from key -> DoubleLinkedListNode
        self._key_to_list_node_map = {}
        # initialize from external iterable
        source_iterable = iterable if iterable else []
        for key in source_iterable:
            self.add(key)

    def add(self, key):
        if key not in self._key_to_list_node_map:
            new_list_node = self._create_new_list_node(key)
            self._key_to_list_node_map[key] = new_list_node
            self._append_list_node(new_list_node)

    def discard(self, key):
        if key in self._key_to_list_node_map:
            list_node = self._key_to_list_node_map[key]
            self._key_to_list_node_map.pop(key)
            self._remove_list_node(list_node)
            self._append_free_list_node(list_node)
            self._shrink_free_list_if_necessary()

    def pop(self):
        if self._key_to_list_node_map:
            first_list_node = self._first_list_node()
            result = first_list_node.key
            self._key_to_list_node_map.pop(first_list_node.key)
            self._remove_list_node(first_list_node)
            self._append_free_list_node(first_list_node)
            self._shrink_free_list_if_necessary()
            return result
        else:
            raise KeyError("pop from an empty set")

    def clear(self):
        # set is not empty
        if self._key_to_list_node_map:
            first, last = self._head.next, self._tail
            last.next = self._free_head.next
            self._free_head.next = first
            self._tail = self._head
            self._head.next = self._tail.next = None
        self._key_to_list_node_map.clear()

    def __len__(self):
        return len(self._key_to_list_node_map)

    def __contains__(self, key):
        return key in self._key_to_list_node_map

    def __iter__(self):
        list_node = self._head.next
        while list_node:
            yield list_node.key
            list_node = list_node.next

    def __reversed__(self):
        list_node = self._tail
        while list_node != self._head:
            yield list_node.key
            list_node = list_node.prev

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        result_list, list_node = [], self._head.next
        while list_node:
            result_list.append(list_node.key)
            list_node = list_node.next
        return "{%s}" % (", ".join(map(lambda item: str(item), result_list)))

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if (not hasattr(other, "__len__")) or (len(self) == len(other)):
            if isinstance(other, OrderedSet):
                return list(self) == list(other)
            else:
                return set(self) == set(other)
        else:
            return False

    def _create_new_list_node(self, key):
        free_node = self._fetch_free_list_node()
        if not free_node:
            self._double_free_list()
            free_node = self._fetch_free_list_node()
        free_node.key = key
        return free_node

    def _append_list_node(self, node):
        node.prev = node.next = None
        self._tail.next = node
        node.prev = self._tail
        self._tail = node

    def _remove_list_node(self, node):
        if node == self._tail:
            self._tail = self._tail.prev
            self._tail.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        node.prev = node.next = None

    def _first_list_node(self):
        return self._head.next

    def _append_free_list_node(self, node):
        node.next = self._free_head.next
        self._free_head.next = node

    def _allocate_free_nodes(self, size):
        for _ in range(size):
            new_node = self.DoubleLinkedListNode()
            self._append_free_list_node(new_node)

    def _double_free_list(self):
        target_size = self.CHUNK_SIZE * self._total_chunk
        self._allocate_free_nodes(target_size)
        self._total_chunk <<= 1

    def _shrink_free_list_if_necessary(self):
        # if we have less than two chunks, we will never shrink it
        if self._total_chunk > 2:
            used, threshold = len(self), (self._total_chunk >> 2) * self.CHUNK_SIZE
            if used <= threshold:
                # TODO maybe we can optimize these codes
                for _ in range((self._total_chunk >> 1) * self.CHUNK_SIZE):
                    self._fetch_free_list_node()
                self._total_chunk >>= 1

    def _fetch_free_list_node(self):
        if self._free_head.next:
            free_node = self._free_head.next
            self._free_head.next = free_node.next
            free_node.next = free_node.prev = None
            return free_node
        else:
            return None
