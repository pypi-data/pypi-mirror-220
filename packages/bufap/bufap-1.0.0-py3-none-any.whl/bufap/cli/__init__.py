#!/usr/bin/env python3

import argparse
import logging
import pprint
import sys

import bufap


def main() -> None:
    output: str = ""

    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    parser = argparse.ArgumentParser(
        description="WAPMシリーズコンフィグツール",  # 引数のヘルプの前に表示
        add_help=True,  # -h/–help オプションの追加
        formatter_class=argparse.RawTextHelpFormatter,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--get-conf",
        help="設定を取得",
        action="store_const",
        const="get-conf",
        dest="action",
    )
    group.add_argument(
        "--read-conf",
        help="設定を読み込み",
        action="store_const",
        const="read-conf",
        dest="action",
    )
    group.add_argument(
        "--wireless-monitor",
        help="無線環境モニター",
        action="store_const",
        const="wireless-monitor",
        dest="action",
    )
    group.add_argument(
        "--client-monitor",
        help="クライアントモニター",
        action="store_const",
        const="client-monitor",
        dest="action",
    )
    group.add_argument(
        "--exec",
        help="コマンド実行の結果を取得",
        action="store_const",
        const="exec",
        dest="action",
    )

    parser.add_argument("--host", help="ホストアドレス(IP)")
    parser.add_argument("--username", default="admin", help="ユーザー名")
    parser.add_argument("--password", default="password", help="パスワード")

    parser.add_argument("--infile", help="設定ファイルのパス")
    parser.add_argument("--outfile", help="出力先ファイルのパス")

    parser.add_argument(
        "--summarize",
        help="ユーザーが変更した部分のみ表示するかどうか",
        choices=["yes", "no"],
        default="yes",
    )

    parser.add_argument(
        "--column", choices=["user", "default"], default="user", help="出力するカラムを指定"
    )

    parser.add_argument(
        "--format",
        choices=["raw", "text", "dict", "csv"],
        default="text",
        help="""設定ファイルの場合：raw(APの設定値そのまま),text(必要な情報に絞った表示),dict(辞書形式)
クライアントモニタ、無線環境モニタの場合：raw(APの出力そのまま。csv(CSV形式)
""",
    )

    parser.add_argument(
        "--command",
        help="exec コマンド指定時のコマンドを実行する",
    )

    args = parser.parse_args()

    summarize = True if args.summarize == "yes" else False

    logging.debug(args)
    if args.action == "get-conf":
        conf = bufap.BUFAPconf(
            hostname=args.host,
            username=args.username,
            password=args.password,
        )
    elif args.action == "read-conf":
        conf = bufap.BUFAPconf(conf_file=args.infile)
    elif args.action == "wireless-monitor":
        tool = bufap.BUFAPtool(args.host, args.username, args.password)
        output = tool.get_wireless_monitor(args.format)
    elif args.action == "client-monitor":
        tool = bufap.BUFAPtool(args.host, args.username, args.password)
        output = tool.get_client_monitor(args.format)
    elif args.action == "exec":
        if args.command:
            tool = bufap.BUFAPtool(args.host, args.username, args.password)
            output = tool.exec(args.command)

    if args.action in ["get-conf", "read-conf"]:
        if args.format == "raw":
            output = conf.as_raw()
        elif args.format == "text":
            conf.parse_as_table(summarize)
            output = conf.as_text(args.column, summarize)
        elif args.format == "dict":
            conf.as_dict(args.column, summarize)
            output = pprint.pformat(conf.conf_dict)

    if args.outfile:
        with open(args.outfile, "w") as f:
            f.write(output)
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
