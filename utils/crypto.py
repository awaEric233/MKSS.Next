"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

哈希工具：SHA-1 与 MD5。
"""

from hashlib import md5 as _md5
from hashlib import sha1 as _sha1


def sha1_file(file_path: str) -> str:
    """计算单个文件的 SHA-1 十六进制摘要。"""
    with open(file_path, "rb") as f:
        return _sha1(f.read()).hexdigest()


def sha1_files(file_paths: list[str]) -> str:
    """将多个文件的字节依次喂入同一个 SHA-1，计算合并摘要。"""
    hash = _sha1()
    for file_path in file_paths:
        with open(file_path, "rb") as f:
            hash.update(f.read())
    return hash.hexdigest()


def md5(string: str) -> str:
    """计算字符串的 MD5 十六进制摘要（UTF-8 编码）。"""
    return _md5(string.encode("utf-8")).hexdigest()
