class TernarySearchTrie(object):
    """key could only be string, value could be any object"""

    class TreeNode(object):

        __slots__ = ["less", "equal", "greater", "parent", "ch", "value"]

        def __init__(self, ch="", value=None):
            self.less = self.equal = self.greater = self.parent = None
            self.ch = ch
            self.value = value

    def __init__(self):
        self._root = None
        self._total = 0

    def __len__(self):
        return self._total

    def __iter__(self):
        return map(lambda tuple: tuple[0], self._get_key_values(self._root, ""))

    def __delitem__(self, key):
        self.remove(key)

    def items(self):
        return self._get_key_values(self._root, "")

    def clear(self):
        self._root = None
        self._total = 0

    def __setitem__(self, key, value):
        assert isinstance(key, str)
        assert value is not None
        self._root = self._insert(self._root, key, 0, value)

    def _insert(self, node, key, current, value):
        node = node or self.TreeNode(key[current])
        if node.ch == key[current]:
            if current == len(key) - 1:
                # new key-value
                if node.value is None:
                    self._total += 1
                node.value = value
            else:
                node.equal = self._insert(node.equal, key, current + 1, value)
                node.equal.parent = node
        else:
            if key[current] < node.ch:
                node.less = self._insert(node.less, key, current, value)
                node.less.parent = node
            else:
                node.greater = self._insert(node.greater, key, current, value)
                node.greater.parent = node
        return node

    def __getitem__(self, item):
        assert isinstance(item, str)
        node = self._find_tree_node(item)
        return node.value if node else None

    def __contains__(self, item):
        return self.__getitem__(item) is not None

    def __str__(self):
        return (
            "{"
            + ", ".join(
                map(
                    lambda tuple: "'" + tuple[0] + "'" + ": " + str(tuple[1]),
                    list(self._get_key_values(self._root, "")),
                )
            )
            + "}"
        )

    def remove(self, item):
        node = self._find_tree_node(item)
        remove_result = True if node is not None and node.value is not None else False
        if node:
            # TODO looks like something wrong with `remove`
            node.value = None
            while node.parent is not None and self._is_leaf(node):
                parent = node.parent
                if parent.less == node:
                    parent.less = None
                elif parent.greater == node:
                    parent.greater = None
                else:
                    parent.equal = None
                node = parent
        if remove_result:
            self._total -= 1
        return remove_result

    def contains_prefix(self, prefix):
        # TODO looks like it is affected by remove
        result = list(self.get_key_values_with_prefix(prefix))
        return len(result) > 0

    def get_key_values_with_prefix(self, prefix):
        node = self._find_tree_node(prefix)
        return self._get_key_values(node.equal, prefix) if node else []

    def _find_tree_node(self, prefix):
        node, current = self._root, 0
        while node:
            if node.ch == prefix[current]:
                if current == len(prefix) - 1:
                    break
                else:
                    node = node.equal
                    current += 1
            elif node.ch > prefix[current]:
                node = node.less
            else:
                node = node.greater
        return node

    def _get_key_values(self, node, base_string):
        if node:
            # need to double check base_string itself
            if node.parent and node.parent.value is not None:
                yield base_string, node.parent.value
            stack = [(node, base_string)]
            while stack:
                current_node, string = stack.pop()
                # key-value is found
                if current_node.value is not None:
                    yield string + current_node.ch, current_node.value
                # in order to guarantee lexicographical order, traverse in pre-order
                if current_node.greater:
                    stack.append((current_node.greater, string))
                if current_node.equal:
                    stack.append((current_node.equal, string + current_node.ch))
                if current_node.less:
                    stack.append((current_node.less, string))
        else:
            return []

    def _is_leaf(self, node):
        return (
            node.value is None
            and node.less is None
            and node.greater is None
            and node.equal is None
        )
