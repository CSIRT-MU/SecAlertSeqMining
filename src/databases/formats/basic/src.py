from .abstract import Basic


class Database(Basic):
    tid_description = "src"

    def read(self, alert):
        if alert.source_ip4:
            self._read(alert.source_ip4, alert.detect_time, [alert.category])
