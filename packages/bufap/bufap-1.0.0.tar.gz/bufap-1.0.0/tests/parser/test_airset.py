import pytest

from bufap.parser import airset


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        (
            "airset ssid steering-policy disable",
            {"airset": {"steering-policy": "disable"}},
        ),
        (
            'airset ssid add ssidname "test-2" band 11g enable 11a disable vlanid 1 auth wpa2psk cipher aes rekey 60 key "password!!" mfp optional fast-trans enable mdid 1111',
            {},
        ),
        (
            "airset ssid disable ssidnum 1",
            {"airset": {"ssid": {"1": {"enable": "disable", "ssidname": "test-2"}}}},
        ),
        (
            "airset ssid band ssidnum 1 11g enable 11a disable",
            {
                "airset": {
                    "ssid": {
                        "1": {"band": {"11g": "enable", "11a": "disable", "6g": None}}
                    }
                }
            },
        ),
        (
            "airset ssid anyscan ssidnum 1 enable",
            {"airset": {"ssid": {"1": {"anyscan": "enable"}}}},
        ),
        (
            "airset ssid privacy ssidnum 1 disable",
            {"airset": {"ssid": {"1": {"privacy": "disable"}}}},
        ),
        (
            "airset ssid vlan ssidnum 1 mode untagged vlanid 1",
            {
                "airset": {
                    "ssid": {
                        "1": {
                            "vlan": {
                                "mode": "untagged",
                                "vlanid": "1",
                                "mvid1": None,
                                "mvid2": None,
                                "mvid3": None,
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid vlan ssidnum 2 mode multiple vlanid 1 additional 10",
            {
                "airset": {
                    "ssid": {
                        "2": {
                            "vlan": {
                                "mode": "multiple",
                                "vlanid": "1",
                                "mvid1": "10",
                                "mvid2": None,
                                "mvid3": None,
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid vlan ssidnum 3 mode multiple vlanid 1 additional 10 20",
            {
                "airset": {
                    "ssid": {
                        "3": {
                            "vlan": {
                                "mode": "multiple",
                                "vlanid": "1",
                                "mvid1": "10",
                                "mvid2": "20",
                                "mvid3": None,
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid vlan ssidnum 4 mode multiple vlanid 1 additional 10 20 30",
            {
                "airset": {
                    "ssid": {
                        "4": {
                            "vlan": {
                                "mode": "multiple",
                                "vlanid": "1",
                                "mvid1": "10",
                                "mvid2": "20",
                                "mvid3": "30",
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid priority ssidnum 1 prioritize",
            {"airset": {"ssid": {"1": {"priority": "prioritize"}}}},
        ),
        (
            "airset ssid using-mode ssidnum 1 both",
            {"airset": {"ssid": {"1": {"using-mode": "both"}}}},
        ),
        (
            "airset ssid band-steering ssidnum 1 enable",
            {"airset": {"ssid": {"1": {"band-steering": "enable"}}}},
        ),
        (
            "airset ssid load-balancing ssidnum 1 11g 256 11a 256",
            {
                "airset": {
                    "ssid": {
                        "1": {
                            "load-balancing": {"11g": "256", "11a": "256", "6g": None}
                        }
                    }
                }
            },
        ),
        (
            'airset ssid security ssidnum 1 auth wpa2psk cipher aes rekey 60 key "password!!" mfp optional fast-trans enable mdid 1111',
            {
                "airset": {
                    "ssid": {
                        "1": {
                            "auth": "wpa2psk",
                            "cipher": "aes",
                            "rekey": "60",
                            "key": "password!!",
                            "mfp": "optional",
                            "fast-trans": "enable",
                            "mdid": "1111",
                        }
                    }
                }
            },
        ),
        (
            "airset ssid addsecurity ssidnum 1 mode acl",
            {
                "airset": {
                    "ssid": {
                        "1": {
                            "addsecurity": {
                                "mode": "acl",
                                "radius-mode": None,
                                "authpass": None,
                            }
                        }
                    }
                }
            },
        ),
        (
            'airset ssid addsecurity ssidnum 2 mode macradius authpass "12345678"',
            {
                "airset": {
                    "ssid": {
                        "2": {
                            "addsecurity": {
                                "mode": "macradius",
                                "radius-mode": "authpass",
                                "authpass": "12345678",
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset 11g channel 1 bandwidth 20m",
            {
                "airset": {
                    "band": {
                        "11g": {
                            "channel": "1",
                            "bandwidth": "20m",
                            "scaninterval": None,
                            "uncond": None,
                        }
                    }
                }
            },
        ),
        (
            "airset 11a channel auto_w52w53w56 bandwidth 40m scaninterval 60",
            {
                "airset": {
                    "band": {
                        "11a": {
                            "channel": "auto_w52w53w56",
                            "bandwidth": "40m",
                            "scaninterval": "60",
                            "uncond": None,
                        }
                    }
                }
            },
        ),
        ("airset 11a mrate auto", {"airset": {"band": {"11a": {"mrate": "auto"}}}}),
        ("airset 11a txpower 100", {"airset": {"band": {"11a": {"txpower": "100"}}}}),
        (
            "airset 11a beacon-period 100",
            {"airset": {"band": {"11a": {"beacon-period": "100"}}}},
        ),
        ("airset 11a dtim 1", {"airset": {"band": {"11a": {"dtim": "1"}}}}),
        (
            "airset wmm ap type background param cwmin 15",
            {"airset": {"wmm": {"ap": {"background": {"cwmin": "15"}}}}},
        ),
        (
            "airset wmm ap type besteffort param txopl 0",
            {"airset": {"wmm": {"ap": {"besteffort": {"txopl": "0"}}}}},
        ),
        (
            "airset wmm ap type video param cwmin 7",
            {"airset": {"wmm": {"ap": {"video": {"cwmin": "7"}}}}},
        ),
        (
            "airset wmm sta type background param cwmin 15",
            {"airset": {"wmm": {"sta": {"background": {"cwmin": "15"}}}}},
        ),
        (
            "airset wmm sta type besteffort param txopl 0",
            {"airset": {"wmm": {"sta": {"besteffort": {"txopl": "0"}}}}},
        ),
        (
            "airset wmm sta type video param cwmin 7",
            {"airset": {"wmm": {"sta": {"video": {"cwmin": "7"}}}}},
        ),
        ("airset scheduler enable", {"airset": {"scheduler": {"enable": "enable"}}}),
        (
            "airset scheduler add ssidnum 1 week sat starttime 12 10 endtime 13 30",
            {
                "airset": {
                    "ssid": {
                        "1": {
                            "scheduler": {
                                "sat": {"starttime": "12 10", "endtime": "13 30"}
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid radius ssidnum 2 server radius-setting",
            {
                "airset": {
                    "ssid": {
                        "2": {
                            "radius": {
                                "mode": "radius-setting",
                                "primary": {"host": None, "secret": None},
                                "secondary": {"host": None, "secret": None},
                            }
                        }
                    }
                }
            },
        ),
        (
            "airset ssid radius ssidnum 2 server each-ssid primary 192.168.11.10 buffalo",
            {
                "airset": {
                    "ssid": {
                        "2": {
                            "radius": {
                                "mode": "each-ssid",
                                "primary": {
                                    "host": "192.168.11.10",
                                    "secret": "buffalo",
                                },
                                "secondary": {
                                    "host": None,
                                    "secret": None,
                                },
                            }
                        }
                    }
                }
            },
        ),
    ],
)
def test_parse(conf: str, expected: dict):
    assert airset.parse(conf) == expected
