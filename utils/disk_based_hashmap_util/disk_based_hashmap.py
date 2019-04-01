from collections import MutableMapping
import pickle
import os
import shutil

from pympler import asizeof
import mmh3

from doubly_linkedlist import DoublyLinkedList
from bucket import Bucket, BucketObject


class DiskBasedHashMap(MutableMapping):
    """Disk Based Hash Map, spill data to disk when exceeding memory threshold"""

    def __init__(self, work_dir=None, bucket_num=None, memory_threshold=None):
        if not work_dir:
            work_dir = os.path.join(os.curdir, "buckets")
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)
        os.mkdir(work_dir)
        # all buckets stored here
        self._work_dir = work_dir
        # data spilling threshold, default is 1G
        self._memory_threshold = memory_threshold or 1024 * 1024
        # total number of bucket, it should always be power of two
        self._bucket_num = self._power_of_two_ceiling(bucket_num) or 256
        # buckets
        self._buckets = [
            Bucket(os.path.join(work_dir, "bucket_{}".format(index)))
            for index in range(self._bucket_num)
        ]
        # in-memory object linked list and disk object linked list, value is BucketObject
        self._in_memory_objects = DoublyLinkedList()
        self._disk_objects = DoublyLinkedList()
        # object -> in_memory list_node or disk list_node
        self._object_to_list_node = {}

    def __getitem__(self, item):
        """raise KeyError"""
        bucket = self._buckets[self._index(item)]
        for node in bucket.linked_list:
            bucket_object_key, bucket_object_value = node.value
            assert isinstance(bucket_object_key, BucketObject)
            assert isinstance(bucket_object_value, BucketObject)
            if bucket_object_key.load_value() == item:
                # move current linked list node to header
                bucket.linked_list.remove_and_add_first(node)
                key_list_node, value_list_node = \
                    self._object_to_list_node[bucket_object_key], self._object_to_list_node[bucket_object_value]
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
        bucket = self._buckets[self._index(key)]
        for node in bucket.linked_list:
            # key, value pair stored in bucket linked list
            bucket_object_key, bucket_object_value = node.value
            assert isinstance(bucket_object_key, BucketObject)
            assert isinstance(bucket_object_value, BucketObject)
            if bucket_object_key.load_value() == key:
                bucket.linked_list.remove_and_add_first(node)
                key_list_node, value_list_node = \
                    self._object_to_list_node[bucket_object_key], self._object_to_list_node[bucket_object_value]
                # update key_list_node and remove value_list_node
                self._in_memory_objects.remove_and_append(key_list_node)
                self._disk_objects.remove_and_append(key_list_node)
                self._in_memory_objects.remove(value_list_node)
                self._disk_objects.remove(value_list_node)
                self._object_to_list_node.pop(bucket_object_value)
                # append value list node to in-memory linked list
                bucket_object_value.value = value
                self._object_to_list_node[bucket_object_value] = DoublyLinkedList.create_new_node(bucket_object_value)
                self._in_memory_objects.append(self._object_to_list_node[bucket_object_value])
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
        """raise KeyError"""
        bucket = self._buckets[self._index(key)]
        node = None
        for node in bucket.linked_list:
            bucket_object_key, bucket_object_value = node.value
            if bucket_object_key.load_value() == key:
                break
        # key is exists
        if node:
            bucket_object_key, bucket_object_value = node.value
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
        else:
            raise KeyError("Key `{}` is not exists".format(key))

    def __iter__(self):
        """return all keys"""
        for bucket in self._buckets:
            for node in bucket.linked_list:
                bucket_key_object, _ = node.value
                yield bucket_key_object.load_value()

    def __str__(self):
        return str(list(self))

    def __len__(self):
        # since we store key-value pair both, it means the total amount of objects is even
        assert len(self._object_to_list_node) % 2 == 0
        return len(self._object_to_list_node) // 2

    def clear(self):
        """default implementation is inefficient"""
        self._in_memory_objects.clear()
        self._disk_objects.clear()
        self._object_to_list_node.clear()
        for bucket in self._buckets:
            bucket.clear()

    def compact(self):
        """compact bucket files"""
        # TODO compact all bucket files, remove redundant storage


        pass

    def _power_of_two_ceiling(self, number):
        ans = 1
        while ans < number:
            ans <<= 1
        return ans

    def _index(self, obj):
        """since bucket_num is power of two, bit operation could benefit us here"""
        return mmh3.hash(str(obj)) & (self._bucket_num - 1)

    def _balance(self):
        # TODO silver bullet



        pass


