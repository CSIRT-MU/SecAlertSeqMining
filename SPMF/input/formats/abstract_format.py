""" Abstract formatter classes for creating various databases.
"""

import abc
import os

from SPMF.input.support.item_map import ItemMap


class AbstractFormat:
    FILE_PATH = "databases"
    item_map = ItemMap()

    def __init__(self, file_suffix=''):
        self.FILE_SUFFIX = file_suffix

    @abc.abstractmethod
    def database_description(self):
        """
        :return: string - One word describing format of output database.
        """
        return ""

    @abc.abstractmethod
    def tid_description(self):
        """
        :return: string - Really short description about transaction id. Will be used to name output files.
        """
        return ""

    def file_root(self):
        suffix = "-" + self.FILE_SUFFIX if self.FILE_SUFFIX else ""
        return "{}/{}/{}{}".format(self.FILE_PATH, self.database_description(), self.tid_description(), suffix)

    def file_path(self):
        os.makedirs(os.path.dirname(self.file_root()), exist_ok=True)
        return self.file_root() + ".txt"

    @abc.abstractclassmethod
    def sequences(self):
        """
        :return: Collection of sequences which will be saved into file.
        """
        return []

    @abc.abstractclassmethod
    def save(self):
        pass

    @abc.abstractclassmethod
    def read(self, idea):
        pass


class Basic(AbstractFormat):
    SEPARATOR = " -1 "
    END_OF_LINE = "-2\n"

    def database_description(self):
        return "basic"

    def save(self):
        with open(self.file_path(), 'w') as file:
            print("Going to save {} sequences".format(len(self.sequences())))
            for t in self.sequences():
                for items in t.values():
                    file.write(" ".join(map(self.item_map.str_to_index, items)))
                    file.write(self.SEPARATOR)
                file.write(self.END_OF_LINE)

        print("Data saved, going to save map")
        self.item_map.save_map(self.file_root())
        print("Map saved")


class Timed(AbstractFormat):
    TIME_MARK = "<{}> "
    SEPARATOR = " -1 "
    END_OF_LINE = "-2\n"

    def database_description(self):
        return "timed"

    def save(self):
        with open(self.file_path(), 'w') as file:
            print("Going to save {} sequences".format(len(self.sequences())))
            for tree in self.sequences():
                init_time = tree.min_key()
                for time, items in tree.items():
                    file.write(self.TIME_MARK.format(time - init_time))
                    file.write(" ".join(map(self.item_map.str_to_index, items)))
                    file.write(self.SEPARATOR)
                file.write(self.END_OF_LINE)

        print("Data saved, going to save map")
        self.item_map.save_map(self.file_root())
        print("Map saved")
