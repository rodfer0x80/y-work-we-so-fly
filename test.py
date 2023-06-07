#!/usr/bin/env python3


import os
import sys

import requests


def findSourceAshby(link):
    keyword = "ashby"
    # page = requests.get(link)
    # for line in page.text.split("\n"):
    #     if keyword in line:
    #         return True
    # return False
    if "jobs.ashbyhq.com" in link:
        return True
    return False


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)
    print(findSourceAshby(sys.argv[1]))
    sys.exit(0)
