import time
from datetime import datetime


def timestamp_to_time(timestamp_input):
    try:
        if timestamp_input.isdigit():
            timestamp_input = int(timestamp_input)
    except:
        pass

    if len(str(timestamp_input)) > 11:
        timestamp_input = timestamp_input / 1000
    time_array = time.localtime(timestamp_input)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def iso8601(timestamp=None):
    try:
        if timestamp.isdigit():
            timestamp = int(timestamp)
    except:
        pass
    if isinstance(timestamp, str):
        if len(timestamp) == 15:
            timestamp = int(timestamp.split('.')[0])
        else:
            return timestamp
    if timestamp is None or not isinstance(timestamp, int) or int(timestamp) < 0:
        return None
    try:
        utc = datetime.utcfromtimestamp(timestamp // 1000)
        return utc.strftime('%Y-%m-%d %H:%M:%S%f')[:-6]
    except (TypeError, OverflowError, OSError):
        return None


def get_utc_datetime():
    return datetime.utcnow()


def get_str_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_datetime():
    return datetime.now()


def get_daml_utc_now_for_request():
    return get_datetime().isoformat() + 'Z'


def get_str_datetime_from_iso_str(iso_str):
    return datetime.strptime(iso_str, '%Y-%m-%dT%H:%M:%S.%fZ')


if __name__ == '__main__':
    print(timestamp_to_time("1650502822"))

