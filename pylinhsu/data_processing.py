import csv
import pandas as pd
import numpy as np


def read_csv(path):
    with open(path) as f:
        data = list(csv.reader(f))
    return data
