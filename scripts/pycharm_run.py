#!/usr/bin/env python3

import os
import sys

def main():
    cmd = " cd ..;\
            test -e ./venv || python3 -m venv venv &&\
            source ./venv/bin/activate && pip install --upgrade pip &&\
            pip install -r requirements.txt;\
            source ./venv/bin/activate && python ./__main__.py"
    os.system(cmd)
    return 0


if __name__ == '__main__':
    sys.exit(main())
