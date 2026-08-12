"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

统一响应结构：爱发电期望的成功响应与通用错误响应。
"""

# 爱发电期望的回调成功响应（ec 非 200 时平台认为回调失败）
IFDIAN_RESPONSE = {
    "ec": 200,
    "em": ""
}


def error_response(name: str, message: str) -> dict[str, str]:
    """构造统一的错误响应 JSON。"""
    return {
        "error": name,
        "message": message
    }
