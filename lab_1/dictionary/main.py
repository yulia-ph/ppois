class DictionaryItem:

    def __init__(self, key, value, left_child=None, right_child=None):
        self.key = key
        self.value = value
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return f"{self.key} : {self.value}"

class Dictionary:

    def __init__(self):
        self.root=None
        self.size = 0

    def add_item(self, key, value):
        flag = True
        if not self.root:
            self.root = DictionaryItem(key, value)
            flag = False
        cur_node = self.root
        while flag:
            if key == cur_node.key:
                cur_node.value = value
                return f"The translation of {cur_node.key} is changed to {value}"
            if key < cur_node.key:
                if not cur_node.left_child:
                    cur_node.left_child = DictionaryItem(key, value)
                    break
                cur_node = cur_node.left_child
            elif key > cur_node.key:
                if not cur_node.right_child:
                    cur_node.right_child = DictionaryItem(key, value)
                    break
                cur_node = cur_node.right_child
        self.size += 1
        return f"New translation is added to the dictionary {key} : {value}"

    def find_item(self, key):
        cur_node = self.root
        while cur_node is not None and cur_node.key != key:
            if  key < cur_node.key:
                cur_node = cur_node.left_child
            elif key > cur_node.key:
                cur_node = cur_node.right_child
        if cur_node is None or cur_node.key != key:
            return "failed"
        return cur_node

    def delete_item(self, key):
        prev_node = None
        cur_node = self.root

        while cur_node is not None and cur_node.key != key:
            prev_node = cur_node
            cur_node = cur_node.left_child if key < cur_node.key else cur_node.right_child

        if cur_node is None:
            return "failed"

        if cur_node.left_child is not None and cur_node.right_child is not None:
            prev_replace_node = cur_node
            replace_node = cur_node.right_child

            while replace_node.left_child is not None:
                prev_replace_node = replace_node
                replace_node = replace_node.left_child

            cur_node.key=replace_node.key
            cur_node.value=replace_node.value
            prev_node = prev_replace_node
            cur_node = replace_node

        child = cur_node.left_child if key < cur_node.key else cur_node.right_child

        if prev_node is None:
            self.root = child
        elif cur_node.key < prev_node.key:
            prev_node.left_child = child
        else:
            prev_node.right_child = child
        self.size -= 1
        return "complete"

    def __len__(self):
        return self.size

    def load_dictionary(self):
        pass

    def view_dictionary(self):
        pass
