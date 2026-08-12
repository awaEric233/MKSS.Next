"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

文件与目录初始化工具。
"""

from json import dump
from os import makedirs
from os.path import exists
from typing import Any


def write_json_file(file_path: str, content: Any) -> None:
    """以 UTF-8 编码、缩进 4 个空格的方式将内容写入 JSON 文件。"""
    with open(file_path, "w", encoding="utf-8") as f:
        dump(content, f, ensure_ascii=False, indent=4)


def create_json_file_if_not_exists(file_path: str, content: Any) -> None:
    """若文件不存在，则创建并写入默认内容。"""
    if not exists(file_path):
        write_json_file(file_path, content)


def create_dir_if_not_exists(dir_path: str) -> None:
    """若目录不存在，则递归创建。"""
    if not exists(dir_path):
        makedirs(dir_path)
