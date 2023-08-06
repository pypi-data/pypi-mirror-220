from enum import Enum
import ipaddress
import logging
import os

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from bufap import BUAPconf

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class DispMode(Enum):
    ALL = 1
    USER_ONLY = 2


COLUMNS = {
    DispMode.ALL: [
        {"column": "user", "heading": "ユーザー設定"},
        {"column": "default", "heading": "初期値"},
    ],
    DispMode.USER_ONLY: [
        {"column": "user", "heading": "ユーザー設定"},
    ],
}


class Application(tk.Frame):
    hostname = "192.168.1.1"
    username = "admin"
    password = "password"
    tree = None
    v_scrollbar = None
    dispMode = DispMode.ALL
    conf = None
    curr_dir = "./"

    def __init__(self, master=None):
        logging.debug("__init__")

        super().__init__(master)

        self.master.geometry("800x400")
        self.master.title("BUFFALO AP configツール")

        self.nb = ttk.Notebook(self.master)

        self.tab_cli = tk.Frame(self.nb)
        self.tab_conf_wifi = tk.Frame(self.nb)
        self.tab_conf_ssid = tk.Frame(self.nb)
        self.tab_conf_radius = tk.Frame(self.nb)
        self.tab_conf_mac = tk.Frame(self.nb)
        self.tab_conf_admin = tk.Frame(self.nb)

        self.nb.add(self.tab_cli, text="CLI")
        self.nb.add(self.tab_conf_wifi, text="Wi-Fi設定")
        self.nb.add(self.tab_conf_ssid, text="SSID設定")
        self.nb.add(self.tab_conf_radius, text="RADIUS設定")
        self.nb.add(self.tab_conf_mac, text="MACアクセス制限設定")
        self.nb.add(self.tab_conf_admin, text="管理設定")

        self.nb.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_tab_cli()
        self.create_tab_conf_wifi()
        self.create_tab_conf_ssid()
        self.create_tab_radius()
        self.create_tab_mac()
        self.create_tab_admin()

    def button_get_config_click(self):
        logging.debug("button_get_config_click")

        try:
            self.hostname = str(ipaddress.ip_address(self.entry_hostname.get()))
            self.username = self.entry_username.get()
            self.password = self.entry_password.get()
        except:
            return

        logging.debug(
            f"hostname: {self.hostname}, username : {self.username}, password : {self.password}"
        )
        self.conf = BUAPconf(
            hostname=self.hostname, username=self.username, password=self.password
        )
        self.update_tree()

    def menu_file_open_click(self, event=None):
        logging.debug("menu_file_open_click")

        filename = filedialog.askopenfilename(title="ファイルを開く", initialdir=self.curr_dir)

        try:
            with open(filename, mode="r") as f:
                contents = f.read()
                self.conf = BUAPconf(contents)
            self.curr_dir = os.path.dirname(filename)

        except FileNotFoundError:
            return False

        self.update_tree()

    def menu_file_saveas_click(self, event=None):
        logging.debug("menu_file_saveas_click")

        filename = filedialog.asksaveasfilename(
            title="名前を付けて保存", initialdir=self.curr_dir
        )
        contents = self.conf.get_conf_as_text("user")
        try:
            with open(filename, mode="w") as f:
                f.write(contents)
            self.curr_dir = os.path.dirname(filename)

        except IOError:
            return False

    def menu_file_clear_click(self, event=None):
        logging.debug("menu_file_clear_click")

        self.delete_tree()

    def menu_disp_useronly_click(self):
        logging.debug("menu_disp_useronly_click")

        if self.dispMode == DispMode.ALL:
            self.dispMode = DispMode.USER_ONLY
        else:
            self.dispMode = DispMode.ALL

        self.update_tree()

    def create_tab_cli(self):
        logging.debug("create tab_cli")

        self.u_frame = tk.Frame(self.tab_cli)
        self.b_frame = tk.Frame(self.tab_cli)
        self.u_frame.pack(fill=tk.X)
        self.b_frame.pack(fill=tk.BOTH, expand=True)

        lbl_hostname = tk.Label(self.u_frame, text="IPアドレス")
        self.entry_hostname = tk.Entry(
            self.u_frame, width=15, textvariable=self.hostname
        )
        self.entry_hostname.insert(0, self.hostname)

        lbl_username = tk.Label(self.u_frame, text="ユーザー名")
        self.entry_username = tk.Entry(
            self.u_frame, width=15, textvariable=self.username
        )
        self.entry_username.insert(0, self.username)

        lbl_password = tk.Label(self.u_frame, text="パスワード")
        self.entry_password = tk.Entry(
            self.u_frame, width=15, textvariable=self.password
        )
        self.entry_password.insert(0, self.password)

        b = tk.Button(self.u_frame, text="設定取得", command=self.button_get_config_click)
        lbl_hostname.pack(side=tk.LEFT)
        self.entry_hostname.pack(side=tk.LEFT, padx=5)
        lbl_username.pack(side=tk.LEFT)
        self.entry_username.pack(side=tk.LEFT, padx=5)
        lbl_password.pack(side=tk.LEFT)
        self.entry_password.pack(side=tk.LEFT, padx=5)
        b.pack(side=tk.LEFT, pady=5)

        menubar = tk.Menu(self)

        menu_file = tk.Menu(menubar, tearoff=False)
        menu_file.add_command(
            label="開く", command=self.menu_file_open_click, accelerator="Ctrl+O"
        )
        menu_file.add_command(
            label="ユーザー設定のみ保存",
            command=self.menu_file_saveas_click,
            accelerator="Ctrl+S",
        )
        menu_file.add_command(label="消去", command=self.menu_file_clear_click)
        menu_file.add_separator()  # 仕切り線
        menu_file.add_command(label="終了", command=self.master.destroy)

        # ショートカットキーの関連付け
        menu_file.bind_all("<Control-o>", self.menu_file_open_click)
        menu_file.bind_all("<Control-s>", self.menu_file_saveas_click)

        menu_disp = tk.Menu(menubar, tearoff=False)
        self.disp1_value = tk.BooleanVar()
        menu_disp.add_checkbutton(
            label="ユーザー設定のみ",
            command=self.menu_disp_useronly_click,
            variable=self.disp1_value,
        )

        # メニューバーに各メニューを追加
        menubar.add_cascade(label="ファイル", menu=menu_file)
        menubar.add_cascade(label="表示", menu=menu_disp)

        # 親ウィンドウのメニューに、作成したメニューバーを設定
        self.master.config(menu=menubar)
        self.create_tree()

    def create_tree(self):
        logging.debug("create_tree")

        columns = self.get_columns()
        logging.debug(f"columns: {columns}")
        self.tree = ttk.Treeview(self.b_frame, columns=columns)
        self.tree.column("#0", width=0, stretch="no")
        for col in COLUMNS[self.dispMode]:
            self.tree.column(col["column"], width=80)
            self.tree.heading(column=col["column"], text=col["heading"])
        self.v_scrollbar = tk.Scrollbar(
            self.b_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=self.v_scrollbar.set)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_tree(self):
        logging.debug("update_tree")

        self.delete_tree()

        if self.conf is None:
            return True

        for row in self.conf.conf_table:
            values = []
            pass_flg = True
            for col in COLUMNS[self.dispMode]:
                values.append(row[col["column"]])
                if row[col["column"]] != "":
                    pass_flg = False
            # すべてのカラムが空白ならスキップする
            if pass_flg:
                continue

            self.tree.insert("", "end", values=values)

    def delete_tree(self):
        logging.debug("delete_tree")

        self.v_scrollbar.destroy()
        self.tree.destroy()

        self.create_tree()

    def get_columns(self):
        return [col["column"] for col in COLUMNS[self.dispMode]]

    def create_tab_conf_wifi(self):
        logging.debug("create_tab_conf_wifi")

    def create_tab_conf_ssid(self):
        logging.debug("create_tab_conf_ssid")

    def create_tab_radius(self):
        logging.debug("create_tab_radius")

    def create_tab_mac(self):
        logging.debug("create_tab_conf_mac")

    def create_tab_admin(self):
        logging.debug("create_tab_conf_admin")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
