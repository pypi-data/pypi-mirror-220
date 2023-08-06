import re
from typing import Optional

from dictknife import deepmerge

ssidname = ""


def parse(conf: str) -> Optional[dict]:
    # logging.debug("airset")

    if conf.startswith("airset linkitg"):
        return parse_linkitg(conf)

    m = re.match(
        r"airset ssid (?P<conf>.*)",
        conf,
    )
    if m:
        return parse_ssid(m.group("conf"))

    m = re.match("airset (?P<band>11g|11a|6g) (?P<conf>.*)", conf)
    if m:
        return parse_band(m.group("band"), m.group("conf"))

    m = re.match(
        r"airset wmm (?P<apsta>ap|sta) type (?P<type>\S+) param (?P<param>\S+) (?P<value>\S+)",
        conf,
    )
    if m:
        return {
            "airset": {
                "wmm": {
                    m.group("apsta"): {
                        m.group("type"): {m.group("param"): m.group("value")}
                    }
                }
            }
        }

    m = re.match(r"airset maclist add (?P<macaddress>\S+)", conf)
    if m:
        return {
            "airset": {
                "maclist": {
                    m.group("macaddress"): "None",
                }
            }
        }

    m = re.match(
        r"airset scheduler (?P<enable>enable|disable)",
        conf,
    )
    if m:
        return {"airset": {"scheduler": {"enable": m.group("enable")}}}

    m = re.match(
        r"airset scheduler add ssidnum (?P<ssidnum>\d+) week (?P<week>\S+) starttime (?P<starttime>\d+ \d+) endtime (?P<endtime>\d+ \d+)",
        conf,
    )
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "scheduler": {
                            m.group("week"): {
                                "starttime": m.group("starttime"),
                                "endtime": m.group("endtime"),
                            }
                        }
                    }
                }
            }
        }
    return None


def parse_band(band: str, conf: str) -> Optional[dict]:
    # logging.debug("parse_band")

    m = re.match(
        r"wireless (?P<enable>enable|disable)",
        conf,
    )
    if m:
        return {"airset": {"band": {band: {"enable": m.group("enable")}}}}

    m = re.match(
        r"channel (?P<channel>\S+) bandwidth (?P<bandwidth>\S+)( scaninterval (?P<scaninterval>\d+))*( (?P<uncond>uncond))*",
        conf,
    )
    if m:
        return {
            "airset": {
                "band": {
                    band: {
                        "channel": m.group("channel"),
                        "bandwidth": m.group("bandwidth"),
                        "scaninterval": m.group("scaninterval"),
                        "uncond": m.group("uncond"),
                    }
                }
            }
        }

    m = re.match(
        r"(?P<option>\S+) (?P<value>\S+)$",
        conf,
    )
    if m:
        return {"airset": {"band": {band: {m.group("option"): m.group("value")}}}}

    return None


def parse_linkitg(conf: str) -> dict:
    m = re.match(
        r"airset linkitg (?P<enable>enable (?P<host>\S+) (?P<interval>\d+) (?P<retry>\d+)|disable)",
        conf,
    )
    if m:
        return {
            "airset": {
                "linkitg": {
                    "enable": "disable" if m.group("enable") == "disable" else "enable",
                    "host": m.group("host"),
                    "interval": m.group("interval"),
                    "retry": m.group("retry"),
                }
            }
        }

    m = re.match(
        r"airset linkitg action ether (?P<port>\d) (?P<action>none|disable|enable)",
        conf,
    )
    if m:
        return {
            "airset": {
                "linkitg": {
                    "action": {
                        "ether": {m.group("port"): {"action": m.group("action")}}
                    }
                }
            }
        }

    m = re.match(
        r"airset linkitg action ssid num (?P<ssidnum>\d+) (?P<action>none|disable|enable)",
        conf,
    )
    if m:
        return {
            "airset": {
                "linkitg": {"action": {"ssid": {m.group("ssidnum"): m.group("action")}}}
            }
        }

    return None


def parse_ssid(conf: str) -> Optional[dict]:
    # logging.debug(f"parse_ssid:{conf}")

    global ssidname

    m = re.match(r"steering-policy (?P<steering_policy>\S+)", conf)
    if m:
        return {"airset": {"steering-policy": m.group("steering_policy")}}

    # airset ssid add ssidname "TOKAI-teacher" band 11g disable 11a enable vlanid 110 auth wpa2eap cipher aes rekey 60 mfp disable fast-trans disable
    m = re.match(r'add ssidname "(?P<ssidname>\S+)".*', conf)
    if m:
        ssidname = m.group("ssidname")
        return {}

    m = re.match(r"(?P<enable>enable|disable) ssidnum (?P<ssidnum>\d+)", conf)
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "ssidname": ssidname,
                        "enable": m.group("enable"),
                    }
                }
            }
        }

    m = re.match(
        r"wep ssidnum (?P<ssidnum>\d+) slot (?P<keyslot>\d+) (key (?P<keystring>\S+)|(?P<transmit>transmit))",
        conf,
    )
    if m:
        if m.group("keystring"):
            return {
                "airset": {
                    "ssid": {
                        m.group("ssidnum"): {"wep": {"keystring": m.group("keystring")}}
                    }
                }
            }
        if m.group("transmit"):
            return {"airset": {"wep": {"transmit": True}}}

    # airset ssid security ssidnum 1 auth wpa2psk cipher aes rekey 60 key "password!!" mfp optional fast-trans enable mdid 1111
    m = re.match(
        r"security ssidnum (?P<ssidnum>\d+) auth (?P<auth>\S+) cipher (?P<cipher>\S+)\s*(?P<options>.*)",
        conf,
    )
    if m:
        # logging.debug("airset ssid security")
        options = _parse_ssid_security_options(m.group("options"))
        ret = deepmerge(
            options,
            {
                "auth": m.group("auth"),
                "cipher": m.group("cipher"),
            },
        )

        return {"airset": {"ssid": {m.group("ssidnum"): ret}}}

    m = re.match(
        r"band ssidnum (?P<ssidnum>\d+) 11g (?P<enable_11g>\S+) 11a (?P<enable_11a>\S+)\s*(6g (?P<enable_6g>\S+))*",
        conf,
    )
    if m:
        # logging.debug("airset ssid band")
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "band": {
                            "11g": m.group("enable_11g"),
                            "11a": m.group("enable_11a"),
                            "6g": None
                            if m.group("enable_6g") == ""
                            else m.group("enable_6g"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"(?P<param>\S+) ssidnum (?P<ssidnum>\d+) (?P<value>\S+)$",
        conf,
    )
    if m:
        # logging.debug("airset <param> ssidnum <ssidnum> <value>")
        return {
            "airset": {
                "ssid": {m.group("ssidnum"): {m.group("param"): m.group("value")}}
            }
        }

    m = re.match(
        r"vlan ssidnum (?P<ssidnum>\d+) mode (?P<mode>\S+) vlanid (?P<vlanid>\d+)\s*(additional (?P<mvid1>\d+)\s*(?P<mvid2>\d+)*\s*(?P<mvid3>\d+)*)*",
        conf,
    )
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "vlan": {
                            "mode": m.group("mode"),
                            "vlanid": m.group("vlanid"),
                            "mvid1": m.group("mvid1"),
                            "mvid2": m.group("mvid2"),
                            "mvid3": m.group("mvid3"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"load-balancing ssidnum (?P<ssidnum>\d+) 11g (?P<lb11g>\d+) 11a (?P<lb11a>\d+)\s*(6g (?P<lb6g>\d+))*",
        conf,
    )
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "load-balancing": {
                            "11g": m.group("lb11g"),
                            "11a": m.group("lb11a"),
                            "6g": m.group("lb6g"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r'addsecurity ssidnum (?P<ssidnum>\d) mode (?P<mode>\S+)\s*(?P<radius_mode>authmac|authpass)*\s*("(?P<authpass>\S+)")*',
        conf,
    )
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "addsecurity": {
                            "mode": m.group("mode"),
                            "radius-mode": m.group("radius_mode"),
                            "authpass": m.group("authpass"),
                        }
                    }
                }
            }
        }

    m = re.match(
        r"radius ssidnum (?P<ssidnum>\d) server (?P<mode>\S+)( primary (?P<host1>\S+)\s(?P<secret1>\S+))*( secondary (?P<host2>\S+)\s(?P<secret2>\S+))*",
        conf,
    )
    if m:
        return {
            "airset": {
                "ssid": {
                    m.group("ssidnum"): {
                        "radius": {
                            "mode": m.group("mode"),
                            "primary": {
                                "host": m.group("host1"),
                                "secret": m.group("secret1"),
                            },
                            "secondary": {
                                "host": m.group("host2"),
                                "secret": m.group("secret2"),
                            },
                        }
                    }
                }
            }
        }

    return None


def _parse_ssid_security_options(options: str) -> dict:
    options = options.strip()
    if options == "":
        return {}

    m = re.match(
        r"fixed keytype (?P<keytype>\S+) transmit (?P<keyslot>\S+) key (?P<keystring>\S+)",
        options,
    )
    if m:
        return {
            "keytype": m.group("keytype"),
            "keyslot": m.group("keyslot"),
            "key": m.group("keystring"),
        }

    m = re.match(r"key (?P<length>\d+)", options)
    if m:
        return {"wep": {"length": m.group("length")}}

    m = re.match(
        r'rekey (?P<interval>\d+) key "(?P<password>\S+)" mfp (?P<mfp>\S+)\s*(?P<options2>.+)',
        options,
    )
    if m:
        options2 = m.group("options2")
        opt2_ret = _parse_security_options2(options2)
        return {
            "rekey": m.group("interval"),
            "key": m.group("password"),
            "mfp": m.group("mfp"),
            "fast-trans": opt2_ret["fast-trans"],
            "mdid": opt2_ret["mdid"],
        }

    m = re.match(r"rekey (?P<interval>\d+)", options)
    if m:
        return {"rekey": m.group("interval")}

    return {}


def _parse_security_options2(options: str) -> dict:
    # logging.debug(f"_parse_security_options2: {options}")
    m = re.match(
        r"fast-trans (?P<fast_trans>enable mdid (?P<mdid>\d+)|disable)", options
    )
    if m:
        return {
            "fast-trans": "disable" if m.group("fast_trans") == "disable" else "enable",
            "mdid": m.group("mdid"),
        }

    return {"fast-trans": None, "mdid": None}
