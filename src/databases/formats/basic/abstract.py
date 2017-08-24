import typing
from collections import defaultdict

from ..AbstractDatabase import AbstractDatabase


class Basic(AbstractDatabase):
    """ Sequential database format.
        * items inside itemset are divided by ' '
        * itemsets inside sequence are divided by '-1'
        * each sequence is on separate line and ends with '-2'
    """
    SEPARATOR = " -1 "
    END_OF_LINE = "-2\n"

    format_description = "basic"

    def __init__(self, output_dir, file_suffix=''):
        super().__init__(output_dir, file_suffix)

        from bintrees import FastRBTree
        self.sequences = defaultdict(FastRBTree)

    def len_sequences(self) -> int:
        return len(self.sequences)

    def _read(self, sequence_key: typing.Hashable, itemset_key, items):
        self.sequences[sequence_key] \
            .set_default(itemset_key, set()) \
            .update(items)

    def save(self):
        with open(self.output_file_path(), 'w') as file:
            for tree in self.sequences.values():
                for items in tree.values():
                    file.write(" ".join(map(lambda x: str(self.item_map[x]), items)))
                    file.write(self.SEPARATOR)
                file.write(self.END_OF_LINE)

        self.save_item_map()