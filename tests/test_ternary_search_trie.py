import sys
import os
import random


sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from ternary_search_trie import TernarySearchTrie


def test_basic_tst_operations():
    trie = TernarySearchTrie()
    trie["a"] = 10
    trie["b"] = "sdf"

    assert trie["a"] == 10
    assert trie["b"] == "sdf"

    trie["a"] = "xyz"

    assert trie["a"] == "xyz"
    assert trie["b"] == "sdf"

    assert len(trie) == 2

    del trie["a"]
    assert len(trie) == 1

    del trie["c"]
    assert len(trie) == 1


def test_tst_overwrite_insert():
    trie = TernarySearchTrie()

    trie["a"] = "dsf"
    assert trie["a"] == "dsf"

    trie["a"] = "23"
    assert trie["a"] == "23"


def test_tst_insert_then_remove():
    trie = TernarySearchTrie()

    trie["a"] = "Sdf"
    assert trie["a"] == "Sdf"

    del trie["a"]
    assert trie["a"] == None


def test_tst_remove_another_key():
    trie = TernarySearchTrie()

    trie["a"] = "Sbds"
    del trie["b"]

    assert len(trie) == 1
    assert trie["a"] == "Sbds"


def test_tst_items():
    trie = TernarySearchTrie()

    keys = list(map(lambda node: str(node), range(100)))
    values = list(range(100))

    key_value_pairs = list(zip(keys, values))
    key_value_pairs.sort()

    for key, value in key_value_pairs:
        trie[key] = value

    next_index = 0
    for key, value in sorted(list(trie.items())):
        assert key , value == key_value_pairs[next_index]
        next_index += 1


def test_tst_get_key_values_with_prefix():
    trie = TernarySearchTrie()

    trie["a"] = "Sdf"
    trie["abs"] = "e2rf"
    trie["azbdsf"] = "23r"
    trie["bsdf"] = "b2r"
    trie["csdf"] = "232"

    items = sorted(list(trie.get_key_values_with_prefix("a")))

    assert items[0] == ("a", "Sdf")
    assert items[1] == ("abs" , "e2rf")
    assert items[2] == ("azbdsf", "23r")


def test_tst_contains_prefix():
    trie = TernarySearchTrie()

    trie["absd"] = "Bsadf"
    trie["absdf"] = "sadf"
    trie["acsd"] = "wef"
    trie["bdsf"] = "few"

    assert trie.contains_prefix("a") == True
    assert trie.contains_prefix("ab") == True
    assert trie.contains_prefix("ac") == True
    assert trie.contains_prefix("bds") == True


def test_tst_clear():
    trie = TernarySearchTrie()

    trie["bsdf"] = "23f2"
    trie["2eb"] = "f23"
    trie.clear()

    assert len(trie) == 0
    assert trie["bsdf"] == None
    assert trie["2eb"] == None


def test_tst_insert_order_will_not_affect_final_result():
    trie1 = TernarySearchTrie()

    trie1["ads"] = "bvdsf"
    trie1["bdsf"] = "2f2e"
    trie1["xcv"] = "f32"

    assert list(trie1.items()) == [("ads", "bvdsf"), ("bdsf", "2f2e"), ("xcv", "f32")]

    trie2 = TernarySearchTrie()

    trie2["bdsf"] = "2f2e"
    trie2["xcv"] = "f32"
    trie2["ads"] = "bvdsf"

    assert list(trie2.items()) == [("ads", "bvdsf"), ("bdsf", "2f2e"), ("xcv", "f32")]


def test_tst_compared_with_hashmap():
    trie = TernarySearchTrie()
    hashmap = dict()

    for _ in range(10000):
        key = _random_string(3)
        value = _random_string(5)
        trie[key] = value
        hashmap[key] = value

        key_value_pair_1 = sorted(list(trie.items()))
        key_value_pair_2 = sorted(list(hashmap.items()))

        assert key_value_pair_1 == key_value_pair_2


def test_tst_remove():
    trie = TernarySearchTrie()

    for i in range(10):
        trie[str(i)] = i

    for i in range(10):
        assert len(trie) == 10 - i
        del trie[str(i)]


def test_real_scenario():

    def get_key_value_with_prefix_in_hashmap(hashmap, prefix):
        ans = []
        for key, value in hashmap.items():
            if key.startswith(prefix):
                ans.append((key, value))
        return ans

    def contains_prefix_in_hashmap(hashmap, prefix):
        for key, value in hashmap.items():
            if key.startswith(prefix):
                return True
        return False

    trie = TernarySearchTrie()
    hashmap = dict()
    ops = ["set", "get", "remove", "get_prefix", "check_prefix", "contains"]
    for _ in range(200000):
        op = random.choice(ops)
        if op == "set":
            key = _random_string(3)
            value = _random_string(5)
            trie[key] = value
            hashmap[key] = value
        elif op == "get":
            key = _random_string(3)
            assert trie[key] == hashmap.get(key, None)
        elif op == "remove":
            key = _random_string(3)
            assert trie[key] == hashmap.get(key, None)
            if trie[key]:
                del trie[key]
                del hashmap[key]
        elif op == "get_prefix":
            prefix = _random_string(2)
            key_value_pair_1 = sorted(trie.get_key_values_with_prefix(prefix))
            key_value_pair_2 = sorted(get_key_value_with_prefix_in_hashmap(hashmap, prefix))
            assert key_value_pair_1 == key_value_pair_2
        elif op == "check_prefix":
            prefix = _random_string(2)
            assert contains_prefix_in_hashmap(hashmap, prefix) == trie.contains_prefix(prefix)
        elif op == "contains":
            key = _random_string(3)
            assert (key in hashmap) == (key in trie)
        key_value_pair_1 = sorted(list(hashmap.items()))
        key_value_pair_2 = sorted(list(trie.items()))
        assert key_value_pair_1 == key_value_pair_2
        assert len(hashmap) == len(trie)


def _random_string(length, charset="abcd"):
    result = ""
    for _ in range(length):
        result += random.choice(charset)
    return result