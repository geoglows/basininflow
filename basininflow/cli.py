import argparse
import datetime
import logging
import os
import sys

from .inflow import create_inflow_file


def main():
    parser = argparse.ArgumentParser(description='Create inflow file for LSM files and input directory.')

    parser.add_argument('--lsmdata', type=str,
                        help='Path to directory of LSM NC files, a single NC file, or a glob pattern for NC files')
    parser.add_argument('--inputdir', type=str,
                        help='Input directory path for a specific VPU which contains weight tables')
    parser.add_argument('--inflowdir', type=str,
                        help='Inflow directory path for a specific VPU where m3 runoff inflows NC files are saved')
    parser.add_argument('--timestep', type=int, default=3,
                        help='Desired time step in hours. Default is 3 hours')
    parser.add_argument('--cumulative', action='store_true', default=False,
                        help='A boolean flag to mark if the runoff is cumulative. Inflows should be incremental')

    args = parser.parse_args()

    gen(parser, args)
    return


def gen(parser, args):
    logging.basicConfig(level=logging.INFO,
                        stream=sys.stdout,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # Access the parsed argument
    lsm_data = args.lsmdata
    input_dir = args.inputdir
    inflow_dir = args.inflowdir
    timestep = datetime.timedelta(hours=args.timestep)
    cumulative = args.cumulative

    if not all([lsm_data, input_dir, inflow_dir]):
        # print usage
        parser.print_usage()
        return

    # check what kind of lsm data was given
    if os.path.isdir(lsm_data):
        lsm_data = os.path.join(lsm_data, '*.nc*')
    elif os.path.isfile(lsm_data):
        ...  # this is correct, a single file is allowed
    elif '*' in lsm_data:
        ...  # this is correct, xarray will interpret the glob sting independently
    elif not os.path.exists(lsm_data) and '*' not in lsm_data:
        raise FileNotFoundError(f'{lsm_data} does not exist and is not a glob pattern')

    # Create the inflow file for each LSM file
    create_inflow_file(lsm_data, input_dir, inflow_dir, timestep=timestep, cumulative=cumulative)
    return