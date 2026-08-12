# MKSS.Next

`Minecraft 芝士站` 是一个 **Plain Craft Launcher 2** 的自定义主页。

**Minecraft 冷知识**和其他好玩的东西都在这里啦！

> [!WARNING]
> 这个项目不是 [MKSS](https://github.com/awaEric233/MKSS)。

> [!NOTE]
> English users? Please go [here](https://github.com/awaEric233/MKSS.Next)!

## ✨ 特性

- **崭新的 Web 框架：** PHP -> Python + FastAPI + Jinja2；
- **原生适配 PCL2：** 主页以 XAML 渲染，开箱即用；
- **内容自动同步：** 通过 SHA-1 指纹告知 PCL2 主页是否需要更新；
- **数据驱动：** 分区、源、标签与公告都是纯 JSON 文件，无需改动代码。

## 🏠 快速开始

1. 打开你的 **Plain Craft Launcher 2**；
2. 点击顶栏上的“设置”；
3. 点击侧栏上的“个性化”；
4. 点击“主页”卡片里的“联网更新”。
5. 将我们的 URL `https://mkss.services.awaeric.xyz` 输入到文本框中。

## 💡 投稿想法

请使用信息卡片中的链接。

> [!IMPORTANT]
> **请不要使用除表单以外的任何方式投稿！**<br/>
> 这会加剧审核者的负担。<br/>

## 🎈 部署到你的服务器

1. 克隆这个存储库；
2. 安装 Python 3.10+，运行 `pip install -r requirements.txt` 来安装依赖；
3. 查看 [SETUP_ZH.md](https://github.com/awaEric233/MKSS.Next/blob/main/SETUP_ZH.md) 并设置你的服务器；
4. 使用 _FastAPI CLI_ 启动服务器：

   ```bash
   fastapi run app.py
   ```

## 📁 项目结构

```text
app.py          # FastAPI 入口与全部路由
models/         # Pydantic 数据模型
utils/          # 页面构建、哈希、爱发电 API、文件读写等工具
templates/      # PCL2 主页 XAML 模板
data/           # 站点配置与内容数据
static/         # 静态资源
```

## 🥳 贡献者

感谢各位贡献者对 MKSS.Next 的支持！

![Contributors](https://contrib.rocks/image?repo=awaEric233/MKSS.Next)
