import pytest
from bufap.parser import setup


@pytest.mark.parametrize(
    ("conf", "expected"),
    [
        (
            "setup apname enterprise-network",
            {"setup": {"apname": "enterprise-network"}},
        ),
        # #("setup password user password abc789",),
        # #("setup username admin administrator password pass123",),
        ("setup date 2019/11/16 12:34:56", {"setup": {"date": "2019/11/16 12:34:56"}}),
        (
            "setup ntp client enable server buffalo.jp interval 24",
            {
                "setup": {
                    "ntp": {
                        "client": {
                            "enable": "enable",
                            "server": "buffalo.jp",
                            "ntp-interval": "24",
                        }
                    }
                }
            },
        ),
        (
            "setup ntp client disable",
            {
                "setup": {
                    "ntp": {
                        "client": {
                            "enable": "disable",
                            "server": None,
                            "ntp-interval": None,
                        }
                    }
                }
            },
        ),
        (
            "setup ntp server disable",
            {"setup": {"ntp": {"server": {"enable": "disable"}}}},
        ),
        ("setup timezone +0900", {"setup": {"timezone": "+0900"}}),
        ("setup timezone UTC", {"setup": {"timezone": "UTC"}}),
        (
            "setup syslog client enable server 192.168.11.202",
            {
                "setup": {
                    "syslog": {
                        "client": {"enable": "enable", "server": "192.168.11.202"}
                    }
                }
            },
        ),
        (
            "setup syslog client disable",
            {"setup": {"syslog": {"client": {"enable": "disable", "server": None}}}},
        ),
        (
            "setup syslog client facility wireless enable",
            {"setup": {"syslog": {"client": {"facility": {"wireless": "enable"}}}}},
        ),
        (
            "setup syslog client usb enable",
            {"setup": {"syslog": {"client": {"usb": {"enable": "enable"}}}}},
        ),
        (
            "setup management http disable",
            {"setup": {"management": {"http": "disable"}}},
        ),
        (
            "setup management telnet disable",
            {"setup": {"management": {"telnet": "disable"}}},
        ),
        # #("setup management adt3 init force",),
        (
            "setup management remote-adt enable remote-host.com 22401 12345678",
            {
                "setup": {
                    "management": {
                        "remote-adt": {
                            "enable": "enable",
                            "host": "remote-host.com",
                            "port": "22401",
                            "pin": "12345678",
                        }
                    }
                }
            },
        ),
        (
            "setup management snmp agent enable version v1v2 get public set private",
            {
                "setup": {
                    "management": {
                        "snmp": {
                            "agent": {
                                "enable": "enable",
                                "version": "v1v2",
                                "get": "public",
                                "set": "private",
                            }
                        }
                    }
                }
            },
        ),
        (
            "setup management snmp trap enable comm public manager 192.168.11.200",
            {
                "setup": {
                    "management": {
                        "snmp": {
                            "trap": {
                                "enable": "enable",
                                "trapcomm": "public",
                                "manager": "192.168.11.200",
                            }
                        }
                    }
                }
            },
        ),
        (
            "setup management remote-management-service enable",
            {
                "setup": {
                    "management": {
                        "remote-management-service": {
                            "enable": "enable",
                        }
                    }
                }
            },
        ),
        (
            "setup management proxy enable 192.168.11.105 8080 buffalo abcd1234",
            {
                "setup": {
                    "management": {
                        "proxy": {
                            "enable": "enable",
                            "host": "192.168.11.105",
                            "port": "8080",
                            "username": "buffalo",
                            "password": "abcd1234",
                        }
                    }
                }
            },
        ),
        (
            "setup authuser add buffalo 123456",
            {"setup": {"authuser": {"buffalo": "123456"}}},
        ),
        ("setup led power disable", {"setup": {"led": {"power": "disable"}}}),
        (
            "setup rebootscheduler enable",
            {"setup": {"rebootscheduler": {"enable": "enable"}}},
        ),
        (
            "setup rebootscheduler week fri enable",
            {"setup": {"rebootscheduler": {"fri": "enable"}}},
        ),
        (
            "setup rebootscheduler week sat enable",
            {"setup": {"rebootscheduler": {"sat": "enable"}}},
        ),
        (
            "setup rebootscheduler time 3 30",
            {"setup": {"rebootscheduler": {"time": "3 30"}}},
        ),
        ("setup urgent-mode enable", {"setup": {"urgent-mode": "enable"}}),
    ],
)
def test_parse(conf: str, expected: dict):
    assert setup.parse(conf) == expected
