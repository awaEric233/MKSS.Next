"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

页面构建工具：将数据文件渲染为 PCL2 可识别的主页 XAML。
"""

from os import listdir
from os.path import abspath

from fastapi import Request
from pydantic import TypeAdapter
from starlette.responses import Response
from starlette.templating import Jinja2Templates

from models import Announcement, Category, Link, MainPage

from .parsing import read_json_file, xaml_safe
from .paths import ANNOUNCEMENTS_FILE, CATEGORIES_DIR, LINKS_FILE, TAGS_FILE, TEMPLATES_DIR

# 模板引擎（进程内复用同一个实例）
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)


def render_template(template_name: str, request: Request, **kwargs) -> Response:
    """渲染指定模板并返回 HTTP 响应。"""
    return TEMPLATES.TemplateResponse(request, template_name, {"request": request, **kwargs})


def build_page(request: Request, settings: dict) -> Response:
    """读取所有分类与公告，构建主页 XAML。"""
    base = abspath(CATEGORIES_DIR)
    paths = readable_source_files(listdir(base))
    page = MainPage()
    tags = read_tags_file()
    for item in paths:
        info = read_source_file(f"{base}/{item}")
        for source in info.sources:
            # 将源中的文本转义为 XAML 安全字符串，防止破坏页面结构
            source.title = xaml_safe(source.title)
            tag = ""
            if source.author in tags:
                # 贡献者标签渲染为 "<标签> " 前缀
                tag = "".join(f"<{tag_name}> " for tag_name in tags[source.author])
            source.author = xaml_safe(f"贡献者：{tag}{source.author}")
            source.content = xaml_safe(source.content)
        page.categories.append(info)
    page.announcements = read_announcement_file()
    return render_template("index.xaml", request, page=page, settings=settings)


def readable_source_files(files: list[str]) -> list[str]:
    """过滤出可读取的源文件：忽略以点开头的隐藏文件与非 JSON 文件。"""
    return [item for item in files if not item.startswith(".") and item.endswith(".json")]


def read_source_file(file_path: str) -> Category:
    """读取并解析一个分类 JSON 文件为 `Category` 模型。"""
    return Category.model_validate(read_json_file(file_path))


def read_tags_file() -> dict[str, list[str]]:
    """读取贡献者标签文件。"""
    return read_json_file(TAGS_FILE)


def read_announcement_file() -> list[Announcement]:
    """读取公告文件，并将公告字段转义为 XAML 安全字符串。"""
    adapter = TypeAdapter(list[Announcement])
    announcements = adapter.validate_python(read_json_file(ANNOUNCEMENTS_FILE))
    for item in announcements:
        item.title = xaml_safe(item.title)
        item.info = xaml_safe(item.info)
        item.content = xaml_safe(item.content)
    return announcements


def read_links_file() -> dict[str, list[Link]]:
    """读取链接文件，并将链接字段转义为 XAML 安全字符串。"""
    adapter = TypeAdapter(dict[str, list[Link]])
    links = adapter.validate_python(read_json_file(LINKS_FILE))
    for group in links.values():
        for item in group:
            item.title = xaml_safe(item.title)
            item.info = xaml_safe(item.info)
            item.link = xaml_safe(item.link)
    return links
