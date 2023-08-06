import re
from typing import Optional


def parse(conf) -> Optional[dict]:
    # logging.debug("setup.parse")

    m = re.match(r"setup apname (?P<apname>\S+)", conf)
    if m:
        return {"setup": {"apname": m.group("apname")}}

    m = re.match(r"setup date (?P<date>[0-9:\/\s]+)", conf)
    if m:
        return {"setup": {"date": m.group("date")}}

    m = re.match(r"setup username (?P<usertype>admin|user) (?P<username>\S+)", conf)
    if m:
        return {
            "setup": {
                "usertype": m.group("usertype"),
                "username": m.group("username"),
            }
        }

    m = re.match(
        r"setup ntp client (?P<enable>enable server (?P<server>\S+) interval (?P<ntpinterval>\d+)|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "ntp": {
                    "client": {
                        "enable": "disable"
                        if m.group("enable") == "disable"
                        else "enable",
                        "server": m.group("server"),
                        "ntp-interval": m.group("ntpinterval"),
                    }
                }
            }
        }

    m = re.match("setup ntp server (?P<enable>enable|disable)", conf)
    if m:
        return {
            "setup": {
                "ntp": {
                    "server": {
                        "enable": "disable"
                        if m.group("enable") == "disable"
                        else "enable"
                    }
                }
            }
        }

    m = re.match(r"setup timezone (?P<timezone>\S+)", conf)
    if m:
        return {"setup": {"timezone": m.group("timezone")}}

    m = re.match(
        r"setup syslog client (?P<enable>enable server (?P<servername>\S+)|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "syslog": {
                    "client": {
                        "enable": "disable"
                        if m.group("enable") == "disable"
                        else "enable",
                        "server": m.group("servername"),
                    }
                }
            }
        }

    m = re.match(
        r"setup syslog client facility (?P<facility>\S+) (?P<enable>enable|disable)",
        conf,
    )
    if m:
        enable = "enable" if m.group("enable") == "enable" else "disable"
        return {
            "setup": {"syslog": {"client": {"facility": {m.group("facility"): enable}}}}
        }

    m = re.match(r"setup syslog client usb (?P<enable>enable|disable)", conf)
    if m:
        return {
            "setup": {
                "syslog": {
                    "client": {
                        "usb": {
                            "enable": "enable"
                            if m.group("enable") == "enable"
                            else "disable"
                        }
                    }
                }
            }
        }

    m = re.match(
        r"setup management (?P<proto>http|https|telnet|ssh) (?P<enable>enable|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    m.group("proto"): "enable"
                    if m.group("enable") == "enable"
                    else "disable"
                }
            }
        }

    m = re.match(
        r"setup management remote-adt (?P<enable>enable (?P<host>\S+) (?P<port>\S+) (?P<pin>\S+)|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "remote-adt": {
                        "enable": "disable"
                        if m.group("enable") == "disable"
                        else "enable",
                        "host": m.group("host"),
                        "port": m.group("port"),
                        "pin": m.group("pin"),
                    }
                }
            }
        }

    m = re.match(
        r"setup management snmp agent (?P<enable>enable version ((?P<version>v1v2) get (?P<get>\S+) set (?P<set>\S+)|v3)|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "snmp": {
                        "agent": {
                            "enable": "disable"
                            if m.group("enable") == "disable"
                            else "enable",
                            "version": m.group("version"),
                            "get": m.group("get"),
                            "set": m.group("set"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"setup management snmp trap (?P<enable>enable (comm (?P<trapcomm>\S+) |)manager (?P<manager>\S+)|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "snmp": {
                        "trap": {
                            "enable": "disable"
                            if m.group("enable") == "disable"
                            else "enable",
                            "trapcomm": m.group("trapcomm"),
                            "manager": m.group("manager"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"setup management remote-management-service (?P<enable>enable|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "remote-management-service": {"enable": m.group("enable")}
                }
            }
        }

    m = re.match(
        r"setup management remote-management-service cloud-setting (?P<enable>enable|disable)",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "remote-management-service": {
                        "cloud-setting": {"enable": m.group("enable")}
                    }
                }
            }
        }

    m = re.match(
        r"setup management proxy (?P<enable>disable|enable (?P<host>\S+) (?P<port>\S+)( (?P<username>\S+) (?P<password>\S+))*)$",
        conf,
    )
    if m:
        return {
            "setup": {
                "management": {
                    "proxy": {
                        "enable": "disable"
                        if m.group("enable") == "disable"
                        else "enable",
                        "host": m.group("host"),
                        "port": m.group("port"),
                        "username": m.group("username"),
                        "password": m.group("password"),
                    }
                }
            }
        }

    m = re.match(r"setup authuser add (?P<username>\S+)\s*(?P<password>\S+)$", conf)
    if m:
        return {"setup": {"authuser": {m.group("username"): m.group("password")}}}

    m = re.match(r"setup led (?P<type>\S+) (?P<enable>\S+)", conf)
    if m:
        return {"setup": {"led": {m.group("type"): m.group("enable")}}}

    m = re.match(r"setup rebootscheduler (?P<enable>enable|disable)", conf)
    if m:
        return {
            "setup": {
                "rebootscheduler": {
                    "enable": m.group("enable"),
                }
            }
        }

    m = re.match(
        r"setup rebootscheduler week (?P<week>\S+) (?P<enable>enable|disable)", conf
    )
    if m:
        return {
            "setup": {
                "rebootscheduler": {
                    m.group("week"): m.group("enable"),
                }
            }
        }

    m = re.match(r"setup rebootscheduler time (?P<time>\d+ \d+)", conf)
    if m:
        return {"setup": {"rebootscheduler": {"time": m.group("time")}}}

    m = re.match(r"setup urgent-mode (?P<enable>enable|disable)", conf)
    if m:
        return {"setup": {"urgent-mode": m.group("enable")}}

    return None
