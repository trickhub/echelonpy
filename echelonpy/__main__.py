import argparse
import os
import logging
from lxml import etree

from echelonpy.reader import read
from echelonpy.tcx import from_laps


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", help="csv file output by the Echelon Console", type=str)
    parser.add_argument("-o", "--output", help="output file destination", type=str)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    return parser


def main():
    args = arg_parser().parse_args()

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)
    laps = read(args.csv_file)
    doc = from_laps(laps)

    tcx = etree.tostring(doc, xml_declaration=True, encoding="utf-8", pretty_print=True)

    output_filename = args.output if args.output is not None else os.path.splitext(args.csv_file)[0] + ".tcx"
    with open(output_filename, 'w') as output_file:
        output_file.write(tcx)
