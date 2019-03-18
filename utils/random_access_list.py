class RandomAccessList(object):
    def __init__(self, value=None):
        # single element list
        if value:
            self._head = ListNode(value=value, size=1)
            self._head.next = ListNode()
            self._size = 1
        # nil list
        else:
            self._head = ListNode()
            self._size = 0

    def cons(self, value):
        new_list = RandomAccessList(value)
        # if we need to merge two trees together
        if self._head and self._head.next and self._head.size == self._head.next.size:
            new_list._head = ListNode(
                left=self._head,
                right=self._head.next,
                size=self._head.size + self._head.next.size + 1,
                next=self._head.next.next,
                value=value,
            )
        # just link to root node
        else:
            new_list._head = ListNode(next=self._head, value=value, size=1)
        new_list._size = self._size + 1
        return new_list

    def head(self):
        assert self._size > 0, "Empty list has no head list"
        return RandomAccessList(self._head.value)

    def tail(self):
        assert self._size > 0
        # if we need to split the head tree
        if self._head.left and self._head.right:
            head_right = ListNode(
                left=self._head.right.left,
                right=self._head.right.right,
                value=self._head.right.value,
                size=self._head.right.size,
                next=self._head.next,
            )
            head_left = ListNode(
                left=self._head.left.left,
                right=self._head.left.right,
                next=head_right,
                value=self._head.left.value,
                size=self._head.left.size,
            )
            new_list = RandomAccessList()
            new_list._head = head_left
            new_list._size = self._size - 1
            return new_list
        else:
            # if head tree only contains one element
            new_list = RandomAccessList()
            new_list._head = self._head.next
            new_list._size = self._size - 1
            return new_list

    def size(self):
        return self._size

    def empty(self):
        return self.size() == 0

    def __len__(self):
        return self.size()

    def get(self, index):
        # check if it is a positive index or negative index
        assert (index >= 0 and index < self._size) or (
            index >= -self._size and index < 0
        )
        if index >= 0:
            index += 1
        else:
            index = self._size + index + 1
        current = self._head
        while index > 1:
            if index > current.size:
                index -= current.size
                current = current.next
            else:
                if index <= current.left.size + 1:
                    index -= 1
                    current = current.left
                else:
                    index -= current.left.size + 1
                    current = current.right
        return current.value

    def clear(self):
        return RandomAccessList()

    def __getitem__(self, item):
        return self.get(item)

    def __str__(self):
        return "(" + ", ".join(map(str, list(self))) + ")"

    def __iter__(self):
        current = self._head
        # exclude nil node
        while current.size > 0:
            stack = [current]
            # collect all values in pre-order traversal
            while stack:
                node = stack.pop()
                yield node.value
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
            current = current.next


class ListNode(object):
    def __init__(self, left=None, right=None, next=None, value=None, size=0):
        self.left = left
        self.right = right
        self.next = next
        self.value = value
        self.size = size
