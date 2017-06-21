"""
    This class map strings to numerical indexes and vice versa,
    .map file is created to maintain pairs of indexes and strings.
"""

from bintrees import FastAVLTree


class ItemMap:
    INDEX_PREFIX = '123'

    def __init__(self):
        self.item_list = {}                 # Just for loading
        self.item_tree = FastAVLTree()      # Just for saving
        self.index_counter = 0

    def str_to_index(self, string):
        """
        Use AVL tree to store index map
        :param string:
        :return: index
        """
        value = self.item_tree.set_default(string, self.index_counter)
        if value == self.index_counter:
            self.index_counter += 1
        return self.INDEX_PREFIX + str(value)

    def save_map(self, file_path):
        """
        Use AVL tree to save map
        :param file_path:
        :return:
        """
        with open(file_path + ".map", 'w') as file:
            for key, index in self.item_tree.items():
                file.write(str(index) + " " + key + '\n')

    def load_map(self, file_path):
        with open(file_path + ".map", 'r') as file:
            for line in file.readlines():
                values = line.split(" ")
                if len(values) == 2:
                    self.item_list[int(values[0])] = values[1].strip()

    def index_to_str(self, index):
        index = index[1:] if index.startswith('}') else index
        index = index[1:] if index.startswith('{') else index

        if not index.startswith(self.INDEX_PREFIX):
            return index

        try:
            index_without_prefix = int(index[len(self.INDEX_PREFIX):])
            return self.item_list[index_without_prefix]
        except (KeyError, ValueError):
            return index
