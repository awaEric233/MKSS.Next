"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.

爱发电（Afdian）开放平台相关的 Pydantic 模型。
"""

from pydantic import BaseModel


class IfdianOrder(BaseModel):
    """爱发电订单。"""

    out_trade_no: str = ""
    user_id: str = ""
    plan_id: str = ""
    month: int = 0
    total_amount: str = ""
    show_amount: str = ""
    status: int = 0
    remark: str = ""
    redeem_id: str = ""
    product_type: int = 0
    discount: str = ""
    sku_detail: list[dict] = []
    address_person: str = ""
    address_phone: str = ""
    address_address: str = ""


class IfdianData(BaseModel):
    """爱发电 API 返回的数据（订单列表）。"""

    list: list[IfdianOrder]


class IfdianResponse(BaseModel):
    """爱发电 API 返回。"""

    ec: int = 0
    em: str = ""
    data: IfdianData


class IfdianWebhookData(BaseModel):
    """爱发电 Webhook 返回的数据（单个订单）。"""

    order: IfdianOrder


class IfdianWebhookResponse(BaseModel):
    """爱发电 Webhook 请求体。"""

    ec: int = 0
    em: str = ""
    data: IfdianWebhookData


class IfdianSponsorUser(BaseModel):
    """爱发电赞助者的用户信息。"""

    user_id: str = ""
    name: str = ""
    avatar: str = ""


class IfdianSponsor(BaseModel):
    """爱发电赞助者。"""

    sponsor_plans: list[dict] = []
    current_plan: dict = {}
    all_sum_amount: str = ""
    create_time: int = 0
    last_pay_time: int = 0
    user: IfdianSponsorUser = IfdianSponsorUser()


class IfdianSponsorData(BaseModel):
    """爱发电 API 返回的赞助者列表数据。"""

    total_count: int = 0
    total_page: int = 0
    list: list[IfdianSponsor]


class IfdianSponsorResponse(BaseModel):
    """爱发电 API 返回（赞助者列表）。"""

    ec: int = 0
    em: str = ""
    data: IfdianSponsorData
