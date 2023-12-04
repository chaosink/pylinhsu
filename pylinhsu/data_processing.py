import os
import csv
import pandas as pd
import numpy as np
from io import StringIO
from pylinhsu.time import benchmark
import pylinhsu.filesystem as fs


def has_tab(path):
    with open(path) as f:
        for l in f:
            if l.find("\t") != -1:
                return True
    return False


def str_has_tab(str):
    lines = str.split("\n")
    for l in lines:
        if l.find("\t") != -1:
            return True
    return False


def get_csv_sep(path):
    return "\t" if has_tab(path) else ","


def get_csv_str_sep(str):
    return "\t" if str_has_tab(str) else ","


def get_csv_dialect(path):
    return "excel-tab" if has_tab(path) else "excel"


def get_csv_str_dialect(str):
    return "excel-tab" if str_has_tab(str) else "excel"


def read_csv(path):
    dialect = get_csv_dialect(path)
    with open(path) as f:
        data = list(csv.reader(f, dialect))
    return data


def read_csv_as_df(path, header="infer"):
    sep = get_csv_sep(path)
    df = pd.read_csv(path, sep=sep, header=header)
    return df


def read_csv_str(str):
    dialect = get_csv_str_dialect(str)
    f = StringIO(str)
    data = list(csv.reader(f, dialect))
    return data


def read_csv_str_as_df(str, header="infer"):
    sep = get_csv_str_sep(str)
    df = pd.read_csv(StringIO(str), sep=sep, header=header)
    return df


def write_csv(path, data):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def merge_csvs(csv_files, vertical=True, skip_first_row_column=False, interlaced=False):
    data = []
    for csv_file in csv_files:
        data.append(read_csv(csv_file))
    if skip_first_row_column:
        if vertical:
            data = [d[1:] for d in data]
        else:
            data = [[r[1:] for r in d] for d in data]

    n_row = len(data[0])  # Assue all CSVs have the same row count.
    n_col = len(data[0][0])  # Assue all CSVs have the same column count.

    if vertical:
        if interlaced:
            merge = []
            for i in range(n_row):
                for d in data:
                    merge.append(d[i])
            return merge
        else:
            return data

    merge = [[] for i in range(n_row)]
    if interlaced:
        for i in range(n_row):
            for j in range(n_col):
                for d in data:
                    merge[i].append(d[i][j])
    else:
        for d in data:
            for i in range(n_row):
                merge[i] += d[i]

    return merge


def read_xlsx(path, header=0, usecols=None):
    return pd.read_excel(path, header=header, usecols=usecols, engine="openpyxl")

    # Cannot execute in parallel.
    import xlwings as xw

    excel_app = xw.App(visible=False)
    excel_book = excel_app.books.open(xlsx_path)
    excel_sheet = excel_book.sheets[0].used_range.value
    data = pd.DataFrame(excel_sheet)
    excel_book.close()
    excel_app.quit()
    return data


def csv_to_xlsx(csv_path, xlsx_path):
    df = read_csv_as_df(csv_path, header=None)
    # xlsxwriter is faster and more compressed than openpyxl.
    df.to_excel(xlsx_path, header=False, index=False, engine="xlsxwriter")
    # df.to_excel(xlsx_path, header=False, index=False, engine='openpyxl')


def csv_to_csv_gz(csv_path, csv_gz_path):
    df = read_csv_as_df(csv_path, header=None)
    df.to_csv(csv_gz_path, header=False, index=False, compression="gzip")


def read_feather(path, use_threads=True):
    df = pd.read_feather(path, use_threads=use_threads)
    return df.values.tolist()

    # Benchmark
    for compression in [["lz4", 16], ["zstd", 22]]:
        for compression_level in [None, compression[1]]:
            test_name = f"{compression[0]:4} {str(compression_level):4} read"
            path_compression = path.replace(
                "feather", f"{compression[0]}.{str(compression_level)}.feather"
            )
            benchmark(
                lambda: pd.read_feather(path_compression, use_threads=False),
                10,
                test_name,
            )
            print(
                f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
            )


def read_parquet(path):
    df = pd.read_parquet(path)
    return df.values.tolist()

    # Benchmark
    for compression in ["snappy", "gzip", "brotli", "lz4", "zstd"]:
        test_name = f"{compression:6} read"
        path_compression = path.replace("parquet", f"{compression}.parquet")
        benchmark(
            lambda: pd.read_parquet(path_compression),
            10,
            test_name,
        )
        print(
            f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
        )


def csv_to_feather(csv_path, feather_path, names=None):
    df = read_csv_as_df(csv_path, header=None)
    if names:
        df.columns = names
    # zstd has larger compression ratio than lz4 with default compression_level.
    # Compression with the highest levels is too slow.
    df.to_feather(feather_path, compression="zstd")
    return

    # Benchmark
    print(
        f"CSV    filesize: {fs.path_filesize_str(csv_path):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
    )
    for compression in [["lz4", 16], ["zstd", 22]]:
        for compression_level in [None, compression[1]]:
            test_name = f"{compression[0]:4} {str(compression_level):4} write"
            feather_path_compression = feather_path.replace(
                "feather", f"{compression[0]}.{str(compression_level)}.feather"
            )
            benchmark(
                lambda: df.to_feather(
                    feather_path_compression,
                    compression=compression[0],
                    compression_level=compression_level,
                ),
                10,
                test_name,
            )
            print(
                f"{test_name}: {fs.path_filesize_str(feather_path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
            )


def csv_to_parquet(csv_path, parquet_path, names=None):
    df = read_csv_as_df(csv_path, header=None)
    if names:
        df.columns = names
    # brotli has the largest compression ratio.
    df.to_parquet(parquet_path, compression="brotli")
    return

    # Benchmark
    print(
        f"CSV filesize: {fs.path_filesize_str(csv_path):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
    )
    for compression in ["snappy", "gzip", "brotli", "lz4", "zstd"]:
        test_name = f"{compression:6} write"
        parquet_path_compression = parquet_path.replace(
            "parquet", f"{compression}.parquet"
        )
        benchmark(
            lambda: df.to_parquet(
                parquet_path_compression,
                compression=compression,
            ),
            10,
            test_name,
        )
        print(
            f"{test_name}: {fs.path_filesize_str(parquet_path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
        )


def df_to_xlsx(df, xlsx_path, header=True):
    df.to_excel(xlsx_path, header=header, index=False, engine="xlsxwriter")


def xlsx_to_parquet(xlsx_path, parquet_path, names=None):
    df = read_xlsx(xlsx_path, header=None)
    if names:
        df.columns = names
    # brotli has the largest compression ratio.
    df.to_parquet(parquet_path, compression="brotli")
    return
