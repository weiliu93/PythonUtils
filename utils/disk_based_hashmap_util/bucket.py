import pickle

from doubly_linkedlist import DoublyLinkedList


class Bucket(object):
    def __init__(self, filepath):
        self._filepath = filepath
        # create a new file or overwrite it
        open(self._filepath, "wb").close()
        self._offset = 0
        # linked list node's value is key-value pair, key and value are BucketObject
        self._linked_list = DoublyLinkedList()

    def __str__(self):
        return "(filepath: {}, offset: {}, linked_list: {})".format(
            self._filepath, self._offset, self._linked_list
        )

    @property
    def filepath(self):
        return self._filepath

    @property
    def linked_list(self):
        return self._linked_list

    def persist_value(self, value):
        with open(self.filepath, "ab") as f:
            pickle_value = pickle.dumps(value)
            # final byte array need to be flushed
            byte_array = self._integer_to_byte_array(len(pickle_value)) + pickle_value
            f.write(byte_array)
            address = self._offset
            self._offset += len(byte_array)
            return DiskAddress(address)

    def clear(self):
        open(self._filepath, "wb").close()
        self._offset = 0
        self._linked_list.clear()

    def _integer_to_byte_array(self, length):
        byte_array = bytearray(4)
        byte_array[0] = (length >> 24) & ((1 << 8) - 1)
        byte_array[1] = (length >> 16) & ((1 << 8) - 1)
        byte_array[2] = (length >> 8) & ((1 << 8) - 1)
        byte_array[3] = length & ((1 << 8) - 1)
        return bytes(byte_array)


class BucketObject(object):
    def __init__(self, value, bucket):
        self.value = value
        self.bucket = bucket

    def load_value(self):
        if isinstance(self.value, DiskAddress):
            # TODO it is time costly in most cases, need to find a way to optimize it
            with open(self.bucket.filepath, "rb") as f:
                f.seek(self.value.address)
                data_length = self._byte_array_to_integer(f.read(4))
                value_byte_array = f.read(data_length)
                return pickle.loads(value_byte_array)
        else:
            return self.value

    def _byte_array_to_integer(self, byte_array):
        ans = 0
        for b in byte_array:
            ans = (ans << 4) + int(b)
        return ans

    def is_in_memory(self):
        return not isinstance(self.value, DiskAddress)

    def __str__(self):
        # load could be a costly operation, just print value object itself without loading
        return str(self.value)


class DiskAddress(object):
    def __init__(self, address):
        self.address = address

    def __str__(self):
        return "(address: {})".format(self.address)
