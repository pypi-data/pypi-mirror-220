import pytest
from bufap.parser import bridge


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        ("bridge aging 10", {"bridge": {"aging": "10"}}),
        ("bridge bpdu-forward disable", {"bridge": {"bpdu-forward": "disable"}}),
        ("bridge stp enable", {"bridge": {"stp": "enable"}}),
        ("bridge stp mode rstp", {"bridge": {"stp": {"mode": "rstp"}}}),
        ("bridge stp priority 40000", {"bridge": {"stp": {"priority": "40000"}}}),
        ("bridge stp fwdelay 20", {"bridge": {"stp": {"fwdelay": "20"}}}),
        ("bridge stp maxage 30", {"bridge": {"stp": {"maxage": "30"}}}),
        ("bridge stp tx-holdcount 8", {"bridge": {"stp": {"tx-holdcount": "8"}}}),
        ("bridge stp autoedge enable", {"bridge": {"stp": {"autoedge": "enable"}}}),
        (
            "bridge stp port ssidnum 3 priority 30 cost 60 edgeport disable ptop disable",
            {
                "bridge": {
                    "stp": {
                        "port": {
                            "ssid": {
                                "3": {
                                    "priority": "30",
                                    "cost": "60",
                                    "edgeport": "disable",
                                    "ptop": "disable",
                                }
                            }
                        }
                    }
                }
            },
        ),
        (
            "bridge stp port wds 11g peernum 5 priority 40 cost 50 edgeport enable ptop disable",
            {
                "bridge": {
                    "stp": {
                        "port": {
                            "wds": {
                                "5": {
                                    "band": "11g",
                                    "priority": "40",
                                    "cost": "50",
                                    "edgeport": "enable",
                                    "ptop": "disable",
                                }
                            }
                        }
                    }
                }
            },
        ),
        (
            "bridge stp port ether 1 priority 20 cost 50 edgeport enable ptop enable",
            {
                "bridge": {
                    "stp": {
                        "port": {
                            "ether": {
                                "1": {
                                    "priority": "20",
                                    "cost": "50",
                                    "edgeport": "enable",
                                    "ptop": "enable",
                                }
                            }
                        }
                    }
                }
            },
        ),
    ],
)
def test_parse(conf: str, expected: dict):
    assert bridge.parse(conf) == expected
