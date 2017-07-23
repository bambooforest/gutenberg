import argparse
import os
import subprocess

import sys
sys.path.append("src")
from utils import populate_raw_from_mirror

if __name__=='__main__':

    parser = argparse.ArgumentParser(
        "Update local PG repository.\n\n"\
        "This script will download all books currently not in your\n"\
        "local copy of PG and get the latest version of the metadata.\n"
        )
    # mirror dir
    parser.add_argument(
        "-m", "--mirror",
        help="Path to the mirror folder that will be updated via rsync.",
        default='data/mirror/',
        type=str)

    # raw dir
    parser.add_argument(
        "-r", "--raw",
        help="Path to the raw folder.",
        default='data/raw/',
        type=str)

    # metadata dir
    parser.add_argument(
        "-M", "--metadata",
        help="Path to the metadata folder.",
        default='metadata/',
        type=str)

    # update argument
    parser.add_argument("-k","--keep_rdf",
        help="If there is an RDF file in metadata dir, do not overwrite it.")

    # update argument
    parser.add_argument("-owr","--overwrite_raw",
        help="Overwrite files in raw.")

    # create the parser
    args = parser.parse_args()
    
    # check that all dirs exist
    if not os.path.isdir(args.mirror):
        raise ValueError("The specified mirror directory does not exist.")
    if not os.path.isdir(args.raw):
        raise ValueError("The specified raw directory does not exist.")
    if not os.path.isdir(args.metadata):
        raise ValueError("The specified metadata directory does not exist.")


    # update mirror
    # rsync -av --del --include '*/' --include '*99-0.txt' --exclude '*' aleph.gutenberg.org::gutenberg data/mirror/

    args = ["rsync", "-av", "--del","--include", "*/", "--include", "*-0.txt", "--exclude", "*", "aleph.gutenberg.org::gutenberg", args.mirror]    
    subprocess.call(args)

    # populate raw from mirror
    populate_raw_from_mirror(
        mirror_dir = args.mirror,
        raw_dir = args.raw,
        overwrite = args.overwrite_raw
        )

    # update metadata
    make_df_metadata(path_xml = os.path.join(args.metadata,'/rdf-files.tar.bz2'),
                     path_out = os.path.join(args.metadata,'/metadata.csv'),
                     update = args.keep_rdf)
