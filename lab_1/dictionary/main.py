"""Binary-search-tree based English-Russian dictionary with JSON persistence."""

import json
from pathlib import Path

class DictionaryNode:
    """A single node of the BST. Internal use only."""
    def __init__(self, k, v, left_child=None, right_child=None):
        self._key = k
        self._value = v
        self._left_child = left_child
        self._right_child = right_child

    def __str__(self):
        return f"{self._key} : {self._value}"

class Dictionary:
    """Unbalanced BST mapping string keys to string values.

    Keys are stored in sorted order, so pack_dictionary() returns pairs
    in ascending key order. The tree is not self-balancing.
    """
    def __init__(self):
        self._root = None
        self._size = 0

    def add_node(self, k, v):
        """Insert a new pair or update the value of an existing key.

        Returns:
            True if a new node was added, False if an existing key was updated.
        """

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
        """Return the value associated with key k.

        Raises:
            KeyError: if k is not in the dictionary.
        """

        cur_node = self._root
        while cur_node is not None and cur_node._key != k:
            if  k < cur_node._key:
                cur_node = cur_node._left_child
            elif k > cur_node._key:
                cur_node = cur_node._right_child
        if cur_node is None or cur_node._key != k:
            raise KeyError(f"Word {k} not found")
        return cur_node._value

    def delete_node(self, k):
        """Remove the pair with key k.

        Returns:
            True if the key was found and removed, False otherwise.
        """

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

            cur_node._key = replace_node._key
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
        """Return all pairs as a plain dict, ordered by ascending key."""
        def traverse(node):
            if node is None:
                return
            yield from traverse(node._left_child)
            yield node._key, node._value
            yield from traverse(node._right_child)

        return dict(traverse(self._root))

    def save_dictionary(self, path):
        """Write the dictionary to a UTF-8 JSON file.

        The file is created or overwritten. Non-ASCII characters are preserved.

        Raises:
            OSError: if the file cannot be written.
        """
        path = Path(path)
        data = self.pack_dictionary()
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_dictionary(self, path):
        """Replace the dictionary contents with data from a JSON file.

        The file must contain a JSON object with string keys and string values.
        If validation fails, the current dictionary is left untouched.

        Raises:
            FileNotFoundError: if the file does not exist.
            json.JSONDecodeError: if the file is not valid JSON.
            TypeError: if the JSON root is not an object, or any key/value
                is not a string.
        """
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise TypeError(f"Expected JSON object, got {type(data).__name__}")

        temp_dict = Dictionary()
        for k, v in data.items():
            if not isinstance(k, str):
                raise TypeError(f"Key must be str, got {type(k).__name__}: {k}")
            if not isinstance(v, str):
                raise TypeError(f"Value must be str, got {type(v).__name__}: {v}")
            temp_dict.add_node(k, v)

        self._root = temp_dict._root
        self._size = temp_dict._size

def show_menu():
    """Print the main menu."""
    print("-------------MENU-------------")
    print("1. Show dictionary")
    print("2. Add/edit translation")
    print("3. Find translation")
    print("4. Delete translation")
    print("5. Show the size of dictionary")
    print("6. Save dictionary to file")
    print("7. Load dictionary from file")
    print("0. Exit")
    print("------------------------------")


def main():
    d = Dictionary()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        match choice:
            case "1":
                print("----------DICTIONARY----------")
                for k, v in d.pack_dictionary().items():
                    print(f"{k} : {v}")
            case "2":
                k = input("Enter word in english: ")
                v = input("Enter translation: ")
                if d.add_node(k, v):
                    print("Translation added")
                else:
                    print("Translation edited")
            case "3":
                k = input("Enter word in english: ")
                try:
                    print(f"Translation: {d.find_node(k)}")
                except KeyError as e:
                    print(e)
            case "4":
                k = input("Enter word in english: ")
                if d.delete_node(k):
                    print("Translation deleted")
                else:
                    print("Translation not found")
            case "5":
                print(f"Size of dictionary: {len(d)}")
            case "6":
                file_name = input("Enter file name: ")
                try:
                    d.save_dictionary(file_name)
                    print(f"Dictionary saved to the file {file_name}")
                except OSError as e:
                    print(f"Could not save: {e}")
            case "7":
                file_name = input("Enter file name: ")
                try:
                    d.load_dictionary(file_name)
                    print(f"Dictionary loaded from file {file_name}")
                except FileNotFoundError:
                    print("File not found")
                except json.JSONDecodeError:
                    print("File is not valid JSON")
                except TypeError as e:
                    print(f"Wrong data in file: {e}")
            case "0":
                print("Exiting...")
                break
            case _:
                print("Input error")

if __name__ == "__main__":
    main()
