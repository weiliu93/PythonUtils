import pickle
import hashlib


class CuckooFilter(object):
    def __init__(self, bucket_num=4, array_size=10007):
        self._bucket_num = bucket_num
        self._array_size = array_size

    def add(self, key):
        """key should be hashable"""

        pass

    def remove(self, key):
        """key should be hashable"""

        pass

    def __contains__(self, item):


        pass

    def __len__(self):


        pass

    def _index(self, key):
        return hash(key) % self._array_size

    def _index_fingerprint(self, item):
        # try to convert item into a byte_array, object should be pickle-able
        byte_array = pickle.dumps(item)
        # create digest for given byte_array
        hash = hashlib.md5()
        hash.update(byte_array)
        # convert digest into integer
        result = 0
        for b in hash.digest():
            result = ((result << 8) + b) % self._array_size
        return result