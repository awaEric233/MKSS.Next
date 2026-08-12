# MKSS.Next 部署配置

要部署 MKSS.Next，**请按照以下步骤进行**：

1. 编辑 `/data/settings.json` 来配置站点设置；
2. 编辑 `/data/categories/` 下的文件来添加或修改分区；
3. 编辑 `/data/tags.json` 来添加或修改贡献者的标签；
4. 编辑 `/data/announcements.json` 来添加或修改公告；
5. 编辑 `/data/links.json` 来添加或修改链接（可选）。

## 设置（Settings）

设置文件是一个 JSON 文件。  
它包含以下设置：

- `info`：站点信息。
    - `baseUrl`：站点的基础 URL（**结尾不要带斜杠！**）；
    - `postUrl`：投稿表单的 URL。
- `ifdian`：爱发电相关设置（可选）。
    - `link`：致谢页“赞助作者”按钮使用的、`https://ifdian.net/a/` 之后的自定义段（例如 `transae`）；
    - `userId`：你的爱发电用户 ID；
    - `token`：你的爱发电 API Token。

> [!NOTE]
> 配置了 `ifdian` 后即开启赞助功能：`userId`/`token` 用于通过爱发电
> `query-sponsor` 接口拉取真实的赞助者列表（服务器启动时刷新并缓存），
> Webhook 接口 `POST /ifdian` 也会先校验请求签名，再记录新的赞助订单。
> 未配置凭据时，赞助者列表保持为空。

#### 示例

```json
{
    "info": {
        "baseUrl": "https://example.com",
        "postUrl": "https://example.com/post"
    },
    "ifdian": {
        "link": "transae",
        "userId": "YourAfdianUserId",
        "token": "YourAfdianToken"
    }
}
```

## 分区（Categories）

每个分区都是 `/data/categories/` 下的一个 JSON 文件。

### 分区字段

- `name`：分区名称；
- `logo`：分区图标；
- `sources`：源（投稿内容）列表。

#### 示例

```json
{
    "name": "脚手架 - 示例",
    "logo": "Grass",
    "sources": [
        {
            "title": "这是一条源！",
            "author": "awa_Eric233",
            "content": "这里是内容。\n这是新的一行。"
        }
    ]
}
```

### 源字段

- `title`：源标题；
- `author`：源贡献者；
- `content`：源内容（使用 `\n` 换行）。

#### 示例

```json
{
    "title": "这是一条源！",
    "author": "awa_Eric233",
    "content": "这里是内容。\n这是新的一行。"
}
```

### 忽略规则

`/data/categories/` 目录下以下文件会被忽略：

- 以点号（.）开头的文件；
- 非 JSON 格式的文件。

#### 示例

```
.HiddenFile.json
IncorrectFormat.txt
```

## 标签（Tags）

标签文件是一个 JSON 文件。  
每个被标记的贡献者都有一组标签。  
键为贡献者名称，值为标签列表。

#### 示例

```json
{
    "awa_Eric233": [
        "MKSS 管理员",
        "MKSS 审核"
    ]
}
```

## 公告（Announcements）

公告文件是一个 JSON 列表。

每条公告包含以下字段：

- `title`：公告标题；
- `info`：公告卡片上显示的简介；
- `isLink`：是否为链接。`false` 会弹窗展示内容，`true` 会用 URL 打开网页；
- `content`：公告内容；若 `isLink` 为 `true`，则为链接 URL。

#### 示例

```json
[
    {
        "title": "欢迎使用 MKSS.Next！",
        "info": "如果你看到这条公告，那么你的部署应该已经成功了！",
        "isLink": false,
        "content": "恭喜！你已成功部署了 MKSS.Next！"
    },
    {
        "title": "官方交流群",
        "info": "欢迎加入！",
        "isLink": true,
        "content": "https://example.com/community"
    }
]
```

## 链接（Links）

链接文件是一个 JSON 字典。  
键为分组名称，值为链接列表。

每条链接包含以下字段：

- `title`：链接标题；
- `info`：链接描述；
- `link`：链接 URL。

#### 示例

```json
{
    "开源存储库": [
        {
            "title": "GitHub",
            "info": "awaEric233/MKSS.Next",
            "link": "https://github.com/awaEric233/MKSS.Next"
        }
    ]
}
```
