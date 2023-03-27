import argparse
import logging
import subprocess
import sys
from typing import List

logging.root.name = "tee-cli"


def run(cmd: List[str], logfile: str):
    # first, open logfile for writing
    with open(logfile, "w") as w:
        # then start a process
        p = subprocess.Popen(
            cmd,
            # use bufsize and universal_newlines to read in utf-8
            bufsize=1,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )

        # read stdout for lines
        for line in p.stdout:
            sys.stdout.write(line)
            w.write(line)

            sys.stdout.flush()
            w.flush()

        # wait for process result, then exit
        sys.exit(p.wait())


def main(argv: List[str] = sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        dest="output",
        default=None,
        required=False,
        help="Path to output log file with stdout+stderr content",
    )
    parser.add_argument("command", help="Command to run")

    args, extras = parser.parse_known_args(args=argv)

    try:
        run([args.command] + extras, args.output)
    except Exception as e:
        logging.error(e)
        sys.exit(1)
