from collections import defaultdict

from SPMF.input.formats.abstract_format import Basic
from bintrees import FastRBTree

from SPMF.input.formats.timed.abstract import AbstractTimed

transactions = defaultdict(FastRBTree)


class Formatter(AbstractTimed):
    def tid_description(self):
        return "src"

    def read(self, idea):
        if idea.source:
            transaction = transactions[idea.source]
            time_index = AbstractTimed.calculate_time_index(idea.time)
            transaction.set_default(time_index, set()).add(idea.category)

    def sequences(self):
        return transactions.values()
