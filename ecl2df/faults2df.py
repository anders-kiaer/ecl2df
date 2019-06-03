#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extract the contents of the FAULTS keyword into
a DataFrame

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import argparse
import numpy as np
import pandas as pd

from .eclfiles import EclFiles

RECORD_COLUMNS = ['NAME', 'IX1', 'IX2', 'IY1', 'IY2', 'IZ1', 'IZ2', 'FACE']
COLUMNS = ['NAME', 'I', 'J', 'K', 'FACE']
ALLOWED_FACES = ['X', 'Y', 'Z', 'I', 'J', 'K', 'X-', 'Y-', 'Z-', 'I-', 'J-', 'K-']


def deck2faultsdf(deck):
    # In[91]: list(deck['FAULTS'][0])
    # Out[91]: [[u'F1'], [36], [36], [41], [42], [1], [14], [u'I']]
    data = []
    # It is allowed in Eclipse to use the keyword FAULTS
    # as many times as needed. Thus we need to loop in some way:
    for keyword in deck:
        if keyword.name == "FAULTS":
            for rec in keyword:
                # Each record now has a range potentially in three
                # dimensions for the fault, unroll this:
                faultname = rec[0][0]
                faultface = rec[7][0]
                for i_idx in range(rec[1][0], rec[2][0] + 1):
                    for j_idx in range(rec[3][0], rec[4][0] + 1):
                        for k_idx in range(rec[5][0], rec[6][0] + 1):
                            data.append([faultname, i_idx, j_idx, k_idx, faultface])
    return pd.DataFrame(columns=COLUMNS, data=data)

def parse_args():
    """Parse sys.argv using argparse"""
    parser = argparse.ArgumentParser()
    parser.add_argument("DATAFILE", help="Name of Eclipse DATA file.")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Name of output csv file.",
        default="faults.csv",
    )
    return parser.parse_args()


def main():
    """Entry-point for module, for command line utility"""
    args = parse_args()
    eclfiles = EclFiles(args.DATAFILE)
    if eclfiles:
        deck = eclfiles.get_ecldeck()
    faults_df = deck2faultsdf(deck)
    faults_df.to_csv(args.output, index=False)
    print("Wrote to " + args.output)
