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
from demand_acep import hello_world

def test_hello_world():
    """
    This function test the function hello_world()
    """
    result = hello_world()

    assert result == "Hello world!", "The function does not return the string 'Hello world!'"
    
    return
