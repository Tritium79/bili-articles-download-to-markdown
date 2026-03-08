import argparse
import subprocess
import os
from bs4 import BeautifulSoup
import re
import sys

# 程序描述
DESCRIPTION = "B站专栏转Markdown工具 (Simplified Version)"

if __name__ == "__main__":
    print(DESCRIPTION)
    print("=" * 30)
    
    # 1. 参数解析：支持命令行参数或手动输入
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("请输入B站专栏或动态URL:")
        url = input().strip()
        if not url:
            print("错误: URL不能为空")
            exit(1)
    
    # 定义中间临时文件名
    raw_html = 'raw_tmp.html'
    formatted_html = 'formatted_tmp.html'
    minified_html = 'minified_tmp.html'
    
    print(f"开始处理 URL: {url}")

    # 2. 获取原始 HTML (注意添加 -o)
    print("正在获取网页内容...")
    subprocess.run(['python', 'fetch_html.py', url, '-o', raw_html])
    
    if not os.path.exists(raw_html):
        print("错误：无法获取网页，请检查网络或URL。")
        exit(1)

    # 3. 提取正文内容 (注意添加 -o)
    print("正在解析正文...")
    subprocess.run(['python', 'format_blbl_html.py', raw_html, '-o', formatted_html])
    
    # 4. 简化 HTML 结构 (注意添加 -o)
    print("正在清理HTML标签...")
    subprocess.run(['python', 'minify_html.py', formatted_html, '-o', minified_html])
    
    # 5. 获取标题作为最终文件名
    with open(raw_html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        title = soup.title.string if soup.title else "bilibili_article"
        # 移除文件名非法字符
        title = re.sub(r'[\\/:*?"<>|]', '_', title).replace('\n', '').strip()
    
    output_md = f"{title}.md"
    
    # 6. 转换为 Markdown (使用你新写的脚本，注意添加 -o)
    print(f"正在转换并生成: {output_md}")
    subprocess.run(['python', 'html_to_md.py', minified_html, '-o', output_md])
    
    # 7. 清理临时文件 (不再需要 Word 相关的临时文件)
    print("正在清理临时文件...")
    for tmp_file in [raw_html, formatted_html, minified_html]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            
    print("=" * 30)
    print(f"转换成功！文件已保存为: {output_md}")