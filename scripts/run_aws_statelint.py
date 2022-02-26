#! /usr/bin/env python
import json
import os
import subprocess
import sys
from ast import literal_eval
from subprocess import Popen
from tempfile import NamedTemporaryFile


def main():
    _dict = literal_eval(sys.argv[1])
    with NamedTemporaryFile("w") as temp:
        json.dump(_dict, temp)
        temp.flush()
        cmd = f'statelint "{temp.name}"'
        process = Popen(cmd, shell=True)
        process.communicate()


if __name__ == "__main__":
    main()
