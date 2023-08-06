import logging
import math
import os
import re
import sys
import time

from ouilookup import OuiLookup


def print_waiting(message: str, seconds: int) -> None:
    for i in range(seconds):
        time.sleep(1)
        periods = "." * i
        print(f"\r{message} {periods}", end="", file=sys.stderr)
    print("")


def mac2vendor(mac) -> str:
    if mac[1] in "2367abefABEF":
        vendor = "<Random MAC>"
    else:
        data_file = os.path.join(os.getcwd(), "ouilookup.json")
        if not os.path.exists(data_file):
            logging.debug("update ouilookup data file")
            OuiLookup(data_file=data_file).update()

        vendors = OuiLookup(data_file="ouilookup.json").query(mac)
        if len(vendors) > 0:
            vendor = list(vendors[0].values())[0]
        else:
            vendor = "<Unknown>"

    return vendor


def convert_to_byte(size: str, unit="B") -> int:
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    m = re.match(r"(?P<size>[0-9\.]+)(?P<unit>\SB)", size)
    if not m:
        raise ValueError(f"invalid syntax: {size}")

    i = units.index(m.group("unit").upper())
    byte = int(float(m.group("size")) * (1000**i))

    return byte
