#!/usr/bin/env python3


import os
import sys

from src.bot import *


def main():
    #if len(sys.argv) != 2:
    #    sys.stdoud.write("Usage: {__file__} <batchfile_path>\n")
    #    return 1
    #else:
    #    batchfile = sys.argv[1]
    batchfile = "./data/preapply.txt"

    bot = Bot()
    
    bot.applyBatch(batchfile)
    #bot.test()

    return 0


if __name__ == '__main__':
    sys.exit(main())
