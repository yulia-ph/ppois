import json
from pathlib import Path

class DictionaryNode:

    def __init__(self, k, v, left_child=None, right_child=None):
        self._key = k
        self._value = v
        self._left_child = left_child
        self._right_child = right_child

    def __str__(self):
        return f"{self._key} : {self._value}"

class Dictionary:

    def __init__(self):
        self._root=None
        self._size = 0

    def add_node(self, k, v):
        """Returns True if the node is added to the dictionary, False if edited"""

        if not self._root:
            self._root = DictionaryNode(k, v)
            self._size += 1
            return True

        cur_node = self._root
        while True:
            if k == cur_node._key:
                cur_node._value = v
                return False
            if k < cur_node._key:
                if not cur_node._left_child:
                    cur_node._left_child = DictionaryNode(k, v)
                    break
                cur_node = cur_node._left_child
            elif k > cur_node._key:
                if not cur_node._right_child:
                    cur_node._right_child = DictionaryNode(k, v)
                    break
                cur_node = cur_node._right_child

        self._size += 1
        return True

    def find_node(self, k):
        """Returns True if the node is found in the dictionary, False otherwise"""

        cur_node = self._root
        while cur_node is not None and cur_node._key != k:
            if  k < cur_node._key:
                cur_node = cur_node._left_child
            elif k > cur_node._key:
                cur_node = cur_node._right_child
        if cur_node is None or cur_node._key != k:
            return False
        return True

    def delete_node(self, k):
        """Returns True if the node is deleted from the dictionary, False otherwise"""

        prev_node = None
        cur_node = self._root

        while cur_node is not None and cur_node._key != k:
            prev_node = cur_node
            cur_node = cur_node._left_child if k < cur_node._key else cur_node._right_child

        if cur_node is None:
            return False

        if cur_node._left_child is not None and cur_node._right_child is not None:
            prev_replace_node = cur_node
            replace_node = cur_node._right_child

            while replace_node._left_child is not None:
                prev_replace_node = replace_node
                replace_node = replace_node._left_child

            cur_node._key=replace_node._key
            cur_node._value=replace_node._value
            prev_node = prev_replace_node
            cur_node = replace_node

        child = cur_node._left_child if cur_node._left_child is not None else cur_node._right_child

        if prev_node is None:
            self._root = child
        elif cur_node._key < prev_node._key:
            prev_node._left_child = child
        else:
            prev_node._right_child = child
        self._size -= 1
        return True

    def __len__(self):
        return self._size

    def pack_dictionary(self):
        """Returns a dict of translations from the dictionary"""
        def traverse(node):
            if node is None:
                return
            yield from traverse(node._left_child)
            yield node._key, node._value
            yield from traverse(node._right_child)

        return dict(traverse(self._root))

    def save_dictionary(self, path):
        """Saves the dictionary to the given path"""
        path = Path(path)
        data = self.pack_dictionary()
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_dictionary(self, path):
        """Loads the dictionary from the given path"""
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(f"Expected JSON object, got {type(data).__name__}")

        for k, v in data.items():
            if not isinstance(k, str):
                raise TypeError(f"Key must be str, got {type(k).__name__}: {k}")
            if not isinstance(v, str):
                raise ValueError(f"Value must be str, got {type(v).__name__}: {v}")
            self.add_node(k, v)

