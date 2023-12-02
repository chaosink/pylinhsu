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


def mktime(t):
    return time.mktime(t)


def benchmark(func, repeat=1000, name=None):
    ts_begin = now()
    for i in range(repeat):
        func()
    ts_end = now()
    ts_delta = ts_end - ts_begin
    print_str = "Time"
    if name:
        print_str += " of " + name
    print(f"{print_str}: {ts_delta / repeat}")
