"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

所有数据文件路径的统一集中定义。如需调整文件/目录位置，只改动此文件即可。
"""

# 数据根目录
DATA_DIR = "./data"

# 数据文件
SETTINGS_FILE = f"{DATA_DIR}/settings.json"
ANNOUNCEMENTS_FILE = f"{DATA_DIR}/announcements.json"
TAGS_FILE = f"{DATA_DIR}/tags.json"
LINKS_FILE = f"{DATA_DIR}/links.json"
SPONSORS_FILE = f"{DATA_DIR}/sponsors.json"
SPONSORS_CACHE_FILE = f"{DATA_DIR}/sponsors_cache.json"
META_BUILD_FILE = f"{DATA_DIR}/meta/build.json"
SUB_LINKS_FILE = f"{DATA_DIR}/sub/links.json"
SUB_THANKS_FILE = f"{DATA_DIR}/sub/thanks.json"

# 数据目录
CATEGORIES_DIR = f"{DATA_DIR}/categories/"

# 应用目录
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"


def category_file(category: str) -> str:
    """返回指定分类对应的 JSON 数据文件路径。"""
    return f"{CATEGORIES_DIR}{category}.json"
