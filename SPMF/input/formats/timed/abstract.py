from datetime import datetime, timezone

from SPMF.input.formats.abstract_format import Timed
from iso8601 import iso8601


class AbstractTimed(Timed):

    @staticmethod
    def calculate_time_index(timestamp):
        """
        :param timestamp: alert timestamp
        :return: Number of 5 minute cluster where timestamp belongs
        """
        INITIAL_DATETIME = iso8601.parse_date("2016-10-30 00:00:00Z")
        FIVE_MIN_INTERVAL = 60 * 5
        delta = datetime.fromtimestamp(timestamp, timezone.utc) - INITIAL_DATETIME
        return delta.seconds // FIVE_MIN_INTERVAL
