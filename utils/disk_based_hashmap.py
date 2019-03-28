from collections import MutableMapping
import pickle

from pympler import asizeof


class DiskBasedHashMap(MutableMapping):
    def __init__(self):
        pass

    def __getitem__(self, item):

        pass

    def __setitem__(self, key, value):

        pass

    def __delitem__(self, key):

        pass

    def __iter__(self):

        pass

    def __len__(self):

        pass

    def clear(self):
        """default implementation is inefficient"""
        pass


class DiskKeyValuePair(object):
    """
    byte_array design
    byte_length:  4     +     4     +     var_length    +     4        +   var_length       +    4
    schema:       header  key_length    key dump object  value_length    value dump object   next_pointer
    """

    def __init__(self, key, value):
        # four bytes header
        self.header = 0
        # temporary variables
        key_dump_result, value_dump_result = pickle.dumps(key), pickle.dumps(value)
        # compute length based on dump result, each of them use four bytes
        self.key_length = len(key_dump_result)
        self.value_length = len(value_dump_result)
        # real key and value, won't be stored in disk
        self.key = key
        self.value = value
        # next pointer, use four byte
        self.next_pointer = -1

    def __setstate__(self, state):
        self.header = self._four_bytes_to_integer(state[0:4])
        self.key_length = self._four_bytes_to_integer(state[4:8])
        self.key = pickle.loads(state[8 : 8 + self.key_length])
        self.value_length = self._four_bytes_to_integer(
            state[8 + self.key_length : 12 + self.key_length]
        )
        self.value = pickle.loads(
            state[12 + self.key_length : 12 + self.key_length + self.value_length]
        )
        self.next_pointer = self._four_bytes_to_integer(state[-4:])

    def __getstate__(self):
        return (
            self._integer_to_four_bytes(self.header)
            + self._integer_to_four_bytes(self.key_length)
            + pickle.dumps(self.key)
            + self._integer_to_four_bytes(self.value_length)
            + pickle.dumps(self.value)
            + self._integer_to_four_bytes(self.next_pointer)
        )

    def __str__(self):
        return "({}, {})".format(str(self.key), str(self.value))

    def _integer_to_four_bytes(self, value):
        byte_array = bytearray(4)
        byte_array[0] = (value >> 24) & ((1 << 8) - 1)
        byte_array[1] = (value >> 16) & ((1 << 8) - 1)
        byte_array[2] = (value >> 8) & ((1 << 8) - 1)
        byte_array[3] = value & ((1 << 8) - 1)
        return bytes(byte_array)

    def _four_bytes_to_integer(self, bytes):
        return (
            (int(bytes[0]) << 24)
            + (int(bytes[1]) << 16)
            + (int(bytes[2]) << 8)
            + int(bytes[3])
        )
