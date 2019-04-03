class DoublyLinkedList(object):
    """Doubly LinkedList, support all common operations. Values could be duplicate
       in LinkedList, but all nodes should be unique.

       eg: 1 -> 4 -> 2 -> 1 is possible, but the first and last node should be distinct
    """

    class LinkedListNode(object):

        __slots__ = ("prev", "next", "value")

        def __init__(self, value, prev=None, next=None):
            self.prev = prev
            self.next = next
            self.value = value

        def __str__(self):
            return "(value: {})".format(str(self.value))

    def __init__(self):
        self._head = self.LinkedListNode(None)
        self._tail = self._head
        # avoid duplication and incorrect update
        self._node_set = set()

    def __iter__(self):
        node = self._head
        while node.next:
            yield node.next
            node = node.next

    def __len__(self):
        return len(self._node_set)

    def __str__(self):
        return str(list(map(str, self)))

    @staticmethod
    def create_new_node(value):
        return DoublyLinkedList.LinkedListNode(value)

    def add_first(self, list_node):
        return self._insert_after(self._head, list_node)

    def append(self, list_node):
        return self._insert_after(self._tail, list_node)

    def remove_and_add_first(self, list_node):
        if self.remove(list_node):
            return self.add_first(list_node)
        else:
            return False

    def remove_and_append(self, list_node):
        if self.remove(list_node):
            return self.append(list_node)
        else:
            return False

    def pop_first(self):
        list_node = self._head.next
        self.remove(list_node)
        return list_node

    def peek_first(self):
        return self._head.next

    def pop_last(self):
        if self._head == self._tail:
            return None
        else:
            result = self._tail
            self.remove(result)
            return result

    def peek_last(self):
        if self._head == self._tail:
            return None
        else:
            return self._tail

    def clear(self):
        self._head = self.LinkedListNode(None)
        self._tail = self._head
        self._node_set.clear()

    def remove(self, list_node):
        """remove list_node from linked list"""
        if list_node not in self._node_set:
            return False
        else:
            assert isinstance(list_node, DoublyLinkedList.LinkedListNode)
            if list_node == self._tail:
                self._tail = self._tail.prev
                self._tail.next = None
            else:
                list_node.prev.next = list_node.next
                list_node.next.prev = list_node.prev
            self._node_set.remove(list_node)
            return True

    def _insert_after(self, target_node, list_node):
        if list_node in self._node_set:
            return False
        else:
            assert isinstance(list_node, DoublyLinkedList.LinkedListNode)
            list_node.next = target_node.next
            list_node.prev = target_node
            list_node.prev.next = list_node
            if list_node.next:
                list_node.next.prev = list_node
            else:
                self._tail = list_node
            self._node_set.add(list_node)
            return True
