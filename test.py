#!/usr/bin/env python3


import requests
import sys


def findSourceTeamtailor(link: str):
    keyword = "teamtailor"
    page = requests.get(link)
    for line in page.text.split("\n"):
        if keyword in line:
            return True
    return False


def main():
    if len(sys.argv) < 2:
        return 1

    print(findSourceTeamtailor(sys.argv[1]))

    return 0


if __name__ == '__main__':
    sys.exit(main())
