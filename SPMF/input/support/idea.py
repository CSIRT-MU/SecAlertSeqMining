""" The Idea class is supposed to facilitate read values from IDEA format.
Class provides simple access to often used values inside IDEA through parameters. None is returned when value is missing.
Complete IDEA alert is accessible as 'json' property.
"""

import ujson as json  # Fast JSON parser
from functools import wraps

import dateutil.parser


def not_found(method):
    """ This decorator make sure that None will be return when method throws KeyError, IndexError or TypeError. """
    @wraps(method)
    def decorator(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except (KeyError, IndexError, TypeError):
            return None

    return decorator


def cached_property(method):
    """
    Simple decorator caches return value of a method.
    This decorator saves return value of method into private attribute (named by the method name with '_' prefix)
    in case that this private attribute hasn't been set yet.
    Once a object has the private attribute the decorator returns the attribute instead of calling the method.
    """
    @property
    @wraps(method)
    def decorator(self, *args, **kwargs):
        attr_name = '_' + method.__name__

        if not hasattr(self, attr_name):
            setattr(self, attr_name, method(self, *args, **kwargs))

        return getattr(self, attr_name)

    return decorator


def idea_property(method):
    """ idea_property decorator just combine @cached_property and @not_found decorators. """
    return cached_property(not_found(method))


class Idea:
    def __init__(self, idea):
        """
        :param idea: One IDEA alert as string
        """
        self._json = json.loads(idea)

    @property
    def json(self):
        return self._json

    @idea_property
    def id(self):
        return self.json["ID"]

    @idea_property
    def aggr_id(self):
        return self.json["AggrID"]

    @idea_property
    def conn_count(self):
        return self.json["ConnCount"]

    @idea_property
    def flow_count(self):
        return self.json["FlowCount"]

    @idea_property
    def sensor(self):
        # Remove warden filler Nodes from list of sensors
        nodes = filter(lambda node: "warden_filer" not in node['Name'], self.json['Node'])
        # Cannot use next(), because Python 2 return list instead of generator
        # return next(nodes, None)['Name']
        return nodes[0]['Name']

    @idea_property
    def category(self):
        return self.json['Category'][0]

    @idea_property
    def sources(self):
        return self.json["Source"]

    @idea_property
    def source_ip(self):
        return self.sources[0]["IP4"]

    @idea_property
    def source(self):
        return self.source_ip[0]

    @idea_property
    def targets(self):
        return self.json["Target"]

    @idea_property
    def target_ip(self):
        return self.targets[0]["IP4"]

    @idea_property
    def target(self):
        return self.target_ip[0]

    @idea_property
    def target_ports(self):
        return self.targets[0]["Port"]

    @idea_property
    def port(self):
        return self.target_ports[0]

    @idea_property
    def time(self):
        return self.json["DetectTime"]

    @idea_property
    def datetime(self):
        return dateutil.parser.parse(self.time)

    @idea_property
    def src_proto(self):
        return self.sources[0]["Proto"][0]

    @idea_property
    def tar_proto(self):
        return self.targets[0]["Proto"][0]

    @idea_property
    def _iabu(self):
        return self.json['_iABU'][0]

    @idea_property
    def iabu_duplicate(self):
        return self._iabu['Duplicate']

    @idea_property
    def iabu_continuing(self):
        return self._iabu['Continuing']

    @idea_property
    def iabu_overlapping(self):
        return self._iabu['Overlapping']

    @idea_property
    def iabu_non_overlapping(self):
        return self._iabu['NonOverlapping']
