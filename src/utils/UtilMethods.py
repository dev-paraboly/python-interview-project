from datetime import datetime, tzinfo


class Utils:
    @staticmethod
    def timestamp_to_str(ts_as_int):
        as_str = datetime.utcfromtimestamp(
            ts_as_int).strftime('%Y-%m-%d %H:%M:%S')
        return as_str
