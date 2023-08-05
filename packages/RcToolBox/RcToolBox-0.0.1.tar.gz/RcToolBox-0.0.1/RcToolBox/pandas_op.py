#!/usr/bin/env python
import pandas as pd
import os

def pd_create_tabel(args):
    """
    Args:
        args: column name

    Returns:

    """
    data = {}
    if isinstance(args, list):
        for _ in args:
            data[str(_)] = []

    return data


def pd_write_table(data, dst_file, sheet_name='Sheet1'):
    if not isinstance(data, dict):
        raise TypeError("Input is expected to be dict, not {}".format(type(data)))
    df = pd.DataFrame()
    for k in data.keys():
        df = pd.concat([df, pd.DataFrame({k: data[k]})], axis=1)
    
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
    df.to_excel(dst_file, index=False, sheet_name=sheet_name)


def create_excel(res, args, dst_file):
    """
    Args:
        res (list): variable
        args (list): column name
        dst_file (str): xlsx file path 

    Returns:
    
    """
    
    if isinstance(res, list) and isinstance(args, list):
        assert len(res[0]) == len(args)
        data = pd_create_tabel(args)
        for i in range(len(res)):
            for j in range(len(args)):
                data[args[j]].append(res[i][j])

        pd_write_table(data, dst_file)
    else:
        raise TypeError


if __name__ == '__main__':
    x = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    y = ['a', 'b', 'c']
    create_excel(x, y, 'test.xlsx')
