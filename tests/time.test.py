from pylinhsu import time
from datetime import datetime


def test_now():
    ts = time.now()
    print(ts)


def test_delta_hms():
    ts0 = time.now()
    print(ts0)

    time.sleep(2)

    ts1 = time.now()
    print(ts1)

    print(time.delta_hms(ts0, ts1))


if __name__ == "__main__":
    test_now()
    test_delta_hms()
