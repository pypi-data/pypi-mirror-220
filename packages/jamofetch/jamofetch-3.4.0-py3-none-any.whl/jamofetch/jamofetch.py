#!/usr/bin/env python3

import logging
import os
import pathlib
import re
import subprocess
import sys
import time
from argparse import ArgumentParser
from stat import ST_CTIME

JAMO_CMD_NERSC = 'module load jamo; jamo link library'
JAMO_CMD_DORI = 'apptainer --silent run docker://doejgi/jamo-dori jamo link -s dori library'

TWO_HOURS = 7200
ONE_MINUTE = 60


def _clean_library_name(library_name):
    clean_name = f"{library_name}".strip()
    if not re.match(r'^[A-Z]+$', clean_name):
        raise ValueError(f"invalid library name {library_name}")
    return clean_name


def _check_int_not_negative(value_to_check, value_name, allow_minus_1=False) -> int:
    """
    Throw an error if value_to_check is not a positive integer.  Provide
    value_name in error message.
    """
    if not value_to_check:
        return 0
    if not isinstance(value_to_check, int):
        raise ValueError(f"invalid value for {value_name}: expecting integer")
    if allow_minus_1 and value_to_check == -1:
        return -1
    if value_to_check <= 0:
        raise ValueError(f"invalid value for {value_name}: expecting positive integer")
    return value_to_check


def _wait_for_seq(seq_path, wait_interval_secs, wait_max_secs):
    """
    Check if seq_path is a link.  If seq_path is a broken link, wait until it is valid.
    Check link each wait_interval_secs seconds.  Exit when link is valid.  Throw
    an error if wait_max_secs is exceeded.  Set wait_max_secs to None to wait
    indefinitely.
    """
    if seq_path is None:
        raise ValueError("null seq_path")

    if not os.path.islink(seq_path):
        raise ValueError("seq_path is not a link")

    wait_interval = _check_int_not_negative(wait_interval_secs, 'wait_interval_secs')
    wait_max = _check_int_not_negative(wait_max_secs, 'wait_max_secs', allow_minus_1=True)

    total_wait = 0
    if wait_max and wait_interval:
        logging.debug(f"waiting for link {seq_path}; wait_interval: {wait_interval}; wait_max: {wait_max}")
        while (not os.path.exists(seq_path)) and (wait_max == -1 or total_wait < wait_max):
            time.sleep(wait_interval_secs)
            if wait_interval > 0:
                total_wait += wait_interval

    if not os.path.exists(seq_path):
        raise RuntimeError(f"sequence for link {seq_path} not provisioned within max wait seconds: {wait_max}")


def _find_fastq_path(lib_name, seq_dir):
    """
    Find symlink created for library in sequence directory
    by matching pattern similar to:
    HHCHO.52485.1.359430.GTGCTTA-GTAAGCA.fastq.gz
    """
    # sort contents in directory by modification time (we want the last modified)
    # adapted from:
    # https://www.tutorialspoint.com/How-do-you-get-a-directory-listing-sorted-by-creation-date-in-Python
    file_paths = [os.path.join(seq_dir, file_name) for file_name in os.listdir(os.path.realpath(seq_dir))]
    logging.debug(f"file paths: {file_paths}")
    # get file stats
    path_stats = [(path, os.lstat(path)) for path in file_paths]
    path_stats.sort(key=lambda x: x[1][ST_CTIME])
    for path_stat in path_stats:
        logging.debug(f"{path_stat[0]}:")
        for stat in sorted(filter(lambda a: a.startswith('st_'), dir(path_stat[1]))):
            logging.debug(f"    {stat}: {getattr(path_stat[1], stat)}")

    matched_link = None
    for path_stat in path_stats:
        filepath = path_stat[0]
        filetime = path_stat[1][ST_CTIME]
        filename = os.path.basename(filepath)
        if not os.path.islink(filepath):
            continue
        logging.debug(f"link candidate: {filename}; creation time: {filetime}")
        if str(filename).startswith(f"{lib_name}.") and str(filename).endswith('.fastq.gz'):
            matched_link = filepath
            logging.debug(f"link match: {filename}")

    if matched_link is not None:
        logging.debug(f"returning library seq file: {matched_link}")
        return matched_link

    raise RuntimeError(f"failed to find sequence file for library {lib_name}")


class LibSeq:

    def __init__(self, lib_name, seq_path):
        self._lib_name = _clean_library_name(lib_name)
        self._seq_path = seq_path

    def get_lib_name(self) -> str:
        return self._lib_name

    def get_seq_path(self):
        return self._seq_path

    def seq_exists(self) -> bool:
        return os.path.exists(self._seq_path)

    def get_real_path(self):
        if self._seq_path is None:
            return None
        return os.path.realpath(self._seq_path)

    def get_real_path_wait(self):
        if self.seq_exists():
            return self.get_real_path()
        else:
            raise RuntimeError(f"{self}: sequence file not available")

    def __str__(self):
        f"{self.__class__.__name__}(lib={self._lib_name};path={self._seq_path})"


class JamoLibSeq(LibSeq):

    def __init__(self, lib_name, seq_path, wait_interval_secs=10, wait_max_secs=-1):
        LibSeq.__init__(self, lib_name, seq_path)
        self._wait_interval_secs = _check_int_not_negative(wait_interval_secs, 'wait_interval_secs')
        self._wait_max_secs = _check_int_not_negative(wait_max_secs, 'wait_max_secs', allow_minus_1=True)
        self._sequence_ready = False

    def get_real_path_wait(self):
        if not self._sequence_ready:
            _wait_for_seq(self._seq_path, self._wait_interval_secs, self._wait_max_secs)
            self._sequence_ready = True
        return os.path.realpath(self._seq_path)


class JamoFetcher():
    def __init__(self, link_dir='.', wait_interval_secs=10, wait_max_secs=-1):
        self._wait_interval_secs = _check_int_not_negative(wait_interval_secs, 'wait_interval_secs')
        self._wait_max_secs = _check_int_not_negative(wait_max_secs, 'wait_max_secs', allow_minus_1=True)
        self._link_dir = os.path.realpath(link_dir)

    def get_cmd(self, clean_lib_name) -> str:
        if os.getenv('SLURM_PARTITION') == 'dori':
            return f"{JAMO_CMD_DORI} {clean_lib_name}"
        return f"{JAMO_CMD_NERSC} {clean_lib_name}"

    def fetch_lib_seq(self, lib_name, out_file=sys.stderr) -> JamoLibSeq:
        """
        Execute JAMO command to link sequence for library
        and return a LibSeq object containing the path to the sequence.
        """
        pathlib.Path(self._link_dir).mkdir(parents=True, exist_ok=True, mode=0o775)
        os.chdir(self._link_dir)
        clean_lib_name = _clean_library_name(lib_name)

        cmd = self.get_cmd(clean_lib_name)
        output = subprocess.check_output(cmd, shell=True)
        for line in output.splitlines():
            print(line.decode("utf-8"), file=out_file)

        seq_path = _find_fastq_path(clean_lib_name, self._link_dir)
        return JamoLibSeq(clean_lib_name, seq_path, self._wait_interval_secs, self._wait_max_secs)


def _fetch_seq(fetcher: JamoFetcher, libs):
    lib_seq_dict = {}
    for lib in libs:
        try:
            lib_seq: JamoLibSeq = fetcher.fetch_lib_seq(lib, out_file=sys.stderr)
            lib_seq_dict[lib_seq.get_lib_name()] = lib_seq
        except Exception as e:
            pass
    return lib_seq_dict


def main(args):
    logging.debug(f"args: {args}")

    if not args.library:
        return

    wait_interval_secs = _check_int_not_negative(args.interval, "interval")
    wait_max_secs = _check_int_not_negative(args.max, "max", allow_minus_1=True)

    link_dir = os.path.realpath(args.directory if args.directory else '.')
    fetcher: JamoFetcher = JamoFetcher(link_dir=link_dir, wait_interval_secs=wait_interval_secs,
                                       wait_max_secs=wait_max_secs)

    print("fetching sequence:")
    lib_seq_dict = _fetch_seq(fetcher, args.library)

    if not lib_seq_dict:
        return  # no sequence was fetched

    print("\nsequence links:")
    for lib_name, lib_seq in sorted(lib_seq_dict.items()):
        print(f"{lib_seq.get_lib_name()} symlink: {lib_seq.get_seq_path()}")
        print(f"{lib_seq.get_lib_name()} realpath: {lib_seq.get_real_path()}")

    if args.wait:
        total_wait = 0
        seq_ready = set()
        print("\nwaiting for JAMO to provision sequence . . . .")
        while (len(seq_ready) < len(lib_seq_dict)) and (wait_max_secs == -1 or total_wait <= wait_max_secs):
            for lib_name, lib_seq in sorted(lib_seq_dict.items()):
                if not lib_name in seq_ready and lib_seq.seq_exists():
                    print(f"{lib_name} sequence ready")
                    seq_ready.add(lib_name)
            if not wait_interval_secs or not wait_max_secs:
                break  # do not wait
            if len(seq_ready) < len(lib_seq_dict):
                time.sleep(wait_interval_secs)
                if wait_max_secs > 0:
                    total_wait += wait_interval_secs
        if len(seq_ready) < len(lib_seq_dict):
            print("\nexiting, not all sequence ready")
            if wait_max_secs != -1 and total_wait >= wait_max_secs:
                print(f"max wait {wait_max_secs} exceeded")


def cli():
    try:
        parser: ArgumentParser = ArgumentParser()
        parser.add_argument('-l', '--library', action='append',
                            help="library name(s) for which to retrieve sequence")
        parser.add_argument('-d', '--directory', required=False, default='.',
                            help="directory where to link sequence, defaults to current directory.  " +
                                 "Directory will be created if it doesn't exit.")
        parser.add_argument('-i', '--interval', required=False, type=int, default=10,
                            help="wait interval in seconds to check if sequence has been fetched, " +
                                 "ignored if wait flag not set")
        parser.add_argument('-m', '--max', required=False, type=int, default=TWO_HOURS,
                            help="maximum time to wait for sequence in seconds, " +
                                 "ignored if wait flag not set.  Specify -1 to wait indefinetely.")
        parser.add_argument('-w', '--wait', action='store_true',
                            help='wait for jamo to link sequence, output real path of linked sequence')
        parser.add_argument('--logging', required=False, default='WARN',
                            help="logging level (specify DEBUG for verbose logging)")

        ARGS = parser.parse_args()
        # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=log_level)
        logging.basicConfig(format='%(message)s', level=ARGS.logging.upper())
        main(ARGS)
    except KeyboardInterrupt:
        print('Interrupted', file=sys.stderr)
        # https://unix.stackexchange.com/questions/251996/why-does-bash-set-exit-status-to-non-zero-on-ctrl-c-or-ctrl-z
        sys.exit(130)


if __name__ == "__main__":
    cli()
