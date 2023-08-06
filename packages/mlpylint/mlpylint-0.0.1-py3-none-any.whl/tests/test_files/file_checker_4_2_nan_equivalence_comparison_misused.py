import numpy as np
import numpy as dummyNp
import numpy
from numpy import nan as fnin


# Test case 1: Incorrect NaN comparison
def incorrect_nan_comparison_1():
    if None is numpy.nan:
        return "This is incorrect"

    if None == np.NaN:
        return "This is incorrect"

    if None != dummyNp.NAN:
        return "This is incorrect"

    if None < fnin:
        return "This is incorrect"


# Test case 2: Correct NaN comparison using 'np.isnan()'
def correct_nan_comparison_1():
    x = np.nan
    if np.isnan(x):
        return "This is correct"
