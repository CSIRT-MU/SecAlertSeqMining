from collections import defaultdict
from bintrees import FastRBTree
from SPMF.input.formats.timed.abstract import AbstractTimed

transactions = defaultdict(FastRBTree)


class Formatter(AbstractTimed):
    def sequences(self):
        return transactions.values()

    def tid_description(self):
        return "tar"

    def read(self, idea):
        if idea.target:
            transaction = transactions[idea.target]
            time_index = AbstractTimed.calculate_time_index(idea.time)
            transaction.set_default(time_index, set()).add(idea.category)
