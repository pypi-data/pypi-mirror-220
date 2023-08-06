import pytest
from bufap.parser import ip


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        (
            "ip lan address 192.168.30.28/255.255.255.0",
            {
                "ip": {
                    "lan": {
                        "address": "192.168.30.28",
                        "maskip": "255.255.255.0",
                        "dhcp": None,
                    }
                }
            },
        ),
        ("ip lan vlan 20", {"ip": {"lan": {"vlan": "20"}}}),
        ("ip defaultgw 192.168.0.250", {"ip": {"defaultgw": "192.168.0.250"}}),
        ("ip dns primary 192.168.11.1", {"ip": {"dns": {"primary": "192.168.11.1"}}}),
        (
            "ip dns secondary 192.168.11.2",
            {"ip": {"dns": {"secondary": "192.168.11.2"}}},
        ),
        (
            "ip dhcp-server disable",
            {
                "ip": {
                    "dhcp-server": {
                        "enable": "disable",
                        "lease_from_addr": None,
                        "lease_range_num": None,
                    }
                }
            },
        ),
        (
            "ip dhcp-server enable 192.168.11.2 num 30",
            {
                "ip": {
                    "dhcp-server": {
                        "enable": "enable",
                        "lease_from_addr": "192.168.11.2",
                        "lease_range_num": "30",
                    }
                }
            },
        ),
        (
            "ip dhcp-server option lease-time 24",
            {"ip": {"dhcp-server": {"option": {"lease-time": "24"}}}},
        ),
        (
            "ip dhcp-server option gateway none",
            {"ip": {"dhcp-server": {"option": {"gateway": "none"}}}},
        ),
        (
            "ip dhcp-server option dns 192.168.11.1",
            {"ip": {"dhcp-server": {"option": {"dns": "192.168.11.1"}}}},
        ),
        ("ip proxyarp enable", {"ip": {"proxyarp": {"enable": "enable"}}}),
    ],
)
def test_parse(conf: str, expected: dict):
    assert ip.parse(conf) == expected
