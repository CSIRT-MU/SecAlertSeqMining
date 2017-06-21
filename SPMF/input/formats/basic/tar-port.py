from collections import defaultdict

from SPMF.input.formats.abstract_format import Basic
from bintrees import FastRBTree
transactions = defaultdict(FastRBTree)


class Formatter(Basic):
    def sequences(self):
        return transactions.values()

    def tid_description(self):
        return "tar-port"

    def read(self, idea):
        if idea.target:
            transaction = transactions[idea.target]
            transaction.set_default(idea.time, set()).update(idea.category_with_ports)
