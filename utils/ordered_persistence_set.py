from collections import Set


class OrderedPersistenceSet(Set):
    """
    Persistence OrderedSet, now almost all programming APIs like `add`, `discard` will
    return a new set instance, it is in-consistent with `Set`'s python design actually

    Implementation based on path copy, it is time costly and not very good memory friendly
    """

    class DoubleLinkedList(object):

        __slots__ = ["prev", "next", "key"]

        def __init__(self, *, prev=None, next=None, key=None):
            self.prev = prev
            self.next = next
            self.key = key

    def __init__(self, iterable=None):
        self._value_dict = {}
        self._head = self._tail = self.DoubleLinkedList()
        iterable = iterable if iterable else []
        for value in iterable:
            if value not in self._value_dict:
                list_node = self.DoubleLinkedList(key=value)
                self._value_dict[value] = list_node
                self._append_list_node(list_node)

    def add(self, key):
        if key not in self._value_dict:
            new_set = OrderedPersistenceSet(self)
            new_list_node = self.DoubleLinkedList(key=key)
            new_set._append_list_node(new_list_node)
            new_set._value_dict[key] = new_list_node
            return new_set
        else:
            return self

    def discard(self, key):
        if key in self._value_dict:
            list_node = self._value_dict[key]
            new_list_head, new_list_tail = self._copy_linked_list_before_specified_node(
                list_node
            )
            new_list_tail.next = list_node.next
            if list_node.next:
                list_node.next.prev = new_list_tail
                new_list_tail = self._tail
            new_value_dict = {}
            node = new_list_head
            while node:
                new_value_dict[node.key] = node
                node = node.next
            new_set = OrderedPersistenceSet()
            new_set._head = new_list_head
            new_set._tail = new_list_tail
            new_set._value_dict = new_value_dict
            return new_set
        else:
            return self

    def remove(self, key):
        if key not in self:
            raise KeyError(key)
        return self.discard(key)

    def pop(self):
        if len(self) > 0:
            return self.discard(self._head.next.key)
        else:
            raise KeyError("pop from an empty set")

    def clear(self):
        if len(self) > 0:
            return OrderedPersistenceSet()
        else:
            return self

    def __len__(self):
        return len(self._value_dict)

    def __contains__(self, key):
        return key in self._value_dict

    def __iter__(self):
        node = self._head.next
        while node:
            yield node.key
            node = node.next

    def __reversed__(self):
        node = self._tail
        while node != self._head:
            yield node.key
            node = node.prev

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
            if isinstance(other, OrderedPersistenceSet):
                return list(self) == list(other)
            else:
                return set(self) == set(other)
        else:
            return False

    def _append_list_node(self, list_node):
        self._tail.next = list_node
        list_node.prev = self._tail
        self._tail = list_node

    def _remove_list_node(self, list_node):
        if list_node == self._tail:
            self._tail = self._tail.prev
            self._tail.next = None
        else:
            list_node.prev.next = list_node.next
            list_node.next.prev = list_node.prev

    def _copy_linked_list_before_specified_node(self, list_node):
        head_node = self._head.next
        copy_head = copy_tail = self.DoubleLinkedList()
        while head_node != list_node:
            new_node = self.DoubleLinkedList(key=head_node.key)
            copy_tail.next = new_node
            new_node.prev = copy_tail
            copy_tail = new_node
            head_node = head_node.next
        return copy_head, copy_tail
