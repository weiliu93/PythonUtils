from collections import MutableMapping
import os
import shutil

from doubly_linkedlist import DoublyLinkedList
from bucket_memory_doubly_linkedlist import BucketMemoryDoublyLinkedList
from bucket import Bucket, BucketObject


class DiskBasedHashMap(MutableMapping):
    """Disk Based Hash Map, spill data to disk when exceeding memory threshold. Non thread safe implementation"""

    def __init__(self, work_dir=None, bucket_num=4, memory_threshold=64 * 1024):
        if not work_dir:
            work_dir = os.path.join(os.curdir, "buckets")
        # force cleanup
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        os.mkdir(work_dir)
        # all buckets stored here
        self._work_dir = work_dir
        # data spilling threshold, default is 64M. `0` means it works in absolutely disk mode
        self._memory_threshold = (
            64 * 1024 if memory_threshold is None else max(memory_threshold, 0)
        )
        # total number of bucket, it should always be power of two
        self._bucket_num = self._power_of_two_ceiling(
            4 if bucket_num is None else max(bucket_num, 1)
        )
        # buckets
        self._buckets = [
            Bucket(
                os.path.abspath(os.path.join(work_dir, "bucket_{}.txt".format(index)))
            )
            for index in range(self._bucket_num)
        ]
        # bucket memory doubly linked list for BucketObject
        self._in_memory_objects = BucketMemoryDoublyLinkedList()
        # all disk objects' memory usage are same
        self._disk_objects = DoublyLinkedList()
        # object -> in_memory list_node or disk list_node
        self._object_to_list_node = {}

    def __getitem__(self, item):
        """Get corresponding value for given key, one thing need to be mentioned here is
           value's update outside of this dict may not come into effect inside this dict
           since that value could be a disk object, you need to use `set` to guarantee your
           update is persisted
        """
        bucket = self._buckets[self._index(item)]
        for node in bucket.linked_list:
            bucket_object_key, bucket_object_value = node.value
            assert isinstance(bucket_object_key, BucketObject)
            assert isinstance(bucket_object_value, BucketObject)
            if bucket_object_key.load_value() == item:
                key_list_node, value_list_node = (
                    self._object_to_list_node[bucket_object_key],
                    self._object_to_list_node[bucket_object_value],
                )
                # update in-memory and disk linked list
                self._in_memory_objects.remove_and_append(key_list_node)
                self._in_memory_objects.remove_and_append(value_list_node)
                self._disk_objects.remove_and_append(key_list_node)
                self._disk_objects.remove_and_append(value_list_node)
                # balance memory usage
                self._balance()
                return bucket_object_value.load_value()
        raise KeyError("Key `{}` is not exists".format(item))

    def __setitem__(self, key, value):
        """Update key-value pair if key existing, otherwise add a new key-value pair"""
        bucket = self._buckets[self._index(key)]
        for node in bucket.linked_list:
            # key, value pair stored in bucket linked list
            bucket_object_key, bucket_object_value = node.value
            assert isinstance(bucket_object_key, BucketObject)
            assert isinstance(bucket_object_value, BucketObject)
            if bucket_object_key.load_value() == key:
                key_list_node, value_list_node = (
                    self._object_to_list_node[bucket_object_key],
                    self._object_to_list_node[bucket_object_value],
                )
                # update key_list_node and remove value_list_node
                self._in_memory_objects.remove_and_append(key_list_node)
                self._disk_objects.remove_and_append(key_list_node)
                self._in_memory_objects.remove(value_list_node)
                self._disk_objects.remove(value_list_node)
                self._object_to_list_node.pop(bucket_object_value)
                # append value list node to in-memory linked list
                bucket_object_value.value = value
                self._object_to_list_node[
                    bucket_object_value
                ] = DoublyLinkedList.create_new_node(bucket_object_value)
                self._in_memory_objects.append(
                    self._object_to_list_node[bucket_object_value]
                )
                # balance memory usage
                self._balance()
                return
        # append key-value pair to current bucket
        bucket_object_key, bucket_object_value = (
            BucketObject(key, bucket),
            BucketObject(value, bucket),
        )
        bucket.linked_list.append(
            DoublyLinkedList.create_new_node((bucket_object_key, bucket_object_value))
        )
        # append key_object and value_object to in_memory_objects
        key_list_node = DoublyLinkedList.create_new_node(bucket_object_key)
        self._in_memory_objects.append(key_list_node)
        value_list_node = DoublyLinkedList.create_new_node(bucket_object_value)
        self._in_memory_objects.append(value_list_node)
        # update object -> list node dict
        self._object_to_list_node[bucket_object_key] = key_list_node
        self._object_to_list_node[bucket_object_value] = value_list_node
        # balance memory usage
        self._balance()

    def __delitem__(self, key):
        """Del key-value pair from dict"""
        bucket = self._buckets[self._index(key)]
        for node in bucket.linked_list:
            bucket_object_key, bucket_object_value = node.value
            if bucket_object_key.load_value() == key:
                # remove objects from object -> list_node dict
                key_list_node = self._object_to_list_node.pop(bucket_object_key)
                value_list_node = self._object_to_list_node.pop(bucket_object_value)
                # remove list_node from in_memory and disk objects
                self._in_memory_objects.remove(key_list_node)
                self._in_memory_objects.remove(value_list_node)
                self._disk_objects.remove(key_list_node)
                self._disk_objects.remove(value_list_node)
                # remove node from bucket linked list
                assert bucket.linked_list.remove(node) == True
                self._balance()
                return
        raise KeyError("Key `{}` is not exists".format(key))

    def __iter__(self):
        """Return all keys"""
        for bucket in self._buckets:
            for node in bucket.linked_list:
                bucket_key_object, _ = node.value
                yield bucket_key_object.load_value()

    def __str__(self):
        return str(list(self))

    def __len__(self):
        # Since we store key-value pair both, it means the total amount of objects is even
        assert len(self._object_to_list_node) % 2 == 0
        return len(self._object_to_list_node) // 2

    def clear(self):
        """Default implementation is inefficient"""
        self._in_memory_objects.clear()
        self._disk_objects.clear()
        self._object_to_list_node.clear()
        for bucket in self._buckets:
            bucket.clear()

    def compact(self):
        """Compact all disk buckets, save disk space and speed up disk data lookup"""

        # create a collection list for each bucket
        bucket_to_list_node_dict = {}
        # we need to ensure all buckets should have a collection list
        for bucket in self._buckets:
            bucket_to_list_node_dict[bucket] = []
        for node in self._disk_objects:
            bucket_object = node.value
            assert not bucket_object.is_in_memory()
            bucket_to_list_node_dict[bucket_object.bucket].append(node)
        # bucket by bucket processing
        for bucket, node_list in bucket_to_list_node_dict.items():
            with open(bucket.filepath, "rb") as source_file:
                tmp_filepath = bucket.filepath + ".tmp"
                tmp_offset, tmp_addresses = 0, []
                with open(tmp_filepath, "wb") as target_file:
                    # copy bytes from filepath to tmp_filepath
                    for node in node_list:
                        bucket_object = node.value
                        source_file.seek(bucket_object.value.address)
                        header = source_file.read(4)
                        data_length = self._byte_array_to_integer(header)
                        data = source_file.read(data_length)
                        target_file.write(header + data)
                        tmp_addresses.append(tmp_offset)
                        tmp_offset += len(header + data)
                # swap files in physical disk
                os.rename(tmp_filepath, bucket.filepath)
                # remove all bucket_object from object_to_list_node dict
                for node in node_list:
                    self._object_to_list_node.pop(node.value)
                # update disk address and object_to_list_node dict
                for node, address in zip(node_list, tmp_addresses):
                    bucket_object = node.value
                    bucket_object.value.address = address
                    self._object_to_list_node[bucket_object] = node
                # update bucket's offset, very important in compaction
                bucket._offset = tmp_offset

    def _balance(self):
        """Maintain a sliding windows, ensure memory usage is under threshold"""

        # first try to load disk object to memory
        while (
            self._in_memory_objects.memory_usage < self._memory_threshold
            and len(self._disk_objects) > 0
        ):
            node = self._disk_objects.pop_last()
            bucket_object = node.value
            # remove object from inverted dict
            self._object_to_list_node.pop(bucket_object)
            # load object from memory
            bucket_object.value = bucket_object.load_value()
            self._object_to_list_node[bucket_object] = node
            self._in_memory_objects.add_first(node)
        # then persist extra objects to disk based on LRU rule
        while self._in_memory_objects.memory_usage > self._memory_threshold:
            node = self._in_memory_objects.pop_first()
            bucket_object = node.value
            # remove object from inverted dict
            self._object_to_list_node.pop(bucket_object)
            # persist object to disk, update bucket_object's value
            disk_value = bucket_object.bucket.persist_value(bucket_object.value)
            bucket_object.value = disk_value
            self._object_to_list_node[bucket_object] = node
            self._disk_objects.append(node)

    def _power_of_two_ceiling(self, number):
        ans = 1
        while ans < number:
            ans <<= 1
        return ans

    def _byte_array_to_integer(self, byte_array):
        ans = 0
        for b in byte_array:
            ans = (ans << 8) + int(b)
        return ans

    def _index(self, obj):
        """since bucket_num is power of two, bit operation could benefit us here"""
        return hash(obj) & (self._bucket_num - 1)
