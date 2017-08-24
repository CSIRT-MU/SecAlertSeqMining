import dateutil.parser


class Csv:
    def __init__(self, alert):
        """
        The Csv class is supposed to facilitate reading and altering alert values represented as csv.

        :param alert: alert in CSV format with the following order of values:
            1. ID
            2. Detect time
            3. Category
            4. Node name (sensor name)
            5. Source IPv4
            6. Source protocol
            7. Target IPv4
            8. Target protocol
            9. List of target ports (separated by ';')
        """
        self._array = alert.split(",")
        self._array = list(map(lambda x: x.strip(), self._array))

        # Ports
        if self._array[8]:
            self._array[8] = set(map(int, self._array[8].split(';')))
        else:
            self._array[8] = set()

    def __str__(self):
        return ",".join(map(Csv._set_to_str, self.array))

    @staticmethod
    def _set_to_str(o):
        if isinstance(o, set):
            return ";".join(map(str, o))
        return str(o)

    @property
    def array(self):
        return self._array

    # ID

    @property
    def id(self):
        return self.array[0]

    # TIME PARAMS

    @property
    def _detect_time(self):
        """ String representation of 'DetectTime' """
        return self.array[1]

    @property
    def detect_time(self):
        """ Datetime object """
        return dateutil.parser.parse(self._detect_time)

    # CATEGORIES

    @property
    def category(self):
        return self.array[2]

    @property
    def category_with_target_ports(self):
        if len(self.target_ports) == 0:
            return [self.category]
        return [f"{self.category}.{port}" for port in self.target_ports]

    # NODES

    @property
    def node_name(self):
        return self.array[3]

    # SOURCES

    @property
    def source_ip4(self):
        return self.array[4]

    @property
    def source_proto(self):
        return self.array[5]

    # TARGETS

    @property
    def target_ip4(self):
        return self.array[6]

    @property
    def target_proto(self):
        return self.array[7]

    @property
    def target_ports(self):
        return self.array[8]

    def add_target_port(self, port):
        self._array[8].update(port)
