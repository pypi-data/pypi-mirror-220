import re
from typing import Optional


def parse(conf) -> Optional[dict]:
    # logging.debug("setup.ip")

    m = re.match(
        r"ip lan address (?P<dhcp>(?P<address>\S+)/(?P<maskip>\S+)|dhcp)", conf
    )
    if m:
        return {
            "ip": {
                "lan": {
                    "address": m.group("address"),
                    "maskip": m.group("maskip"),
                    "dhcp": "dhcp" if m.group("dhcp") == "dhcp" else None,
                }
            }
        }

    m = re.match(r"ip lan vlan (?P<id>\d+)", conf)
    if m:
        return {"ip": {"lan": {"vlan": m.group("id")}}}

    m = re.match(r"ip defaultgw (?P<gateway>\S+)", conf)
    if m:
        return {"ip": {"defaultgw": m.group("gateway")}}

    m = re.match(r"ip dns (?P<type>primary|secondary) (?P<dnsserver>\S+)", conf)
    if m:
        return {
            "ip": {
                "dns": {
                    m.group("type"): ""
                    if m.group("dnsserver") == "clear"
                    else m.group("dnsserver"),
                }
            }
        }

    m = re.match(
        r"ip dhcp-server (?P<enable>enable (?P<lease_from_addr>\S+) num (?P<lease_range_num>\d+)|disable)",
        conf,
    )
    if m:
        return {
            "ip": {
                "dhcp-server": {
                    "enable": "disable" if m.group("enable") == "disable" else "enable",
                    "lease_from_addr": m.group("lease_from_addr"),
                    "lease_range_num": m.group("lease_range_num"),
                }
            }
        }

    m = re.match(r"ip dhcp-server option (?P<option>\S+) (?P<value>\S+)", conf)
    if m:
        return {
            "ip": {"dhcp-server": {"option": {m.group("option"): m.group("value")}}}
        }

    m = re.match(r"ip proxyarp (?P<enable>enable|disable)", conf)
    if m:
        return {"ip": {"proxyarp": {"enable": m.group("enable")}}}

    return None
