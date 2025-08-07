# B站专栏转Word工具

## 项目简介
这是一个可以将B站专栏文章转换为Word文档的工具，支持自动提取网页标题作为文件名，并调整图片大小以适应文档。

## 功能特点
- 自动获取B站专栏文章内容
- 提取网页标题作为Word文档名称
- 调整图片大小至页面宽度和高度的一半
- 保留文章格式和图片
- 简单易用的命令行界面

## 工作流程
1. 接收用户输入的B站专栏URL
2. 通过fetch_html.py获取网页原始HTML内容
3. 调用format_blbl_html.py和minify_html.py处理HTML，提取有效内容
4. html_to_word.py将处理后的HTML转换为Word文档，同时调整图片大小
5. 以网页标题命名并保存Word文档到本地

## 临时文件说明
- 程序运行过程中会在images/目录下生成临时图片文件，用于存储从网页中提取的图片
- 这些临时图片会在Word文档生成后保留，便于用户查看和二次编辑

## 安装说明
1. 克隆或下载本项目到本地
2. 安装Python 3.6+环境（2025年8月7日测试最高支持Python3.12）
3. 安装依赖包：
   ```
   pip install -r requirements.txt
   ```

## 使用方法
1. 打开命令行，进入项目目录
2. 运行以下命令：
   ```
   python main.py [B站专栏URL]
   ```
3. 例如：
   ```
   python main.py "https://www.bilibili.com/opus/861469533622239256"
   ```
   或者
   ```
   python main.py " https://b23.tv/aV4E92X"
   ```
   或者
   ```
   python main.py
   ```
   
4. 如果没有提供URL，程序会引导你输入

## 项目结构
```
webconverter/
├── fetch_html.py       # 获取网页内容
├── format_blbl_html.py # 处理B站HTML
├── html_to_word.py     # 转换HTML为Word
├── main.py             # 主程序入口
├── minify_html.py      # 简化HTML内容
├── requirements.txt    # 依赖包列表
├── images/             # 图片保存目录
└── venv/               # 虚拟环境
```

## 免责声明
本工具不保证对所有B站专栏文档都能完美转换，由于网页结构可能存在差异，转换效果可能会有所不同。请在使用前自行测试。

## 作者信息
- 作者：[@罗橙二（哔哩哔哩）](https://space.bilibili.com/1145468140)

## 致谢
感谢使用本工具！如有问题或建议，请联系作者。
邮箱：lxz2102141297@163.com或者直接在哔哩哔哩私信。
哔哩哔哩[@罗橙二](https://space.bilibili.com/1145468140)（uid:1145468140）
致敬：[@Up主纪念馆](https://space.bilibili.com/1362658251)（uid:1362658251）
