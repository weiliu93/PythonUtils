from collections import defaultdict


class IndexPriorityQueue(object):

    def __init__(self, init_data=None):
        # None as placeholder
        self._buffer = [None]
        # value to all possible indexes
        self._value_to_index_set_dict = defaultdict(set)
        # build heap with given data
        if init_data:
            self._buffer = [None] + list(init_data)
            total = len(self._buffer) - 1
            # fill value_to_index_set_dict with appropriate indexes
            i = 1
            while i <= total:
                self._value_to_index_set_dict[self._buffer[i]].add(i)
                i += 1
            # adjust heap
            i = total // 2
            while i >= 1:
                self._sink(i)
                i -= 1

    def __len__(self):
        return len(self._buffer) - 1

    def __iter__(self):
        for value in self._buffer[1: ]:
            yield value

    def add(self, value):
        index = len(self._buffer)
        # mapping value and next available index
        self._buffer.append(value)
        self._value_to_index_set_dict[value].add(index)
        # swim value from bottom to top
        self._swim(index)

    def empty(self):
        return len(self._buffer) == 1

    def update(self, value, new_value):
        if self.remove(value):
            self.add(new_value)
        else:
            raise Exception("value is not exists")

    def pop(self):
        if self.empty():
            raise Exception("priority queue is empty")
        ans = self._buffer[1]
        # update value to index set dict
        total = len(self._buffer) - 1
        self._swap(1, total)
        self._value_to_index_set_dict[self._buffer[total]].remove(total)
        self._buffer.pop()
        # keep balance
        self._sink(1)
        return ans

    def peek(self):
        if self.empty():
            raise Exception("priority queue is empty")
        return self._buffer[1]

    def remove(self, value):
        # need to check if value exists, and set is not empty
        if value in self._value_to_index_set_dict and self._value_to_index_set_dict[value]:
            total = len(self._buffer) - 1
            index = list(self._value_to_index_set_dict[value])[0]
            # swap index with total
            self._swap(index, total)
            # remove last element
            self._value_to_index_set_dict[self._buffer[total]].remove(total)
            self._buffer.pop()
            self._keep(index)
            return True
        else:
            return False

    def clear(self):
        self._buffer = [None]
        self._value_to_index_set_dict.clear()

    def _keep(self, index):
        # keep index element subtree balanced
        if index < len(self._buffer):
            self._swim(index)
            self._sink(index)

    def _swap(self, index1, index2):
        # swap buffer array elements and value_to_index_set_dict
        if index1 != index2:
            value1, value2 = self._buffer[index1], self._buffer[index2]
            self._value_to_index_set_dict[value1].remove(index1)
            self._value_to_index_set_dict[value2].remove(index2)
            self._buffer[index1], self._buffer[index2] = value2, value1
            self._value_to_index_set_dict[value1].add(index2)
            self._value_to_index_set_dict[value2].add(index1)

    def _swim(self, index):
        # balance from bottom to top
        while index > 1:
            parent_index = index // 2
            if self._buffer[index] < self._buffer[parent_index]:
                self._swap(index, parent_index)
                index = parent_index
            else:
                break

    def _sink(self, index):
        # balance from top to bottom
        while index < len(self._buffer):
            # both of the two children exists
            if index * 2 + 1 < len(self._buffer):
                left_children, right_children = self._buffer[index * 2], self._buffer[index * 2 + 1]
                if left_children < right_children:
                    children = left_children
                    children_index = index * 2
                else:
                    children = right_children
                    children_index = index * 2 + 1
                if children < self._buffer[index]:
                    self._swap(index, children_index)
                    index = children_index
                else:
                    break
            elif index * 2 < len(self._buffer):
                # only one child
                if self._buffer[index] > self._buffer[index * 2]:
                    self._swap(index , index * 2)
                break
            else:
                # no children available
                break
