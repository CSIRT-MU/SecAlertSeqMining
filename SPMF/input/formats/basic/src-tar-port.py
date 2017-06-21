from collections import defaultdict
from bintrees import FastRBTree

from SPMF.input.formats.abstract_format import Basic

transactions = defaultdict(FastRBTree)


class Formatter(Basic):

    def sequences(self):
        return transactions.values()

    def tid_description(self):
        return "src-tar-port"

    def read(self, idea):
        if idea.source and idea.target:
            transaction = transactions[idea.source, idea.target]
            transaction.set_default(idea.time, set()).update(idea.category_with_ports)
