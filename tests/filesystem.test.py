import pylinhsu.filesystem as fs


def test_filesize_str():
    assert fs.filesize_str(0) == "0   B"
    assert fs.filesize_str(0, False) == "0  B"

    assert fs.filesize_str(1000 - 1) == "999   B"
    assert fs.filesize_str(1000 - 1, False) == "999  B"

    assert fs.filesize_str(1000) == "1000   B"
    assert fs.filesize_str(1000, False) == "1.00 KB"

    assert fs.filesize_str(1024) == "1.00 KiB"
    assert fs.filesize_str(1024, False) == "1.02 KB"

    assert fs.filesize_str(1000**2 - 1) == "976.56 KiB"
    assert fs.filesize_str(1000**2 - 1, False) == "1000.00 KB"

    assert fs.filesize_str(1024**2 - 1) == "1024.00 KiB"
    assert fs.filesize_str(1024**2 - 1, False) == "1.05 MB"

    assert fs.filesize_str(1000**2) == "976.56 KiB"
    assert fs.filesize_str(1000**2, False) == "1.00 MB"

    assert fs.filesize_str(1024**2) == "1.00 MiB"
    assert fs.filesize_str(1024**2, False) == "1.05 MB"


if __name__ == "__main__":
    test_filesize_str()
