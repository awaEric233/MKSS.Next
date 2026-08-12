"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

爱发电赞助者数据的获取与缓存：供致谢页展示赞助者昵称/头像。
同时维护赞助者名称与 UserId 的对应关系缓存。
"""

from time import time

from .files import write_json_file
from .ifdian import query_all_sponsors
from .parsing import read_json_file
from .paths import SPONSORS_CACHE_FILE, SPONSORS_FILE

# 赞助者列表缓存的有效期（秒），到期后才会重新请求爱发电 API
SPONSORS_CACHE_TTL = 600


def get_sponsors(ifdian_settings: dict | None = None) -> list:
    """
    获取用于致谢页展示的赞助者列表。

    若配置了爱发电 API 凭据（`ifdian.userId` / `ifdian.token`），则通过
    `query-sponsor` 接口分页拉取真实赞助者（含昵称/头像），结果缓存到
    `data/sponsors_cache.json`（默认 10 分钟过期，避免频繁请求爱发电接口）。
    未配置时回退到读取 `data/sponsors.json`（Webhook 记录的订单实例）。

    返回可直接用于模板渲染的 JSON 兼容列表（统一为 `{name, user_id, amount, avatar_url}` 结构）。
    """
    if isinstance(ifdian_settings, dict) and ifdian_settings.get("userId") and ifdian_settings.get("token"):
        sponsors = _cached_api_sponsors(ifdian_settings["userId"], ifdian_settings["token"])
    else:
        try:
            sponsors = read_json_file(SPONSORS_FILE)
        except Exception:
            sponsors = []
    mapping = get_sponsors_mapping()
    return [_normalize_sponsor(item, mapping) for item in sponsors if isinstance(item, dict)]


def _normalize_sponsor(item: dict, mapping: dict) -> dict:
    """
    将不同来源的赞助者记录统一为 `{name, user_id, amount, avatar_url}` 结构。

    - 爱发电 `query-sponsor` 返回的赞助者：昵称/ID/头像位于 `user` 下，金额为 `all_sum_amount`；
    - Webhook 记录的订单实例：金额为 `show_amount`，昵称可从名称↔UserId 映射补全。
    """
    user = item.get("user") if isinstance(item.get("user"), dict) else {}
    user_id = user.get("user_id") or item.get("user_id") or ""
    return {
        "name": user.get("name") or mapping.get(user_id, ""),
        "user_id": user_id,
        "amount": item.get("all_sum_amount") or item.get("show_amount") or "",
        "avatar_url": user.get("avatar") or "",
    }


def refresh_sponsors_cache(user_id: str, token: str) -> dict | None:
    """
    请求一次爱发电 API 获取当前全部赞助者，并缓存其名称↔UserId 映射。

    成功时写入 `data/sponsors_cache.json`（含赞助者列表与 `mapping` 字段）并返回缓存内容；
    失败时打印警告并返回 None（保留原有缓存）。
    """
    try:
        sponsors = [sponsor.model_dump(mode="json") for sponsor in query_all_sponsors(user_id, token)]
    except Exception as e:
        print(f"[W] Failed to fetch sponsors from ifdian API.\n  - {e}")
        return None
    cache = {
        "updated_at": round(time()),
        "sponsors": sponsors,
        "mapping": {
            sponsor["user"]["name"]: sponsor["user"]["user_id"]
            for sponsor in sponsors
            if isinstance(sponsor.get("user"), dict) and sponsor["user"].get("name")
        },
    }
    write_json_file(SPONSORS_CACHE_FILE, cache)
    return cache


def _cached_api_sponsors(user_id: str, token: str) -> list:
    """
    读取赞助者缓存；缓存过期/缺失时向爱发电重新查询并刷新缓存。

    查询失败时回退到过期缓存，尽力保证页面可用。
    """
    cache = _read_cache()
    if cache is not None and time() - cache.get("updated_at", 0) < SPONSORS_CACHE_TTL:
        return cache.get("sponsors", [])
    refreshed = refresh_sponsors_cache(user_id, token)
    if refreshed is not None:
        return refreshed.get("sponsors", [])
    return cache.get("sponsors", []) if cache else []


def get_sponsors_mapping() -> dict:
    """读取缓存的赞助者名称→UserId 映射；暂无缓存时返回空 dict。"""
    cache = _read_cache()
    if cache:
        mapping = cache.get("mapping")
        return mapping if isinstance(mapping, dict) else {}
    return {}


def _read_cache() -> dict | None:
    """读取赞助者缓存，文件不存在或内容损坏时返回 None。"""
    try:
        cache = read_json_file(SPONSORS_CACHE_FILE)
        return cache if isinstance(cache, dict) else None
    except Exception:
        return None
