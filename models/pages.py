"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

页面聚合模型：主页由若干分类与公告组成。
"""

from .info import Announcement, Category


class MainPage:
    """主页，聚合所有分类与公告，供模板渲染。"""

    def __init__(self) -> None:
        self.categories: list[Category] = []
        self.announcements: list[Announcement] = []
