import sys
import os
import inspect
import shutil
import random


sys.path.append(
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "utils",
        "disk_based_hashmap_util",
    )
)
sys.path.append(
    os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "utils")
)

from disk_based_hashmap_util.disk_based_hashmap import DiskBasedHashMap

package_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "packages", "test_disk_based_hashmap")
)


def test_basic_set_and_get():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        work_dir=test_case_package, memory_threshold=128, bucket_num=2
    )
    for i in range(10):
        disk_map[i] = i + 10

    for i in range(10):
        assert disk_map[i] == i + 10

    for i in range(10):
        del disk_map[i]

    assert list(disk_map) == []

    _clean_up(test_case_package)


def test_set_get_and_del():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_hashmap = DiskBasedHashMap(
        work_dir=test_case_package, memory_threshold=128, bucket_num=2
    )

    keys, values = [], []
    for _ in range(100):
        key, value = random.randint(1, 1000), random.randint(1, 1000)
        while key in keys:
            key = random.randint(1, 1000)
        keys.append(key)
        values.append(value)

    for key, value in zip(keys, values):
        disk_hashmap[key] = value

    key_set = set(keys)
    key_value_pairs = list(zip(keys, values))
    random.shuffle(key_value_pairs)
    for key, value in key_value_pairs:
        assert disk_hashmap[key] == value
        del disk_hashmap[key]

        key_set.remove(key)
        assert set(disk_hashmap.keys()) == key_set

    assert list(disk_hashmap.keys()) == []

    _clean_up(test_case_package)


def test_reset_existing_key():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, work_dir=test_case_package, memory_threshold=128
    )

    # trigger disk spill
    for i in range(10):
        disk_map[i] = i

    disk_map[10] = 20

    assert disk_map[0] == 0

    disk_map[0] = 100

    assert disk_map[0] == 100

    for i in range(1, 10, 1):
        assert disk_map[i] == i

    _clean_up(test_case_package)


def test_get_not_existing_key():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, work_dir=test_case_package, memory_threshold=128
    )

    for i in range(10):
        disk_map[i] = i

    for _ in range(100):
        index = random.randint(1, 1000)
        if index >= 0 and index < 10:
            assert disk_map[index] == index
        else:
            try:
                value = disk_map[index]
                assert False
            except Exception as e:
                assert isinstance(e, KeyError)

    _clean_up(test_case_package)


def test_del_not_existing_key():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, work_dir=test_case_package, memory_threshold=128
    )

    for i in range(10):
        disk_map[i] = i

    try:
        del disk_map[100]
        assert False
    except Exception as e:
        assert isinstance(e, KeyError)

    try:
        del disk_map["sdf"]
        assert False
    except Exception as e:
        assert isinstance(e, KeyError)

    _clean_up(test_case_package)


def test_clear():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, work_dir=test_case_package, memory_threshold=128
    )
    for _ in range(10):
        key, value = random.randint(1, 100), random.randint(1, 100)
        disk_map[key] = value
    disk_map.clear()

    assert list(disk_map) == []

    _clean_up(test_case_package)


def test_iter():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, memory_threshold=128, work_dir=test_case_package
    )

    keys = set()
    for _ in range(100):
        key, value = random.randint(1, 1000), random.randint(1, 1000)
        keys.add(key)
        disk_map[key] = value
    assert sorted(list(disk_map)) == sorted(list(keys))

    _clean_up(test_case_package)


def test_len():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=4, memory_threshold=128, work_dir=test_case_package
    )
    key_set = set()
    for _ in range(1000):
        key = random.randint(1, 100)
        value = random.randint(1, 1000)
        # set
        if random.random() < 0.5:
            disk_map[key] = value
            key_set.add(key)
        else:
            # del
            if key in key_set:
                key_set.remove(key)
                del disk_map[key]
            try:
                del disk_map[key]
            except Exception as e:
                assert isinstance(e, KeyError)
        # assert len
        assert len(disk_map) == len(key_set)

    _clean_up(test_case_package)


def test_compact():
    def bucket_files_size(work_dir):
        result = 0
        for root, dirs, files in os.walk(work_dir):
            for f in files:
                path = os.path.join(root, f)
                result += os.path.getsize(path)
        return result

    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(
        bucket_num=1, memory_threshold=0, work_dir=test_case_package
    )
    for i in range(10):
        disk_map[i] = i
    original_size = bucket_files_size(test_case_package)

    for i in range(1, 10, 1):
        del disk_map[i]
    disk_map.compact()
    compact_size = bucket_files_size(test_case_package)

    assert list(disk_map) == [0] and len(disk_map) == 1

    assert original_size > compact_size

    del disk_map[0]
    disk_map.compact()
    # bucket file should be empty
    assert bucket_files_size(test_case_package) == 0

    assert list(disk_map) == []

    _clean_up(test_case_package)


def test_bucket_offset_before_and_after_compact():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    disk_map = DiskBasedHashMap(bucket_num = 1, memory_threshold = 0, work_dir = test_case_package)
    for i in range(10):
        disk_map[i] = i
    original_offset = disk_map._buckets[0]._offset

    for i in range(1, 10, 1):
        del disk_map[i]
    disk_map.compact()
    current_offset = disk_map._buckets[0]._offset

    assert current_offset < original_offset

    del disk_map[0]
    disk_map.compact()
    assert disk_map._buckets[0]._offset == 0

    _clean_up(test_case_package)


def test_memory_usage_never_exceeding_threshold():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    memory_threshold = 1024
    keys = set()
    disk_map = DiskBasedHashMap(bucket_num = 4, memory_threshold = memory_threshold, work_dir = test_case_package)
    for _ in range(10000):
        key, value = random.randint(1, 100), random.randint(1, 100)
        # set
        if random.random() < 0.7:
            keys.add(key)
            disk_map[key] = value
        else:
            # del
            if key in keys:
                keys.remove(key)
                del disk_map[key]
            else:
                try:
                    del disk_map[key]
                    assert False
                except:
                    pass
        assert keys == set(disk_map.keys()) and len(keys) == len(disk_map)
        if len(keys) == 0:
            assert disk_map._in_memory_objects.memory_usage == 0
        else:
            assert disk_map._in_memory_objects.memory_usage <= memory_threshold

    _clean_up(test_case_package)


def test_real_scenario():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    comp_dict = {}
    disk_map = DiskBasedHashMap(memory_threshold = 1024, bucket_num = 8, work_dir = test_case_package)
    for _ in range(50000):
        key, value = random.randint(1, 300), random.randint(1, 1000)
        # set, get, del, clear
        # 4    3    2     1
        weight_index = random.randint(1, 10)
        if weight_index <= 4:
            disk_map[key] = value
            comp_dict[key] = value
        elif weight_index <= 7:
            assert comp_dict.get(key, None) == disk_map.get(key, None)
        elif weight_index <= 9:
            assert comp_dict.pop(key, None) == disk_map.pop(key, None)
        else:
            comp_dict.clear()
            disk_map.clear()
        key_value_pairs_1 = [(key, value) for key, value in comp_dict.items()]
        key_value_pairs_2 = [(key, value) for key, value in disk_map.items()]
        key_value_pairs_1.sort()
        key_value_pairs_2.sort()
        assert key_value_pairs_1 == key_value_pairs_2

    _clean_up(test_case_package)


def test_real_scenario_with_compaction():
    test_case_package = os.path.join(
        package_root, inspect.currentframe().f_code.co_name
    )
    _clean_up(test_case_package)

    comp_dict = {}
    disk_map = DiskBasedHashMap(memory_threshold=1024, bucket_num=8, work_dir=test_case_package)
    for _ in range(50000):
        key, value = random.randint(1, 300), random.randint(1, 1000)
        # set, get, del, clear, compact
        # 3    3    2     1       1
        weight_index = random.randint(1, 10)
        if weight_index <= 3:
            disk_map[key] = value
            comp_dict[key] = value
        elif weight_index <= 6:
            assert comp_dict.get(key, None) == disk_map.get(key, None)
        elif weight_index <= 8:
            assert comp_dict.pop(key, None) == disk_map.pop(key, None)
        elif weight_index <= 9:
            comp_dict.clear()
            disk_map.clear()
        else:
            disk_map.compact()
        key_value_pairs_1 = [(key, value) for key, value in comp_dict.items()]
        key_value_pairs_2 = [(key, value) for key, value in disk_map.items()]
        key_value_pairs_1.sort()
        key_value_pairs_2.sort()
        assert key_value_pairs_1 == key_value_pairs_2

    _clean_up(test_case_package)


def _clean_up(test_case_package):
    if os.path.exists(test_case_package):
        shutil.rmtree(test_case_package)
    os.mkdir(test_case_package)
