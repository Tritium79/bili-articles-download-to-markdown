import argparse
import os
import html2text
from bs4 import BeautifulSoup

def convert_to_md(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 配置 html2text
        h = html2text.HTML2Text()
        h.ignore_links = False  # 保留链接
        h.body_width = 0        # 不自动换行
        h.ignore_images = False # 保留图片

        markdown_text = h.handle(html_content)

        # 确保目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        print(f"成功转换为Markdown: {output_file}")
        return True
    except Exception as e:
        print(f"转换失败: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    convert_to_md(args.input, args.output)