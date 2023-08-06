import re
from typing import Optional


ssidname = ""


def parse(conf: str) -> Optional[dict]:
    # logging.debug("radius:parse")

    m = re.match(
        r"radius (?P<server>primary|secondary) (?P<enable>enable|disable)$",
        conf,
    )
    if m:
        return {"radius": {m.group("server"): {"enable": m.group("enable")}}}

    m = re.match(
        r"radius (?P<server>primary|secondary) accounting (?P<enable>enable|disable)$",
        conf,
    )
    if m:
        return {
            "radius": {m.group("server"): {"accounting": {"enable": m.group("enable")}}}
        }

    m = re.match(
        r"radius (?P<server>primary|secondary) (?P<enable>enable|disable) (?P<type>server (?P<host>\S+) secret (?P<secret>\S+)|internal_server)$",
        conf,
    )
    if m:
        return {
            "radius": {
                m.group("server"): {
                    "enable": m.group("enable"),
                    "type": "internal_server"
                    if m.group("type") == "internal_server"
                    else "server",
                    "host": m.group("host"),
                    "secret": m.group("secret"),
                }
            }
        }

    m = re.match(
        r"radius (?P<server>primary|secondary) (?P<param>\S+) (?P<value>\S+)$",
        conf,
    )
    if m:
        return {"radius": {m.group("server"): {m.group("param"): m.group("value")}}}

    m = re.match(
        r"radius (?P<param>\S+) (?P<value>\S+)$",
        conf,
    )
    if m:
        return {"radius": {m.group("param"): m.group("value")}}

    m = re.match(
        r"radius internal_server (?P<param>\S+) (?P<value>\S+)",
        conf,
    )
    if m:
        return {"radius": {"internal_server": {m.group("param"): m.group("value")}}}

    m = re.match(
        r"radius asam (?P<enable>enable auth secret key (?P<key>\S+)|disable)$",
        conf,
    )
    if m:
        return {
            "radius": {
                "asam": {
                    "enable": "disable" if m.group("enable") == "disable" else "enable",
                    "key": m.group("key"),
                }
            }
        }

    return None
