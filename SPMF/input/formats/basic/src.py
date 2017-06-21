from collections import defaultdict

from SPMF.input.formats.abstract_format import Basic
from bintrees import FastRBTree

transactions = defaultdict(FastRBTree)


class Formatter(Basic):
    def tid_description(self):
        return "src"

    def read(self, idea):
        if idea.source:
            transaction = transactions[idea.source]
            transaction.set_default(idea.time, set()).add(idea.category)

    def sequences(self):
        return transactions.values()
