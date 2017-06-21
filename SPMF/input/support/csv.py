""" The Csv class is supposed to facilitate reading and altering alert values represented as csv.
"""
from datetime import timezone, datetime


class Csv:
    def __init__(self, idea):
        """
        :param idea: One IDEA alert as string
        """
        self._array = idea.split(",")
        self._array[-1] = self._array[-1].strip()

        # Ports
        if self._array[8]:
            self._array[8] = set(map(int, self._array[8].split(';')))
        else:
            self._array[8] = set()

        # Conn count
        if self._array[9]:
            self._array[9] = int(self._array[9])

    @property
    def array(self):
        return self._array

    @property
    def id(self):
        return self.array[0]

    @property
    def aggr_id(self):
        return self.array[1]

    @property
    def time(self):
        return float(self.array[2])
        # Old csv with date in iso/rfc format
        # return iso8601.parse_date(self.array[2])

    @property
    def date_time(self):
        return datetime.fromtimestamp(self.time, timezone.utc)

    @property
    def category(self):
        return self.array[3]

    @property
    def category_with_ports(self):
        if len(self.port) == 0:
            return [self.category]
        return ["{}.{}".format(self.category, port) for port in self.port]

    @property
    def source(self):
        return self.array[4]

    @property
    def source_proto(self):
        return self.array[5]

    @property
    def target(self):
        return self.array[6]

    @property
    def target_proto(self):
        return self.array[7]

    @property
    def port(self):
        return self.array[8]

    def add_port(self, port):
        self._array[8].update(port)

    @property
    def conn_count(self):
        return self.array[9]

    @property
    def sensor(self):
        return self.array[10]

    def __str__(self):
        return ",".join(map(Csv._set_to_str, self.array))

    @staticmethod
    def _set_to_str(o):
        if isinstance(o, set):
            return ";".join(map(str, o))
        return str(o)
