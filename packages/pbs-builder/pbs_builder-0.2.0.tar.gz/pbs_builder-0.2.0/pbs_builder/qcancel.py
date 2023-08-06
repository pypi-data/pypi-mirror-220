#!/usr/bin/env python3
import os
import sys
from subprocess import getstatusoutput

def run():
    if len(sys.argv) == 1 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
        sys.stderr.write("Usage: qcancel work_dir/jobs\n\ncancel all unfinished jobs in a pipeline\n")
        sys.exit(0)

    in_file = sys.argv[1]
    with open(in_file, 'r') as f:
        for line in f:
            content = line.rstrip().split('\t')
            sample = content[0]
            qid = content[1]
            status, ret = getstatusoutput(f"qdel {qid}")
            if status != 0:
                sys.stderr.write(f"Failed to delete job {sample}, {ret}:\n")
    sys.stderr.write("All jobs canceled!\n")
