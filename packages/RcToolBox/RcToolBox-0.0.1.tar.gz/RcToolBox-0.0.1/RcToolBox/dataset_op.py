# /usr/bin/env python
import os
import glob
import SimpleITK as sitk
import numpy as np
from nifti_op import load_nifti


join = os.path.join


# calculate file size, return in MB
def get_file_size(file_path):
    """
    Args:
        file_path: file path
    Returns:
        file size
    """
    return os.path.getsize(file_path) / 1024 / 1024


if __name__ == '__main__':
    pass
