from .abstract import Timed


class Database(Timed):
    tid_description = 'src-tar-port'

    def read(self, alert):
        if alert.source_ip4 and alert.target_ip4:
            self._read((alert.source_ip4, alert.target_ip4), alert.detect_time, alert.category_with_target_ports)
