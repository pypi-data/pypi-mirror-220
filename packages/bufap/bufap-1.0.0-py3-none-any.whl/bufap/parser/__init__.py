from typing import Optional

from dictknife import deepmerge

from . import airset
from . import bridge
from . import ether
from . import ip
from . import radius
from . import setup


def parse(conf: str) -> Optional[dict]:
    conf_dict = None

    if conf.startswith("airset"):
        conf_dict = airset.parse(conf)
    elif conf.startswith("bridge"):
        conf_dict = bridge.parse(conf)
    elif conf.startswith("ether"):
        conf_dict = ether.parse(conf)
    elif conf.startswith("ip"):
        conf_dict = ip.parse(conf)
    elif conf.startswith("radius"):
        conf_dict = radius.parse(conf)
    elif conf.startswith("setup"):
        conf_dict = setup.parse(conf)

    return conf_dict
