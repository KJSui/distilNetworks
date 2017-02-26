#!/usr/bin/python
"""
run_distilNetworks.py: Top-level Run.
"""
from distilNetworks import *

if __name__ == '__main__':
    obj = logEnrichment()
    file = input()
    obj.addIPClass(file)
    obj.IPRateLimiting(file)
    obj.logAggregation(file)
