# MKSS.Next

`Minecraft Knowledge Sharing Site` is a custom homepage for **Plain Craft Launcher 2**.

Discover **Minecraft trivia** and more!

> [!WARNING]
> This project is not [MKSS](https://github.com/awaEric233/MKSS).

> [!NOTE]
> 中文用户请移步[此处](https://github.com/awaEric233/MKSS.Next/blob/main/README_ZH.md)！

## ✨ Features

- **Brand-new web framework**: PHP -> Python + FastAPI + Jinja2;
- **PCL2-native homepage**: rendered as XAML, directly usable in Plain Craft Launcher 2;
- **Automatic content sync**: SHA-1 fingerprints tell PCL2 when the homepage needs updating;
- **Data-driven content**: categories, sources, tags and announcements are plain JSON files, no code changes required.

## 🏠 Getting started

1. Open your **Plain Craft Launcher 2**;
2. Click "设置" on the top bar;
3. Click "个性化" on the side bar;
4. Click "联网更新" in the "主页" card;
5. Input our URL: `https://mkss.services.awaeric.xyz` into the text box.

## 💡 Submit your ideas

Please use the link in the information card.

> [!IMPORTANT]
> **Please do not submit your work through any means other than the form!**  
> This adds to the reviewers' workload.

> [!TIP]
> **The form is in Simplified Chinese.**  
> Can't read Chinese?  
> Try Google Translate.

## 🎈 Deploy to your own server

1. Clone this repository;
2. Install Python 3.10+ and run `pip install -r requirements.txt` to install dependencies;
3. View [SETUP.md](https://github.com/awaEric233/MKSS.Next/blob/main/SETUP.md) and set up your server;
4. Start the server using the _FastAPI CLI_:

   ```bash
   fastapi run app.py
   ```

## 📁 Project structure

```text
app.py          # FastAPI entrypoint and all routes
models/         # Pydantic data models
utils/          # Page building, hashing, Afdian API, file I/O helpers
templates/      # Homepage XAML templates for PCL2
data/           # Site configuration and content data
static/         # Static assets
```

## 🥳 Contributors

Thanks to all contributors for supporting MKSS.Next!

![Contributors](https://contrib.rocks/image?repo=awaEric233/MKSS.Next)
