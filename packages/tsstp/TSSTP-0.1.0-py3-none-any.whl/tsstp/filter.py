# -*- coding: utf-8 -*-
"""
Filter function for processing data extracted from template variables.
"""
from tsstp.internal_ds import SymbolNode

def sum(args):
    sum = 0
    for arg in args:
        sum += int(arg)
    return sum

def toInt(args: list[SymbolNode]):
    # Convert strings to integers
    for node in args:
        value = node.value
        if any(isinstance(i, list) for i in value):
            # nested list
            value[:] = [list(map(int, i)) for i in value]
        elif isinstance(value, list):
            value[:]= list(map(int, value))
        elif isinstance(value, str):
            value = int(value)

def toFloat(args: list[SymbolNode]):
    # Convert strings to float
    for node in args:
        value = node.value
        if any(isinstance(i, list) for i in value):
            # nested list
            value[:] = [list(map(float, i)) for i in value]
        elif isinstance(value, list):
            value[:]= list(map(float, value))
        elif isinstance(value, str):
            value = float(value)


