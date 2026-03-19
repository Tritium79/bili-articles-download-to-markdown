import argparse
import os
import html2text
from bs4 import BeautifulSoup

def convert_to_md(input_file, output_file, author="未知", date="未知", url=""):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 配置 html2text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.body_width = 0
        h.ignore_images = False

        # 转换正文
        markdown_body = h.handle(html_content)

        # 构造顶部的元数据信息
        # 使用 Markdown 的引用块或列表格式，让它看起来更整洁
        header = f"""# 文章信息
* **作者:** {author}
* **发布时间:** {date}
* **原文链接:** [{url}]({url})

---
"""
        final_content = header + markdown_body

        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
        
        print(f"成功转换为Markdown: {output_file}")
        return True
    except Exception as e:
        print(f"转换失败: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-o', '--output')
    # 增加传入元数据的参数
    parser.add_argument('--author', default="未知")
    parser.add_argument('--date', default="未知")
    parser.add_argument('--url', default="")
    
    args = parser.parse_args()
    convert_to_md(args.input, args.output, args.author, args.date, args.url)