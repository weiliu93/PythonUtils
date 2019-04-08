import pickle
import hashlib
import random
import builtins
import itertools


class CuckooFilter(object):
    class Bucket(object):
        """Bucket used to store bunch of fingerprints"""

        def __init__(self, bucket_size, index):
            self._bucket_size = bucket_size
            self._index = index
            # use "" as empty slot
            self._bucket_array = ["" for _ in range(bucket_size)]

        @property
        def index(self):
            return self._index

        def __contains__(self, item):
            return item in self._bucket_array

        def __len__(self):
            return self.size()

        def __str__(self):
            return "[" + ", ".join(map(str, self._bucket_array)) + "]"

        def __iter__(self):
            return itertools.filterfalse(lambda item: item is "", self._bucket_array)

        def remove(self, item):
            """remove item from bucket_array if exists"""
            if item in self._bucket_array:
                self.replace(item)
                return True
            else:
                return False

        def add(self, item):
            """replace empty slot with item"""
            if "" in self._bucket_array:
                self.replace("", item)
                return True
            else:
                return False

        def replace(self, item, substitution=""):
            """replace item with substitution"""
            if item in self._bucket_array:
                self._bucket_array.remove(item)
                self._bucket_array.append(substitution)
                return True
            else:
                return False

        def random_choice(self):
            candidates = list(
                builtins.filter(lambda item: item != "", self._bucket_array)
            )
            return random.choice(candidates)

        def is_full(self):
            return self.size() == self._bucket_size

        def is_empty(self):
            return self.size() == 0

        def size(self):
            return sum(map(lambda item: item != "", self._bucket_array))

        def clear(self):
            self._bucket_array = ["" for _ in range(self._bucket_size)]

    def __init__(self, bucket_size=4, array_size=1 << 16, substitution_limit=100):
        self._array_size = self._ceiling_power_of_two(array_size)
        self._buckets = [
            self.Bucket(bucket_size=bucket_size, index=index)
            for index in range(self._array_size)
        ]
        self._substitution_limit = substitution_limit
        self._size = 0

    def add(self, key):
        """key should be hashable"""
        assert hasattr(key, "__hash__")
        fingerprint, index, another_index = self._fetch_item_info(key)
        bucket_1, bucket_2 = self._buckets[index], self._buckets[another_index]
        # if fingerprint exists
        if fingerprint in bucket_1 or fingerprint in bucket_2:
            return False
        # flag used to represents if insert succeeded
        add_succeeded = True
        if self._substitution(bucket_1):
            assert bucket_1.add(fingerprint) == True
        elif self._substitution(bucket_2):
            assert bucket_2.add(fingerprint) == True
        else:
            # if substitution failed, it means insert failed
            add_succeeded = False
        self._size += int(add_succeeded)
        return add_succeeded

    def remove(self, key):
        """key should be hashable"""
        assert hasattr(key, "__hash__")
        fingerprint, index, another_index = self._fetch_item_info(key)
        # check both buckets
        bucket_1, bucket_2 = self._buckets[index], self._buckets[another_index]
        exists = key in self
        bucket_1.replace(fingerprint)
        bucket_2.replace(fingerprint)
        self._size -= int(exists)
        return exists

    def clear(self):
        for bucket in self._buckets:
            bucket.clear()
        self._size = 0

    def __contains__(self, item):
        assert hasattr(item, "__hash__")
        fingerprint, index, another_index = self._fetch_item_info(item)
        # check if fingerprint exists in buckets
        return (fingerprint in self._buckets[index]) or (
            fingerprint in self._buckets[another_index]
        )

    def __len__(self):
        return self._size

    def __iter__(self):
        return itertools.chain(*self._buckets)

    def __str__(self):
        return "[" + ", ".join(map(str, list(self))) + "]"

    def _fetch_item_info(self, item):
        fingerprint = self._fingerprint(item)
        index = self._index_key(item)
        another_index = index ^ self._index_fingerprint(fingerprint)
        return fingerprint, index, another_index

    def _index_key(self, key):
        return hash(key) & (self._array_size - 1)

    def _index_fingerprint(self, fingerprint):
        # fingerprint in hex
        result = 0
        for hex_ch in fingerprint:
            result = ((result << 4) + int(hex_ch, 16)) & (self._array_size - 1)
        return result

    def _fingerprint(self, item):
        # try to convert item into a byte_array, object should be pickle-able
        byte_array = pickle.dumps(item)
        # create digest for given byte_array
        hash = hashlib.md5()
        hash.update(byte_array)
        # digest string in hex
        return hash.hexdigest()

    def _ceiling_power_of_two(self, value):
        value = 0 if value is None else value
        ans = 1
        while ans < value:
            ans <<= 1
        return ans

    def _substitution(self, start_bucket):
        substitution_chain = []
        vis_set, sub_cnt, current_bucket = set(), 0, start_bucket
        # linear probing, not exhausted search, since solution space could be very huge
        while (
            current_bucket.is_full()
            and current_bucket not in vis_set
            and sub_cnt < self._substitution_limit
        ):
            vis_set.add(current_bucket)
            fingerprint = current_bucket.random_choice()
            substitution_chain.append((current_bucket, fingerprint))
            # jump to next bucket
            current_bucket = self._buckets[
                current_bucket.index ^ self._index_fingerprint(fingerprint)
            ]
            sub_cnt += 1
        if not current_bucket.is_full():
            # substitute in reversed order
            for bucket, fingerprint in reversed(substitution_chain):
                another_bucket = self._buckets[
                    bucket.index ^ self._index_fingerprint(fingerprint)
                ]
                assert bucket.remove(fingerprint) == True
                assert another_bucket.add(fingerprint) == True
            return True
        else:
            return False
