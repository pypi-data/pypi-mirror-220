import pytest
from bufap.parser import ether


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        ("ether port 1 link enable", {"ether": {"port": {"1": {"link": "enable"}}}}),
        ("ether port 2 link disable", {"ether": {"port": {"2": {"link": "disable"}}}}),
        (
            "ether port 1 media mdi auto speed 100 flowctl enable",
            {
                "ether": {
                    "port": {
                        "1": {
                            "media": {
                                "duplex": None,
                                "mdi": "auto",
                                "speed": "100",
                                "flowctl": "enable",
                            }
                        }
                    }
                }
            },
        ),
        (
            "ether port 2 media mdi normal speed 1000 duplex full flowctl disable",
            {
                "ether": {
                    "port": {
                        "2": {
                            "media": {
                                "mdi": "normal",
                                "speed": "1000",
                                "duplex": "full",
                                "flowctl": "disable",
                            }
                        }
                    }
                }
            },
        ),
        (
            "ether port 1 vlan mode hybrid vlan 1 lan-vid 1",
            {
                "ether": {
                    "port": {
                        "1": {"vlan": {"mode": "hybrid", "vlan": "1", "lan-vid": "1"}}
                    }
                }
            },
        ),
        (
            "ether port 2 vlan mode multiple vlan 200 additional 300 lan-vid 200",
            {
                "ether": {
                    "port": {
                        "2": {
                            "vlan": {
                                "mode": "multiple",
                                "vlan": "200",
                                "mvid1": "300",
                                "mvid2": None,
                                "mvid3": None,
                                "lan-vid": "200",
                            }
                        }
                    }
                }
            },
        ),
        # (
        #     "ether port 3 vlan mode multiple vlan 200 additional 300 400 lan-vid 200",
        #     {
        #         "ether": {
        #             "port": {
        #                 "3": {
        #                     "vlan": {
        #                         "mode": "multiple",
        #                         "vlan": "200",
        #                         "mvid1": "300",
        #                         "mvid2": "400",
        #                         "lan-vid": "200",
        #                     }
        #                 }
        #             }
        #         }
        #     },
        # ),
        # (
        #     "ether port 4 vlan mode multiple vlan 200 additional 300 400 500 lan-vid 200",
        #     {
        #         "ether": {
        #             "port": {
        #                 "2": {
        #                     "vlan": {
        #                         "mode": "multiple",
        #                         "vlan": "200",
        #                         "mvid1": "300",
        #                         "mvid2": "400",
        #                         "mvid3": "500",
        #                         "lan-vid": "200",
        #                     }
        #                 }
        #             }
        #         }
        #     },
        # ),
        # (
        #     "ether port 1 8023az enable",
        #     {"ether": {"port": {"1": {"8023az": "enable"}}}},
        # ),
    ],
)
def test_parse(conf: str, expected: dict):
    assert ether.parse(conf) == expected
