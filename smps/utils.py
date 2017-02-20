"""
"""
from .io import *

def _get_bin_count(fpath, encoding='ISO-8859-1'):
    """Get the number of bins in the file."""
    bins = 0
    with open(fpath, 'r', encoding=encoding) as f:
        for line in f:
            try:
                if float(line.split(',')[0]):
                    bins += 1
            except: pass

    return bins

def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

def load_dataset(name):
    """Load a dataset from the online repository (internet required)."""

    path = "https://github.com/dhhagan/py-smps/raw/master/{}.txt".format(name)

    return load_smps_file(path)
