from datetime import datetime, timezone


def parse_datetime(dt_str):
    return datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)


def parse_datetime_short(dt_str):
    try:
        return datetime.strptime(dt_str, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
    except ValueError:
        return None #TODO test
