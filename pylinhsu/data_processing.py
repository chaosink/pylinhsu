import csv
import argparse
import pandas as pd
from io import StringIO
from pylinhsu.time import benchmark
import pylinhsu.filesystem as fs
import json


def list_to_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def df_to_list(df, header=True):
    data = df.values.tolist()
    if header:
        data.insert(0, df.columns.values.tolist())
    return data


def df_to_csv(df, csv_path, header=True):
    df.to_csv(csv_path, header=header, index=False)


def df_to_xlsx(df, xlsx_path, header=True):
    df.to_excel(xlsx_path, header=header, index=False, engine="xlsxwriter")


def benchmark_feather_write(df, path):
    for compression in [["lz4", 16], ["zstd", 22]]:
        for compression_level in [None, compression[1]]:
            test_name = f"{compression[0]:4} {str(compression_level):4} write"
            path_compression = fs.replace_ext(
                path, f"{compression[0]}.{str(compression_level)}.feather"
            )
            benchmark(
                lambda: df.to_feather(
                    path_compression,
                    compression=compression[0],
                    compression_level=compression_level,
                ),
                10,
                test_name,
            )
            print(
                f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
            )


def df_to_feather(df, path):
    # zstd has larger compression ratio than lz4 with default compression_level.
    # Compression with the highest levels is too slow.
    df.to_feather(path, compression="zstd")
    return
    # Benchmark
    benchmark_feather_write(df, path)


def benchmark_parquet_write(df, path):
    for compression in ["snappy", "gzip", "brotli", "lz4", "zstd"]:
        test_name = f"{compression:6} write"
        path_compression = fs.replace_ext(path, f"{compression}.parquet")
        benchmark(
            lambda: df.to_parquet(
                path_compression,
                compression=compression,
            ),
            10,
            test_name,
        )
        print(
            f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
        )


def df_to_parquet(df, path):
    # brotli has the largest compression ratio.
    df.to_parquet(path, compression="brotli")
    return
    # Benchmark
    benchmark_parquet_write(df, path)


def json_to_dict(json_path):
    return json.load(open(json_path))


def dict_to_json(data, json_path, indent=4):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=indent)
        f.write("\n")


def file_has_tab(path):
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
    return "\t" if file_has_tab(path) else ","


def get_csv_str_sep(str):
    return "\t" if str_has_tab(str) else ","


def get_csv_dialect(path):
    return "excel-tab" if file_has_tab(path) else "excel"


def get_csv_str_dialect(str):
    return "excel-tab" if str_has_tab(str) else "excel"


def csv_to_list(path):
    dialect = get_csv_dialect(path)
    with open(path) as f:
        data = list(csv.reader(f, dialect))
    return data


def csv_str_to_list(str):
    dialect = get_csv_str_dialect(str)
    f = StringIO(str)
    data = list(csv.reader(f, dialect))
    return data


def csv_to_df(path, header="infer", names=None):
    sep = get_csv_sep(path)
    # With `header=0` and `names=[...]`, `names` is used as the header. So `names` has higher priority. However the first row of data is lost.
    df = pd.read_csv(path, sep=sep, header=header, names=names)
    return df


def csv_str_to_df(str, header="infer", names=None):
    sep = get_csv_str_sep(str)
    df = pd.read_csv(StringIO(str), sep=sep, header=header, names=names)
    return df


def csv_to_csv_gz(csv_path, csv_gz_path):
    df = csv_to_df(csv_path, header=None)
    df.to_csv(csv_gz_path, header=False, index=False, compression="gzip")


def csv_to_xlsx(csv_path, xlsx_path):
    df = csv_to_df(csv_path, header=None)
    # xlsxwriter is faster and more compressed than openpyxl.
    df.to_excel(xlsx_path, header=False, index=False, engine="xlsxwriter")
    # df.to_excel(xlsx_path, header=False, index=False, engine='openpyxl')


def csv_to_feather(csv_path, feather_path, names=None):
    df = csv_to_df(csv_path, names=names)
    df_to_feather(df, feather_path)
    return
    # Benchmark
    print(
        f"CSV    filesize: {fs.path_filesize_str(csv_path):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
    )
    benchmark_feather_write(df, feather_path)


def csv_to_parquet(csv_path, parquet_path, names=None):
    df = csv_to_df(csv_path, names=names)
    df_to_parquet(df, parquet_path)
    return
    # Benchmark
    print(
        f"CSV filesize: {fs.path_filesize_str(csv_path):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
    )
    benchmark_parquet_write(df, parquet_path)


def xlsx_to_df(path, header="infer", names=None):
    # `read_excel()` doesn't support inferring header as `read_csv()`, hence the implementation here.
    if header == "infer":
        if names is None:
            header = 0
        else:
            header = None
    # With `header=0` and `names=[...]`, `names` is used as the header. So `names` has higher priority. However the first row of data is lost.
    return pd.read_excel(path, header=header, names=names, engine="openpyxl")

    # Cannot execute in parallel.
    import xlwings as xw

    excel_app = xw.App(visible=False)
    excel_book = excel_app.books.open(path)
    excel_sheet = excel_book.sheets[0].used_range.value
    df = pd.DataFrame(excel_sheet)
    if header != 0 and names is not None:
        df.columns = names
    excel_book.close()
    excel_app.quit()
    return df


def xlsx_to_csv(xlsx_path, csv_path):
    df = xlsx_to_df(xlsx_path, header=None)
    df.to_csv(csv_path, header=False, index=False)


def xlsx_to_feather(xlsx_path, feather_path, names=None):
    df = xlsx_to_df(xlsx_path, names=names)
    df_to_feather(df, feather_path)


def xlsx_to_parquet(xlsx_path, parquet_path, names=None):
    df = xlsx_to_df(xlsx_path, names=names)
    df_to_parquet(df, parquet_path)


def feather_to_list(path, header=True, use_threads=True):
    df = feather_to_df(path, use_threads=use_threads)
    return df_to_list(df, header)


def benchmark_feather_read(path, use_threads):
    for compression in [["lz4", 16], ["zstd", 22]]:
        for compression_level in [None, compression[1]]:
            test_name = f"{compression[0]:4} {str(compression_level):4} read"
            path_compression = fs.replace_ext(
                path, f"{compression[0]}.{str(compression_level)}.feather"
            )
            benchmark(
                lambda: pd.read_feather(path_compression, use_threads=use_threads),
                10,
                test_name,
            )
            print(
                f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
            )


def feather_to_df(path, use_threads=True):
    return pd.read_feather(path, use_threads=use_threads)
    # Benchmark
    benchmark_feather_read(path, use_threads=False)
    benchmark_feather_read(path, use_threads=True)


def feather_to_csv(feather_path, csv_path, header=True, use_threads=True):
    df = feather_to_df(feather_path, use_threads)
    df_to_csv(df, csv_path, header)


def parquet_to_list(path, header=True):
    df = parquet_to_df(path)
    return df_to_list(df, header)


def benchmark_parquet_read(path):
    for compression in ["snappy", "gzip", "brotli", "lz4", "zstd"]:
        test_name = f"{compression:6} read"
        path_compression = fs.replace_ext(path, f"{compression}.parquet")
        benchmark(
            lambda: pd.read_parquet(path_compression),
            10,
            test_name,
        )
        print(
            f"{test_name}: {fs.path_filesize_str(path_compression):>{fs.FILESIZE_STR_BASE_1024_MAX_LEN}}"
        )


def parquet_to_df(path):
    return pd.read_parquet(path)
    # Benchmark
    benchmark_parquet_read(path)


def parquet_to_csv(parquet_path, csv_path, header=True):
    df = parquet_to_df(parquet_path)
    df_to_csv(df, csv_path, header)


def merge_csvs(csv_files, vertical=True, skip_first_row_column=False, interlaced=False):
    data = []
    for csv_file in csv_files:
        data.append(csv_to_list(csv_file))
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


# ----------------------------------------------------------------------------------------------------
# Main entry.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Handy utilities for data processing.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(required=True, dest="subparser_name")

    # recommit
    parser_recommit = subparsers.add_parser(
        "parquet_to_csv",
        aliases=["p2c"],
        description=parquet_to_csv.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_recommit.add_argument(
        "parquet_path",
        metavar="parquet_path",
        type=str,
        help="parquet path",
    )
    parser_recommit.add_argument(
        "csv_path",
        metavar="csv_path",
        type=str,
        help="csv path",
    )
    parser_recommit.add_argument(
        "--header",
        "-H",
        action="store_true",
        help="export header to csv",
    )
    parser_recommit.set_defaults(
        func=lambda args: parquet_to_csv(args.parquet_path, args.csv_path, args.header)
    )

    args = parser.parse_args()
    args.func(args)
