import json
import argparse
from pyxk.m3u8 import M3U8


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "uri", help="m3u8链接")
    parser.add_argument(
        "-f", "--file", help="媒体文件名称")
    parser.add_argument(
        "-r", "--rerequest", help="重新请求m3u8(default: False)", action="store_true")
    parser.add_argument(
        "--delete", help="删除m3u8文本文件(default: False)", action="store_true")
    parser.add_argument(
        "--reserve", help="保留segments文件(default: False)", action="store_true")
    parser.add_argument(
        "-l", "--limit", help="异步并发连接数(default: 8)", default=8, type=int)
    parser.add_argument(
        "-p", "--probe", help="测试m3u8链接(default: False)", action="store_true")
    parser.add_argument(
        "--parameter", help="requests 请求参数(type: dict)", default='{}', type=json.loads)
    args = parser.parse_args()

    m3u8_downloader = M3U8()
    m3u8_downloader.limit = args.limit

    if args.probe:
        args.rerequest = True

    m3u8_downloader.load_m3u8_uri(
        uri=args.uri,
        video=args.file,
        probe=args.probe,
        rerequest=args.rerequest,
        delete_m3u8file=args.delete,
        reserve_segments=args.reserve,
        **args.parameter
    )
