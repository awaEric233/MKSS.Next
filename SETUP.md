# MKSS.Next Setup

To set up your MKSS.Next, **follow these steps**:

1. Edit `/data/settings.json` to configure the website settings;
2. Edit files under `/data/categories/` to add or modify categories;
3. Edit `/data/tags.json` to add or modify tags of authors;
4. Edit `/data/announcements.json` to add or modify announcements;
5. Edit `/data/links.json` to add or modify links (optional).

## Settings

The settings file is a JSON file.  
It contains the following settings:

- `info`: General information.
    - `baseUrl`: Base URL of the website (**no trailing slash!**);
    - `postUrl`: URL of the submission form.
- `ifdian`: Afdian settings (optional).
    - `link`: The slug after `https://ifdian.net/a/` used by the "Sponsor the author" button on the thanks page (e.g. `transae`);
    - `userId`: ID of your Afdian account;
    - `token`: Token of your Afdian account.

> [!NOTE]
> Once `ifdian` is configured, the sponsor features are enabled: `userId`/`token`
> are used to fetch the real sponsor list from the Afdian `query-sponsor` API
> (refreshed on server startup and cached afterwards), and the webhook at
> `POST /ifdian` verifies the incoming request signature before recording new
> sponsor orders. Without these credentials, the sponsor list stays empty.

#### Example

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

## Categories

Each category is a JSON file under `/data/categories/`.

### Category fields

- `name`: Name of the category;
- `logo`: Logo of the category;
- `sources`: List of sources.

#### Example

```json
{
    "name": "Scaffolding - Example",
    "logo": "Grass",
    "sources": [
        {
            "title": "This is a source!",
            "author": "awa_Eric233",
            "content": "Some content here.\nThis is a new line."
        }
    ]
}
```

### Source fields

- `title`: Title of the source;
- `author`: Author of the source;
- `content`: Content of the source (use `\n` for a new line).

#### Example

```json
{
    "title": "This is a source!",
    "author": "awa_Eric233",
    "content": "Some content here.\nThis is a new line."
}
```

### Ignore

The following files in the `/data/categories/` directory will be ignored:

- Files whose names start with a dot (.);
- Files that are not in JSON format.

#### Example

```
.HiddenFile.json
IncorrectFormat.txt
```

## Tags

The tags file is a JSON file.  
Each tagged author has a list of tags.  
The key is the author's name, and the value is the list of tags.

#### Example

```json
{
    "awa_Eric233": [
        "MKSS Admin",
        "MKSS Reviewer"
    ]
}
```

## Announcements

The announcements file is a JSON list of announcements.

Each announcement contains the following fields:

- `title`: Title of the announcement;
- `info`: Short description shown on the announcement card;
- `isLink`: Whether the announcement is a link. `false` opens a popup window
  with the content, `true` opens a web page with the URL;
- `content`: Content of the announcement, or the link URL if `isLink` is `true`.

#### Example

```json
[
    {
        "title": "Welcome to MKSS.Next!",
        "info": "If you can see this announcement, your deployment is successful!",
        "isLink": false,
        "content": "Congratulations! You have successfully deployed MKSS.Next!"
    },
    {
        "title": "Official community",
        "info": "Join us!",
        "isLink": true,
        "content": "https://example.com/community"
    }
]
```

## Links

The links file is a JSON dictionary.  
Each key is a group name, and each value is a list of links.

Each link contains the following fields:

- `title`: Title of the link;
- `info`: Description of the link;
- `link`: URL of the link.

#### Example

```json
{
    "Open Source Repositories": [
        {
            "title": "GitHub",
            "info": "awaEric233/MKSS.Next",
            "link": "https://github.com/awaEric233/MKSS.Next"
        }
    ]
}
```
