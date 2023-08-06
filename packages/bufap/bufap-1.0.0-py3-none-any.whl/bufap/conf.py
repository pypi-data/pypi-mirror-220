from dictknife import deepmerge
import logging
from typing import Optional

from bufap import parser
from bufap import ssh


class BUFAPconf:
    conf_text: Optional[str] = None
    conf_table: list = []
    conf_dict: dict = {}
    PROMPT: str = ["\$.*"]

    def __init__(
        self,
        conf_file=None,
        hostname=None,
        username=None,
        password=None,
    ):
        if conf_file is not None:
            self.conf_text = self.get_config_file(conf_file)
        elif username is None or password is None or hostname is None:
            raise ValueError("username or password or hostname is null")
        else:
            self.get_config_ssh(
                hostname=hostname,
                username=username,
                password=password,
            )

    """設定ファイルを表形式に解析
    設定ファイルを表形式に解析する
    項目
      raw: 元の形式
      user: ユーザーが初期値から変更した部分
      default: 初期値

    解析ルール
    ・コメント行: raw=元の内容, user='', default=''
    ・空行: スキップする
    ・規定値のまま: raw=元の内容, user='', default="(default)"の右側
    ・規定値から変更: raw=元の内容, user=#の左側, default="(default)"の右側
    ・ユーザー設定のみ： raw=元の内容, user=元の内容, default=''
    """

    def parse_as_table(self, summarize=True):
        self.conf_table = []
        for line in self.conf_text.splitlines():
            raw_conf = line.strip()
            if raw_conf == "":
                continue
            elif raw_conf.startswith("#"):
                user_conf = default_conf = ""
            elif "#" in raw_conf:
                (user_conf, default_conf) = raw_conf.split("#")
                user_conf = user_conf.strip()
                default_conf = default_conf.replace("(default)", "").strip()
                if user_conf == default_conf and summarize:
                    user_conf = ""
            else:
                user_conf = raw_conf
                default_conf = ""

            self.conf_table.append(
                {"raw": raw_conf, "user": user_conf, "default": default_conf}
            )

        return self.conf_table

    def parse_as_dict(self, column="user"):
        self.conf_dict = {}

        for line in self.conf_table:
            conf = line[column].strip()
            if conf == "":
                continue
            conf_dict = parser.parse(conf)

            if conf_dict is None:
                logging.warning(f"parse not match: {conf}")
            else:
                self.conf_dict = deepmerge(self.conf_dict, conf_dict)

        return self.conf_dict

    def as_raw(self):
        return self.conf_text

    def as_text(self, column, summarize=True):
        return "\n".join(self.as_table(column, summarize))

    def as_table(self, column, summarize=True):
        self.parse_as_table(summarize)

        return [conf[column] for conf in self.conf_table if conf[column] != ""]

    def as_dict(self, column="user", summarize=True):
        self.parse_as_table(summarize)

        return self.parse_as_dict(column)

    def get_config_file(self, filename):
        with open(filename, "r") as f:
            self.conf_text = f.read()

        return self.conf_text

    def get_config_ssh(self, hostname, username, password):
        sshconn = ssh.BUFAPssh(hostname, username, password)
        self.conf_text = sshconn.get("show config all")

        return self.conf_text
