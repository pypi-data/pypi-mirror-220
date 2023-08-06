import logging
import time

import paramiko

RECV_SIZE = 1024 * 32


class BUFAPssh:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def get(self, command):
        logging.debug("BUFAPssh:get_ssh")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                self.hostname,
                22,
                self.username,
                self.password,
                timeout=10,
                look_for_keys=False,
            )
        except:
            raise ValueError("ssh connect failed")

        try:
            shell = ssh.invoke_shell(width=256)
            shell.send("")
            time.sleep(1)
            if shell.recv_ready():
                shell.recv(RECV_SIZE)

            shell.send(f"{command}\n")
            time.sleep(1)

            ret_data = []
            while True:
                if shell.recv_ready():
                    recv_data = shell.recv(RECV_SIZE)
                    row_data = [
                        row.strip()
                        for row in recv_data.decode("utf-8").splitlines()
                        if row.strip() != ""
                    ]

                    if len(row_data) == 0:
                        continue

                    if len(row_data) == 1 and (command in row_data[0]):
                        row_data = []
                        continue

                    if len(row_data) > 1 and (command in row_data[0]):
                        row_data = row_data[1:]

                    if "--More--" in row_data[-1]:
                        if len(row_data) > 1:
                            ret_data += row_data[:-1]
                        shell.send(" ")

                    elif "$" in row_data[-1]:
                        if len(row_data) > 1:
                            ret_data += row_data[:-1]
                        break

                    else:
                        ret_data += row_data

            ret_text = "\n".join(ret_data)

        finally:
            ssh.close()

        return ret_text
