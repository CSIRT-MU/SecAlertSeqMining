from collections import defaultdict

from bintrees import FastRBTree

from SPMF.input.formats.timed.abstract import AbstractTimed

transactions = defaultdict(FastRBTree)


class Formatter(AbstractTimed):
    def tid_description(self):
        return "src-port"

    def read(self, idea):
        if idea.source:
            transaction = transactions[idea.source]
            time_index = AbstractTimed.calculate_time_index(idea.time)
            transaction.set_default(time_index, set()).update(idea.category_with_ports)

    def sequences(self):
        return transactions.values()
