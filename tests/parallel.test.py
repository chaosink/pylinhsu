import pylinhsu.parallel as pl


def test_parallel_for():
    def func(args):
        i, k = args
        print(i, k)

    data = [i**2 for i in range(100)]
    pl.parallel_for(func, enumerate(data))


if __name__ == "__main__":
    test_parallel_for()
