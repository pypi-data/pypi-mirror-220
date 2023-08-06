import csv
import io
import logging
import re

from bufap.ssh import BUFAPssh
from bufap import common


class BUFAPtool:
    ssh = None

    def __init__(self, hostname, username, password):
        self.ssh = BUFAPssh(hostname, username, password)

    def get(self, command) -> str:
        return self.ssh.get(command)

    def get_wireless_monitor(self, format="csv") -> list:
        ret = self.get("airset wireless-monitor scan")
        common.print_waiting("scanning", 60)
        ret = self.get("airset wireless-monitor show status")

        if format in ["dict"]:
            return self.parse_wireless_monitor(ret)
        if format in ["csv"]:
            fields = [
                "Index",
                "MAC",
                "Vendor",
                "SSID",
                "Channel",
                "Mode",
                "RSSI",
                "Noise",
                "Security",
            ]
            ret_csv = io.StringIO()
            writer = csv.DictWriter(ret_csv, fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.parse_wireless_monitor(ret))
            return ret_csv.getvalue()

        return ret

    def parse_wireless_monitor(self, output: str) -> list:
        ret = []
        start_flg = False
        for line in output.splitlines():
            if line.startswith("--------------------------------------"):
                start_flg = True
                continue
            if not start_flg:
                continue
            try:
                (index, mac, ssid, channel, mode, rssi, noise, security) = line.split()
                vendor = common.mac2vendor(mac)
                ret.append(
                    {
                        "Index": index,
                        "MAC": mac,
                        "Vendor": vendor,
                        "SSID": ssid,
                        "Channel": channel,
                        "Mode": mode,
                        "RSSI": rssi,
                        "Noise": noise,
                        "Security": security,
                    }
                )
            except Exception as e:
                logging.warning(f"{e}")
                logging.warning(f"{line}")

        return ret

    def get_client_monitor(self, format="csv") -> list:
        ret = self.get("airset client-monitor show status")

        if format in ["raw", "text"]:
            return ret

        if format in ["dict"]:
            return self.parse_client_monitor(ret)

        if format in ["csv"]:
            fields = [
                "band",
                "SSID",
                "MAC",
                "Vendor",
                "Tx",
                "Rx",
                "RSSI",
                "connect",
                "idle",
            ]
            ret_csv = io.StringIO()
            writer = csv.DictWriter(ret_csv, fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(self.parse_client_monitor(ret))

        return ret_csv.getvalue()

    def parse_client_monitor(self, output: str) -> list:
        ret = []
        start_flg = False
        band = ""
        for line in output.splitlines():
            m = re.match(r"\[\s*(?P<band>\S+)\s*\]", line)
            if m:
                start_flg = True
                band = m.group("band")
                continue

            if not start_flg:
                continue

            if line.startswith("SSID") or line.startswith("----------"):
                continue

            try:
                (ssid, mac, tx, rx, rssi, connect, idle) = line.split()
                vendor = common.mac2vendor(mac)
                ret.append(
                    {
                        "band": band,
                        "SSID": ssid,
                        "MAC": mac,
                        "Vendor": vendor,
                        "Tx": common.convert_to_byte(tx),
                        "Rx": common.convert_to_byte(rx),
                        "RSSI": rssi,
                        "connect": connect,
                        "idle": idle,
                    }
                )
            except Exception as e:
                logging.warning(f"{e}")
                logging.warning(f"{line}")

        return ret

    def exec(self, command):
        ret = self.get(command)

        return ret
