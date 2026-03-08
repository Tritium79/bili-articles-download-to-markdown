import argparse
import subprocess
import os
from bs4 import BeautifulSoup
import re
import sys

# 程序描述
DESCRIPTION = """
========================================
       B站专栏/动态转Markdown工具
========================================
"""

if __name__ == "__main__":
    print(DESCRIPTION)
    
    # 1. 参数解析：支持命令行直接传入或启动后手动输入
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("请输入B站专栏或动态URL (例如 https://www.bilibili.com/read/cv...):")
        url = input().strip()
        if not url:
            print("错误: URL不能为空")
            exit(1)
    
    # 定义中间临时文件名
    raw_html = 'raw_tmp.html'
    formatted_html = 'formatted_tmp.html'
    minified_html = 'minified_tmp.html'
    
    print(f"\n[1/5] 正在获取网页内容...")
    # 2. 获取原始 HTML (使用 -o 指定输出)
    subprocess.run(['python', 'fetch_html.py', url, '-o', raw_html])
    
    if not os.path.exists(raw_html):
        print("错误：无法获取网页，请检查网络或URL是否正确。")
        exit(1)

    # 3. 提取正文内容 (使用 -o)
    print("[2/5] 正在解析正文区域...")
    subprocess.run(['python', 'format_blbl_html.py', raw_html, '-o', formatted_html])
    
    # 4. 简化 HTML 结构 (使用 -o)
    print("[3/5] 正在清洗无用标签...")
    subprocess.run(['python', 'minify_html.py', formatted_html, '-o', minified_html])
    
    # 5. 提取元数据：标题、作者、发布时间
    print("[4/5] 正在提取文章元数据...")
    with open(raw_html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
        # 提取标题并清理非法字符
        title_raw = soup.title.string if soup.title else "bilibili_article"
        title = re.sub(r'[\\/:*?"<>|]', '_', title_raw).replace('\n', '').strip()
        
        # 提取作者 (适配多种B站模板)
        author_tag = soup.select_one('.up-info__name, .user-name, .up-name, .opus-module-author__name')
        author = author_tag.get_text(strip=True) if author_tag else "未知作者"
        
        # 提取发布时间
        date_tag = soup.select_one('.pub-date-text, .publish-text, .opus-module-content-info-pub-time')
        date = date_tag.get_text(strip=True) if date_tag else "未知时间"

    output_md = f"{title}.md"
    
    # 6. 转换为 Markdown
    print(f"[5/5] 正在转换并生成 Markdown 文件: {output_md}")
    # 调用你修改后的 html_to_md.py，传入元数据参数
    subprocess.run([
        'python', 'html_to_md.py', 
        minified_html, 
        '-o', output_md,
        '--author', author,
        '--date', date,
        '--url', url
    ])
    
    # 7. 清理临时文件
    print("\n正在清理临时缓存...")
    for tmp_file in [raw_html, formatted_html, minified_html]:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
            
    print("=" * 40)
    print(f"🎉 转换成功！")
    print(f"文件位置: {os.path.abspath(output_md)}")
    print("=" * 40)