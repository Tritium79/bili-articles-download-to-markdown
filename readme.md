# B站专栏转Markdown工具 (Bili-Read-Getter to MD)

## 项目变更说明

本项目基于 **[@罗橙二](https://space.bilibili.com/1145468140)** 的 [bili-read-getter (Gitee)](https://gitee.com/StarVase/bili-read-getter) 项目修改。

**主要改动：**

* **转换格式：** 由 `HTML to Word` 改为 `HTML to Markdown`。
* **批量抓取：** 一键获取并下载该用户全部专栏文章。
* **元数据注入：** 在生成的 Markdown 顶部自动添加作者、发布时间及原文链接。

## 项目简介

这是一个可以将B站专栏文章转换为 Markdown 文档的工具。它能够自动提取网页标题、作者、发布时间，并尽可能保留文章中的图片链接与排版格式。支持单篇转换与用户全量批量抓取，生成的 `.md` 文件可完美适配 Typora、Obsidian 等编辑器。

## 功能特点

* **多源支持：** 自动获取B站专栏文章（read）或 Opus 动态内容。
* **元数据提取：** 自动抓取网页标题、作者名、发布日期及原文链接并写入文档。
* **批量抓取：** 支持通过用户 UID 自动获取该用户投稿的所有文章并分类保存。
* **格式友好：** 转换为通用 Markdown 格式，代码块与图片引用清晰。
* **简洁高效：** 命令行操作，自动清理处理过程中的临时 HTML 文件。

## 工作流程

1. 接收用户输入的 B 站 URL 或用户 UID。
2. 若为 UID，调用 `fetch_user_articles.py` 获取全量文章列表。
3. 通过 `fetch_html.py` 获取网页原始 HTML 内容。
4. 调用 `format_blbl_html.py` 和 `minify_html.py` 处理 HTML，提取有效正文。
5. `html_to_md.py` 将处理后的内容转换为包含元数据的 Markdown 文档。
6. 以文章标题命名并保存（批量模式下自动创建用户专属文件夹）。

## 安装说明

1. 克隆或下载本项目到本地。
2. 安装 Python 3.6+ 环境。
3. 安装依赖包：
```bash
pip install -r requirements.txt

```



## 使用方法

1. **转换单篇文章**：
```bash
python main.py [B站专栏URL]

```


2. **批量转换用户全部文章**：
```bash
python main.py [用户UID]

```


3. **交互模式**：
直接运行 `python main.py`，根据提示输入 URL 或 UID。

## 项目结构

```text
bili-read-getter/
├── fetch_html.py           # 获取网页内容
├── fetch_user_articles.py  # 获取用户全量文章列表
├── format_blbl_html.py     # 处理B站HTML
├── html_to_md.py           # 转换HTML为Markdown（含元数据插入）
├── main.py                 # 主程序入口（支持单篇/批量逻辑）
├── minify_html.py          # 简化HTML内容
└── requirements.txt        # 依赖列表

```

## 免责声明

本工具仅供学习交流使用，请勿用于任何形式的商业用途。本工具不保证对所有B站文章都能完美转换，转换效果受B站网页结构变动影响。

### 作者

* **Tritium79**
* **项目地址：** [https://github.com/Tritium79](https://github.com/Tritium79)

### 原作者

* **@罗橙二 (哔哩哔哩)**
* **原项目地址：** [https://gitee.com/StarVase/bili-read-getter](https://gitee.com/StarVase/bili-read-getter)	[https://www.bilibili.com/video/BV19dY4zvEcy](https://www.bilibili.com/video/BV19dY4zvEcy)