import sys
import os
import inspect
import shutil


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
        work_dir=test_case_package, memory_threshold=1024, bucket_num=2
    )
    for i in range(10):
        disk_map[i] = i + 10

    for i in range(10):
        assert disk_map[i] == i + 10

    for i in range(10):
        del disk_map[i]

    assert list(disk_map) == []

    _clean_up(test_case_package)


# TODO add more test cases


def _clean_up(test_case_package):
    shutil.rmtree(test_case_package)
    os.mkdir(test_case_package)
