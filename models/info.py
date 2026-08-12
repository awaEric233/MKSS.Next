"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

信息模型：分类、源、公告与链接的 Pydantic 定义。
"""

from pydantic import BaseModel, Field


class Source(BaseModel):
    """分类中的一条源（投稿内容）。"""

    title: str = ""
    author: str = ""
    content: str = ""


class Category(BaseModel):
    """一个分类，包含名称、图标与若干源。"""

    name: str = ""
    logo: str = ""
    sources: list[Source] = []


class Announcement(BaseModel):
    """一条公告。"""

    title: str = ""
    info: str = ""
    is_link: bool = Field(alias="isLink", default=False)
    content: str = ""


class Link(BaseModel):
    """链接页中的一条链接。"""

    title: str = ""
    info: str = ""
    link: str = ""
