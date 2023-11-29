import time
from datetime import datetime


EPOCH = datetime(1970, 1, 1)


def now():
    return datetime.now()


def sleep(s):
    time.sleep(s)


def delta_hms(ts0, ts1):
    d = ts1 - ts0
    epoch_ts = EPOCH + d
    return epoch_ts.strftime("%H:%M:%S")
