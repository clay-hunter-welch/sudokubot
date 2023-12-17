#!/usr/bin/python
'''
-/ change point class to namedtuple
-/ formatted prints instead of from future stuff
-	dynamic board update to watch solve
-/all loops upgraded to enumerate which warrant upgrade
-sorting routines used
-fullest nines support
-PEP 8 conventions sweep
-x	tabs out
-/	spacing around =
-/	spacing between classes and class functions

rewrite alone is ~20 ms faster
'''

from __future__ import print_function
import argparse as ap
from copy import deepcopy as dc
import csv
import time
import collections
import re
import sys
import curses


def pbar(window):
    for i in range(10):
        window.addstr(1, 10, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.addstr(2, 10, "[" + ("=" * i) + ">" + (" " * (10 - i )) + "]")
        window.refresh()
        time.sleep(0.5)


def main():
	curses.wrapper(pbar)


main()