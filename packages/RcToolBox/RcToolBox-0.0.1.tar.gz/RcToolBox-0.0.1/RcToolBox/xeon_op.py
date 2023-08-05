#!/usr/bin/env python
from multiprocessing import Pool


# map and apply_sync both are worth exploring
def hardcore_process(function, args, num_workers=4):
    res = None
    if isinstance(args, list):
        if len(args) != 1:
            print("We will use {} cpu!".format(num_workers))
            p = Pool(num_workers)
            res = p.map(function, args)
            p.close()
            p.join()
    else:
        try:
            res = function(args)
        except Exception as err:
            print(err)
    
    if res is None:
        print("Multiprocessing Result is None, it may be caused by the input or the function")
    return res


if __name__ == '__main__':
    pass
