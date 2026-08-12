"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

JSON 读取与 XAML 转义工具。
"""

from json import loads
from typing import Any


def read_json_file(file_path: str) -> Any:
    """读取 UTF-8 编码的 JSON 文件并返回其内容。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return loads(f.read())


def xaml_safe(text: str) -> str:
    """将文本转义为可在 XAML 属性/文本中安全使用的字符串。"""
    return (
        text
        .replace("&", "&amp;")
        .replace("\n", "&#xA;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
