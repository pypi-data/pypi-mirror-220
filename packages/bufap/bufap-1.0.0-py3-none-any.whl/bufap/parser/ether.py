import re
from typing import Optional

"""
ether:
    <port no>:
        link:enable|disable
        media:
            mdi: auto|normal
            speed: auto|10|100|1000|2500
            flowctl: enable
            duplex: full|half
        vlan:
            mode: hybrid|untagged|tagged|multiple
            pvid:
            lan-vid:
            mvid[1-3]:
        8023az: enable|disable
"""


def parse(conf) -> Optional[dict]:
    # logging.debug("setup.ether")

    m = re.match(r"ether port (?P<port>\d) link (?P<enable>enable|disable)", conf)
    if m:
        return {"ether": {"port": {m.group("port"): {"link": m.group("enable")}}}}

    m = re.match(
        r"ether port (?P<port>\d) media mdi (?P<mdi>\S+) speed (?P<speed>\S+)\s*(duplex (?P<duplex>full|half)|)* flowctl (?P<flowctl>enable|disable)",
        conf,
    )
    if m:
        return {
            "ether": {
                "port": {
                    m.group("port"): {
                        "media": {
                            "mdi": m.group("mdi"),
                            "speed": m.group("speed"),
                            "duplex": m.group("duplex"),
                            "flowctl": m.group("flowctl"),
                        }
                    }
                }
            }
        }

    m = re.match(r"ether port (?P<port>\d) vlan mode tagged", conf)
    if m:
        return {"ether": {"port": {m.group("port"): {"vlan_mode": "tagged"}}}}

    m = re.match(
        r"ether port (?P<port>\d) vlan mode (?P<vlan_mode>hybrid|untagged) vlan (?P<pvid>\d+) lan-vid (?P<lan_vid>\d+)",
        conf,
    )
    if m:
        return {
            "ether": {
                "port": {
                    m.group("port"): {
                        "vlan": {
                            "mode": m.group("vlan_mode"),
                            "lan-vid": m.group("lan_vid"),
                            "vlan": m.group("pvid"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"ether port (?P<port>\d) vlan mode multiple vlan (?P<pvid>\d+) additional (?P<mvid1>\d+) (?P<mvid2>\d+)*\s*(?P<mvid3>\d+)*\s*lan-vid (?P<lan_vid>\d+)",
        conf,
    )
    if m:
        return {
            "ether": {
                "port": {
                    m.group("port"): {
                        "vlan": {
                            "mode": "multiple",
                            "vlan": m.group("pvid"),
                            "mvid1": m.group("mvid1"),
                            "mvid2": m.group("mvid2"),
                            "mvid3": m.group("mvid3"),
                            "lan-vid": m.group("lan_vid"),
                        }
                    }
                }
            }
        }

    m = re.match(r"ether port (?P<port>\d) 8023az (?P<enable>enable|disable)", conf)
    if m:
        return {"ether": {"port": {m.group("port"): {"8023az": m.group("enable")}}}}

    return None
