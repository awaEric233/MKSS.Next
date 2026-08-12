"""
Plain Craft Launcher 2 - Minecraft 芝士站主页 ( Minecraft Knowledge Sharing Site Homepage, MKSS )
(C) 2026 awa_Eric233. Under the MIT License.
"""

from contextlib import asynccontextmanager
from os import listdir
from os.path import abspath
from typing import Annotated, Any

from fastapi import FastAPI, Header, Request, Response, status
from starlette.staticfiles import StaticFiles

from models import IfdianWebhookResponse
from utils import (
    IFDIAN_RESPONSE,
    ANNOUNCEMENTS_FILE,
    CATEGORIES_DIR,
    LINKS_FILE,
    META_BUILD_FILE,
    SETTINGS_FILE,
    SPONSORS_FILE,
    STATIC_DIR,
    SUB_LINKS_FILE,
    SUB_THANKS_FILE,
    TAGS_FILE,
    build_page,
    category_file,
    create_dir_if_not_exists,
    create_json_file_if_not_exists,
    error_response,
    get_sponsors,
    read_json_file,
    read_links_file,
    readable_source_files,
    refresh_sponsors_cache,
    render_template,
    sha1_files,
    verify_webhook_signature,
    write_json_file,
)

# 爱发电赞助页地址前缀，`[mylink]` 为 settings.json 中可自定义的部分
IFDIAN_LINK_BASE = "https://ifdian.net/a/"

#region: 初始化（确保数据目录与默认数据文件存在）
create_json_file_if_not_exists(SETTINGS_FILE, {
    "info": {
        "baseUrl": "http://127.0.0.1:8080",
        "postUrl": "http://127.0.0.1:8080/post"
    },
    "ifdian": {
        "link": "transae"
    }
})
create_dir_if_not_exists(CATEGORIES_DIR)
create_json_file_if_not_exists(ANNOUNCEMENTS_FILE, [{
    "title": "欢迎使用 MKSS.Next！",
    "info": "如果你看到这条公告，那么你的部署应该已经成功了！",
    "isLink": False,
    "content": "恭喜！你已成功部署了 MKSS.Next！"
}])
create_json_file_if_not_exists(TAGS_FILE, {})
create_json_file_if_not_exists(LINKS_FILE, {})
#endregion

#region: 配置（加载站点设置与构建信息）
try:
    settings = read_json_file(SETTINGS_FILE)
    meta = read_json_file(META_BUILD_FILE)
except Exception as e:
    print(f"[X] Failed to load settings file, please check your configuration.\n  - {e}")
    exit(1)
#endregion

#region: 实例
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    服务器启动时向爱发电请求一次当前赞助者，
    并缓存赞助者名称与 UserId 的对应关系（未配置 API 凭据时跳过）。
    """
    ifdian_settings = settings.get("ifdian")
    if isinstance(ifdian_settings, dict) and ifdian_settings.get("userId") and ifdian_settings.get("token"):
        print("[I] Fetching sponsors from ifdian API on startup...")
        refresh_sponsors_cache(ifdian_settings["userId"], ifdian_settings["token"])
    else:
        print("[I] Ifdian API credentials not configured, skipping startup sponsor refresh.")
    yield

app = FastAPI(title="MKSS.Next", version=meta["version"], lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
#endregion

#region: 路由
@app.get("/", name="主页", status_code=status.HTTP_200_OK)
async def route_index(request: Request, user_agent: Annotated[str | None, Header()] = None):
    """
    **获取主页。**

    - **在 PCL2 中**（UA 以 `PCL2/` 开头）：此接口会渲染并返回主页 XAML；
    - **否则**：此接口会返回元数据。
    """

    # 判断 UA，是否为 PCL2（注意 UA 可能缺失，需要判空）
    if user_agent and user_agent.startswith("PCL2/"):
        return build_page(request, settings)
    else:
        return meta

@app.get("/version", name="版本", status_code=status.HTTP_200_OK)
async def route_version() -> dict[str, str]:
    """
    **获取版本信息。**
    
    这将返回 JSON，包含如下内容：
    - `categories`：所有分区的 SHA1 值；
    - `extend`：其他文件（公告、标签）的 SHA1 值。
    """

    base = abspath(CATEGORIES_DIR)
    files = [f"{base}/{x}" for x in readable_source_files(listdir(base))]
    return {
        "categories": sha1_files(files),
        "extend": sha1_files([ANNOUNCEMENTS_FILE, TAGS_FILE])
    }

@app.get("/categories", name="分区", status_code=status.HTTP_200_OK)
async def route_categories() -> list[str]:
    """
    **获取所有分区。**
    
    这将返回 JSON，包含所有分区的名称。
    """

    base = abspath(CATEGORIES_DIR)
    files = readable_source_files(listdir(base))
    return [x.replace(".json", "") for x in files]

@app.get("/categories/{category}", name="特定分区信息", status_code=status.HTTP_200_OK)
async def route_category(category: str, response: Response) -> dict:
    """
    **获取指定分区。**

    这将返回 JSON，包含如下内容：
    - `name`：分区名称；
    - `logo`：分区图标，适配 PCL2；
    - `sources`：分区内的源（投稿内容）。

    源又包含如下内容：
    - `title`：源标题；
    - `author`：源贡献者（不带标签）；
    - `content`：源内容（\\n 换行）。
    """

    base = abspath(CATEGORIES_DIR)
    files = readable_source_files(listdir(base))
    final = [x.replace(".json", "") for x in files]
    if category not in final:
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_response("file_not_found", "No such file. Check your spelling.")
    try:
        return read_json_file(category_file(category))
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to read file: {category_file(category)}, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")

@app.get("/announcements", name="公告", status_code=status.HTTP_200_OK)
async def route_announcements(response: Response) -> list[dict]:
    """
    **获取公告。**
    
    这将返回 JSON，包含如下内容：
    - `title`：公告标题；
    - `info`：公告信息；
    - `isLink`：是否为链接；
    - `content`：公告内容（\\n 换行）（或链接 URL）。
    """

    try:
        return read_json_file(ANNOUNCEMENTS_FILE)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to read file: {ANNOUNCEMENTS_FILE}, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")

@app.get("/tags", name="标签", status_code=status.HTTP_200_OK)
async def route_tags(response: Response) -> dict:
    """
    **获取标签。**
    
    这将返回 JSON，键为贡献者名称，值为标签列表。
    """

    try:
        return read_json_file(TAGS_FILE)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to read file: {TAGS_FILE}, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")

@app.get("/sub/links.json", name="链接页帮助配置文件", status_code=status.HTTP_200_OK)
async def route_sub_links_json(response: Response) -> dict:
    """
    **链接页的帮助配置文件。**
    
    适配 PCL2，无额外用途。
    """
    
    try:
        return read_json_file(SUB_LINKS_FILE)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to read file: {SUB_LINKS_FILE}, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")

@app.get("/sub/links.xaml", name="链接页 XAML", status_code=status.HTTP_200_OK)
async def route_sub_links_xaml(request: Request, response: Response):
    """
    **链接页 XAML。**

    适配 PCL2，无额外用途。
    """
    
    try:
        links = read_links_file()
        return render_template("links.xaml", request, links=links)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to build links page, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")
    
@app.get("/sub/thanks.json", name="致谢页帮助配置文件", status_code=status.HTTP_200_OK)
async def route_sub_thanks_json(response: Response) -> dict:
    """
    **致谢页的帮助配置文件。**
    
    适配 PCL2，无额外用途。
    """
    
    try:
        return read_json_file(SUB_THANKS_FILE)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to read file: {SUB_THANKS_FILE}, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")
    
@app.get("/sub/thanks.xaml", name="致谢页 XAML", status_code=status.HTTP_200_OK)
async def route_sub_thanks_xaml(request: Request, response: Response):
    """
    **致谢页 XAML。**
    
    适配 PCL2，无额外用途。
    """
    
    try:
        # 从 settings.json 读取自定义的爱发电赞助页地址（默认 transae）
        ifdian_cfg = settings.get("ifdian") if isinstance(settings.get("ifdian"), dict) else {}
        sponsor_url = f"{IFDIAN_LINK_BASE}{ifdian_cfg.get('link') or 'transae'}"
        # 获取赞助者列表（配置了爱发电 API 则查询真实赞助者昵称，否则回退到 Webhook 记录）
        sponsors = get_sponsors(ifdian_cfg)
        return render_template("thanks.xaml", request, sponsor_url=sponsor_url, sponsors=sponsors)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        print(f"[X] Failed to build thanks page, check the file.\n  - {e}")
        return error_response("failed_to_read_file", "Failed to read this file. Contact the admin.")
    
@app.post("/ifdian", name="爱发电 Webhook", status_code=status.HTTP_201_CREATED)
async def route_ifdian_webhook(request: Request, response: Response) -> dict[str, Any]:
    """
    **爱发电 Webhook 接口。**

    当有新的赞助订单时，爱发电会以 POST 方式回调此接口，
    我们将其中的订单实例（`IfdianOrder`）记录到 `data/sponsors.json`。
    正常情况下只应被爱发电调用。
    """

    create_json_file_if_not_exists(SPONSORS_FILE, [])

    # 读取原始请求体，用于解析订单与（可选）签名校验
    body = await request.body()

    # 解析订单（body 为 JSON，直接交给 pydantic 校验）
    try:
        order = IfdianWebhookResponse.model_validate_json(body)
    except Exception as e:
        print(f"[X] Failed to parse ifdian webhook payload.\n  - {e}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"ec": 400, "em": "invalid payload"}

    # 若在 settings.json 中配置了 ifdian.userId / ifdian.token，则校验请求签名
    ifdian_settings = settings.get("ifdian")
    if ifdian_settings and ifdian_settings.get("userId") and ifdian_settings.get("token"):
        signature = request.headers.get("X-Ifdian-Signature", "")
        ts = request.headers.get("X-Ifdian-Ts", "")
        if not verify_webhook_signature(ifdian_settings["userId"], ifdian_settings["token"], ts, signature):
            print("[X] Ifdian webhook signature validation failed.")
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {"ec": 401, "em": "signature validation failed"}
    else:
        print("[W] Ifdian webhook signature check is disabled. Configure settings.json -> ifdian to enable it.")

    # 追加赞助订单实例到赞助者列表（按 out_trade_no 幂等去重，避免爱发电重试导致重复记录）
    sponsors = read_json_file(SPONSORS_FILE)
    existing_ids = {
        item["out_trade_no"]
        for item in sponsors
        if isinstance(item, dict) and item.get("out_trade_no")
    }
    order_inst = order.data.order.model_dump(mode="json")
    if order_inst["out_trade_no"] not in existing_ids:
        sponsors.append(order_inst)
        write_json_file(SPONSORS_FILE, sponsors)

    return IFDIAN_RESPONSE

#endregion
