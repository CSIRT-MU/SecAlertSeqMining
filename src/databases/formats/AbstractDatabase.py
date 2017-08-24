""" Abstract classes for creating various databases.
"""

import os
from abc import abstractmethod, ABCMeta
from collections import defaultdict


class AbstractDatabase(metaclass=ABCMeta):
    def __init__(self, output_dir, file_suffix=None):
        self.output_dir = output_dir
        self.file_suffix = file_suffix

        # Dictionary providing mapping between integer and string representations of items.
        self.item_map = defaultdict(lambda: len(self.item_map))

    @abstractmethod
    def read(self, alert):
        """ Process alert - add alert into inner object structure representing sequential database. """

    @abstractmethod
    def save(self):
        """ Save database into file. """

    @property
    @abstractmethod
    def format_description(self) -> str:
        """ One word describing format of output database. E.g. 'basic', 'timed' """

    @property
    @abstractmethod
    def tid_description(self) -> str:
        """ Short description of transaction ID. Will be used to name output files. E.g. 'src-tar' """

    def output_file_path(self) -> str:
        suffix = f"-{self.file_suffix}" if self.file_suffix else ''
        path = f"{self.output_dir}/{self.format_description}/{self.tid_description}{suffix}"
        path = os.path.normpath(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return path

    @abstractmethod
    def len_sequences(self) -> int:
        """
        :return: number of sequences in database
        """

    def save_item_map(self):
        with open(f"{self.output_file_path()}.map", 'w') as f:
            for key, value in self.item_map.items():
                print("{},{}".format(value, key), file=f)
