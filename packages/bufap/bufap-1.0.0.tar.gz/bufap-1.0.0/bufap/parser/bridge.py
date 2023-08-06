import re
from typing import Optional

ssidname = ""


def parse(conf: str) -> Optional[dict]:
    # logging.debug("bridge")

    m = re.match(
        "bridge (?P<command>\S+) (?P<value>\S+)$",
        conf,
    )
    if m:
        return {"bridge": {m.group("command"): m.group("value")}}

    m = re.match(
        "bridge stp (?P<command>\S+) (?P<value>\S+)$",
        conf,
    )
    if m:
        return {"bridge": {"stp": {m.group("command"): m.group("value")}}}

    m = re.match(
        r"bridge stp port (?P<conf>.*)",
        conf,
    )
    if m:
        return _parse_stp_port(m.group("conf"))

    return None


def _parse_stp_port(conf: str) -> dict:
    m = re.match(
        r"ssidnum (?P<ssidnum>\d+) priority (?P<priority>\d+) cost (?P<cost>\d+) edgeport (?P<state1>\S+) ptop (?P<state2>\S+)",
        conf,
    )
    if m:
        return {
            "bridge": {
                "stp": {
                    "port": {
                        "ssid": {
                            m.group("ssidnum"): {
                                "priority": m.group("priority"),
                                "cost": m.group("cost"),
                                "edgeport": m.group("state1"),
                                "ptop": m.group("state2"),
                            }
                        }
                    }
                }
            }
        }

    m = re.match(
        r"wds (?P<band>\S+) peernum (?P<peernum>\d+) priority (?P<priority>\d+) cost (?P<cost>\d+) edgeport (?P<state1>\S+) ptop (?P<state2>\S+)",
        conf,
    )
    if m:
        return {
            "bridge": {
                "stp": {
                    "port": {
                        "wds": {
                            m.group("peernum"): {
                                "band": m.group("band"),
                                "priority": m.group("priority"),
                                "cost": m.group("cost"),
                                "edgeport": m.group("state1"),
                                "ptop": m.group("state2"),
                            }
                        }
                    }
                }
            }
        }

    m = re.match(
        r"ether (?P<port>\d+) priority (?P<priority>\d+) cost (?P<cost>\d+) edgeport (?P<state1>\S+) ptop (?P<state2>\S+)",
        conf,
    )
    if m:
        return {
            "bridge": {
                "stp": {
                    "port": {
                        "ether": {
                            m.group("port"): {
                                "priority": m.group("priority"),
                                "cost": m.group("cost"),
                                "edgeport": m.group("state1"),
                                "ptop": m.group("state2"),
                            }
                        }
                    }
                }
            }
        }

    return None
