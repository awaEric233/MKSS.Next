"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

爱发电（Afdian）开放平台相关工具：API 签名、订单查询、Webhook 签名校验。
"""

import hmac
from json import dumps
from time import time

from requests import get

from models import IfdianOrder, IfdianResponse, IfdianSponsor, IfdianSponsorResponse

from .crypto import md5

IFDIAN_BASE_URL = "https://ifdian.net/api/open/"


def _params_to_json(params: dict) -> str:
    """
    将请求参数序列化为签名与请求均使用的最小化 JSON 字符串。

    爱发电官方约定 params 的 JSON 为紧凑格式（无多余空格），
    例如 `{"a":333}`，因此需要指定 `separators=(",", ":")`。
    """
    return dumps(params, ensure_ascii=False, separators=(",", ":"))


def ifdian_sign(user_id: str, token: str, params: dict, ts: int) -> str:
    """
    计算爱发电 API 请求签名。

    规则：`md5(token + params{params} + ts{ts} + user_id{user_id})`
    """
    pattern = f"{token}params{_params_to_json(params)}ts{ts}user_id{user_id}"
    return md5(pattern)


def query_order(user_id: str, token: str, page: int = 1) -> list[IfdianOrder]:
    """
    按页查询爱发电的历史订单（按创建时间倒序）。

    `page`：页码，从 1 开始。
    """
    params = {"page": page}
    params_json = _params_to_json(params)
    ts = round(time())
    sign = ifdian_sign(user_id, token, params, ts)
    response = get(
        f"{IFDIAN_BASE_URL}query-order",
        params={
            "user_id": user_id,
            "params": params_json,
            "ts": ts,
            "sign": sign,
        },
        timeout=10,
    )
    return IfdianResponse.model_validate_json(response.text).data.list


def query_sponsor(user_id: str, token: str, page: int = 1, per_page: int = 100) -> IfdianSponsorResponse:
    """
    按页查询爱发电的赞助者列表（按建立关系时间倒序）。

    `page`：页码，从 1 开始；`per_page`：每页数量，爱发电默认 20、支持 1-100。
    """
    params = {"page": page, "per_page": per_page}
    params_json = _params_to_json(params)
    ts = round(time())
    sign = ifdian_sign(user_id, token, params, ts)
    response = get(
        f"{IFDIAN_BASE_URL}query-sponsor",
        params={
            "user_id": user_id,
            "params": params_json,
            "ts": ts,
            "sign": sign,
        },
        timeout=10,
    )
    return IfdianSponsorResponse.model_validate_json(response.text)


def query_all_sponsors(user_id: str, token: str) -> list[IfdianSponsor]:
    """
    分页拉取爱发电的全部赞助者（按建立关系时间倒序）。

    自动翻页直到取完 `total_page` 的所有页。
    """
    sponsors: list[IfdianSponsor] = []
    page = 1
    while True:
        data = query_sponsor(user_id, token, page=page).data
        sponsors.extend(data.list)
        if page >= data.total_page or not data.list:
            break
        page += 1
    return sponsors


def verify_webhook_signature(user_id: str, token: str, ts: str, signature: str) -> bool:
    """
    校验爱发电 Webhook 签名。

    签名规则：`md5(user_id + ts + token)`，
    其中 user_id/token 为自己的开发者凭据，ts 取自请求头 `X-Ifdian-Ts`，
    传入的 signature 取自请求头 `X-Ifdian-Signature`。

    使用常量时间比较，防止时序攻击。
    """
    if not signature:
        return False
    expected = md5(f"{user_id}{ts}{token}")
    return hmac.compare_digest(expected, signature.lower())
