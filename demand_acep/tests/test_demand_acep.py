"""
This is the place for all the unit tests for the package demand_acep.
We can refactor this if this becomes too large.

"""

import pandas as pd
import os, sys
import re
from os import listdir
from os.path import isfile, join
import pytest # automatic test finder and test runner

# To import files from the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import demand_acep as da
from create_db_schema import read_source_file 

################################################################################
######## Tests for function read_source_file ###################################
################################################################################
def test_read_source_file():
    
    
    return 