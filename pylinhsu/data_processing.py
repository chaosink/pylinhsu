import csv
import pandas as pd
import numpy as np


def has_tab(path):
    with open(path) as f:
        for l in f:
            if l.find("\t") != -1:
                return True
    return False


def get_csv_sep(path):
    return "\t" if has_tab(path) else ","


def get_csv_dialect(path):
    return "excel-tab" if has_tab(path) else "excel"


def read_csv(path):
    dialect = get_csv_dialect(path)
    with open(path) as f:
        data = list(csv.reader(f, dialect))
    return data


def read_csv_as_dataframe(path, header="infer"):
    sep = get_csv_sep(path)
    df = pd.read_csv(path, sep=sep, header=header)
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


def csv_to_xlsx(csv_path, xlsx_path):
    df = read_csv_as_dataframe(csv_path, header=None)
    # xlsxwriter is faster and more compressed than openpyxl.
    df.to_excel(xlsx_path, header=False, index=False, engine="xlsxwriter")
    # df.to_excel(xlsx_path, header=False, index=False, engine='openpyxl')


def csv_to_csv_gz(csv_path, csv_gz_path):
    df = read_csv_as_dataframe(csv_path, header=None)
    df.to_csv(csv_gz_path, header=False, index=False, compression="gzip")


def csv_to_feather(csv_path, feather_path):
    df = read_csv_as_dataframe(csv_path, header=None)
    df.to_feather(feather_path)


def csv_to_parquet(csv_path, parquet_path):
    df = read_csv_as_dataframe(csv_path, header=None)
    df.to_parquet(parquet_path)
