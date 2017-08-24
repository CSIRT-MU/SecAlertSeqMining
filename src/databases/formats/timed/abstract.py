import typing
from collections import defaultdict
from datetime import datetime

from ..AbstractDatabase import AbstractDatabase


class Timed(AbstractDatabase):
    """ Time extended sequential database format.
        * items inside itemset are divided by ' '
        * itemset begins with '<X>' where X is number representing time of occurrence
        * itemsets inside sequence are divided by '-1'
        * each sequence is on separate line and ends with '-2'
    """
    TIME_MARK = "<{}> "
    SEPARATOR = " -1 "
    END_OF_LINE = "-2\n"

    format_description = "timed"

    def __init__(self, output_dir, file_suffix=''):
        super().__init__(output_dir, file_suffix)

        from bintrees import FastRBTree
        self.sequences = defaultdict(FastRBTree)

    def len_sequences(self) -> int:
        return len(self.sequences)

    def _read(self, sequence_key: typing.Hashable, time: datetime, items):
        time_index = Timed.calculate_time_index(time)
        self.sequences[sequence_key]\
            .set_default(time_index, set())\
            .update(items)

    def save(self):
        with open(self.output_file_path(), 'w') as file:
            for tree in self.sequences.values():
                init_time = tree.min_key()
                for time, items in tree.items():
                    file.write(self.TIME_MARK.format(time - init_time))
                    file.write(" ".join(map(lambda x: str(self.item_map[x]), items)))
                    file.write(self.SEPARATOR)
                file.write(self.END_OF_LINE)

        self.save_item_map()

    @staticmethod
    def calculate_time_index(time: datetime):
        """
        :type time: datetime
        :return: Number of 5 minute cluster where given datetime belongs
        """
        from dateutil.tz import tzutc
        initial_datetime = datetime(2016, 1, 1, 0, 0, tzinfo=tzutc())
        five_min_interval = 60 * 5
        delta = time - initial_datetime
        return delta.seconds // five_min_interval
