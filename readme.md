# B站专栏转Markdown工具

## 项目简介

这是一个可以将B站专栏文章转换为Markdown文档的工具，支持自动提取网页标题、作者、发布时间，并保留文章中的图片链接与排版格式。此外，还支持通过用户UID一键批量抓取该用户的所有专栏文章。

## 功能特点

- 自动获取B站专栏文章/动态内容
- 提取网页标题、作者名、发布日期及原文链接
- 支持单篇URL转换或用户UID全量文章抓取
- 转换为通用的Markdown格式，适配Typora、Obsidian等编辑器
- 简单易用的命令行界面

## 工作流程

1. 接收用户输入的B站URL或用户UID
2. 若为UID，调用 `fetch_user_articles.py` 获取全量文章列表
3. 通过 `fetch_html.py` 获取网页原始HTML内容
4. 调用 `format_blbl_html.py` 和 `minify_html.py` 处理HTML，提取有效正文
5. `html_to_md.py` 将处理后的HTML转换为包含元数据的Markdown文档
6. 以文章标题命名并保存到本地（批量模式下自动创建用户专属文件夹）

## 临时文件说明

* 程序运行过程中会生成 `raw_tmp.html` 等临时文件用于中间数据处理
* 转换完成后，这些临时文件会自动被清理，以保持目录整洁

## 安装说明

1. 克隆或下载本项目到本地
2. 安装Python 3.6+环境
3. 安装依赖包：
```
pip install -r requirements.txt

```

## 使用方法

1. 打开命令行，进入项目目录
2. **转换单篇文章**：
```
python main.py [B站专栏URL]

```

例如：`python main.py "https://www.bilibili.com/read/cv4613248"`
3. **批量转换用户全部文章**：
```
python main.py [用户UID]

```

例如：`python main.py 1145468140`
4. **交互模式**：
直接运行 `python main.py`，根据提示输入URL或UID。

## 项目结构

```
bili-read-getter/
├── fetch_html.py           # 获取网页内容
├── fetch_user_articles.py  # 获取用户全量文章列表
├── format_blbl_html.py     # 处理B站HTML
├── html_to_md.py           # 转换HTML为Markdown（含元数据插入）
├── main.py                 # 主程序入口（支持单篇/批量逻辑）
├── minify_html.py          # 简化HTML内容
├── requirements.txt        # 依赖包列表
└── venv/                   # 虚拟环境

```

## 免责声明

本工具仅供学习交流使用，请勿用于任何形式的商业用途。本工具不保证对所有B站文章都能完美转换，转换效果受B站网页结构变动影响。

## 作者信息

* 作者：[@罗橙二（哔哩哔哩）](https://space.bilibili.com/1145468140)

## 致谢

感谢使用本工具！如有问题或建议，请联系作者。
邮箱：lxz2102141297@163.com 或者直接在哔哩哔哩私信。
哔哩哔哩：[@罗橙二](https://space.bilibili.com/1145468140)（uid:1145468140）
致敬：[@Up主纪念馆](https://space.bilibili.com/1362658251)（uid:1362658251）