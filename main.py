import argparse
import subprocess
import os
from bs4 import BeautifulSoup
import re
import sys
import time

# 导入刚才写的函数
from fetch_user_articles import get_user_articles

DESCRIPTION = "B站专栏全量抓取工具 (Markdown版)"

def process_single_url(url, save_dir="."):
    """处理单个URL的逻辑"""
    raw_html = 'raw_tmp.html'
    formatted_html = 'formatted_tmp.html'
    minified_html = 'minified_tmp.html'
    
    # 执行流水线
    subprocess.run(['python', 'fetch_html.py', url, '-o', raw_html], capture_output=True)
    if not os.path.exists(raw_html): return
    
    subprocess.run(['python', 'format_blbl_html.py', raw_html, '-o', formatted_html], capture_output=True)
    subprocess.run(['python', 'minify_html.py', formatted_html, '-o', minified_html], capture_output=True)
    
    # 提取元数据
    with open(raw_html, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        title_raw = soup.title.string if soup.title else "article"
        title = re.sub(r'[\\/:*?"<>|]', '_', title_raw).replace('\n', '').strip()
        author = (soup.select_one('.up-info__name, .user-name') or type('Obj', (object,), {'get_text': lambda x, **k: "未知"})()).get_text(strip=True)
        date = (soup.select_one('.pub-date-text, .publish-text') or type('Obj', (object,), {'get_text': lambda x, **k: "未知"})()).get_text(strip=True)

    output_md = os.path.join(save_dir, f"{title}.md")
    
    # 转换为 Markdown
    subprocess.run([
        'python', 'html_to_md.py', minified_html, '-o', output_md,
        '--author', author, '--date', date, '--url', url
    ])
    
    # 清理
    for tmp in [raw_html, formatted_html, minified_html]:
        if os.path.exists(tmp): os.remove(tmp)

if __name__ == "__main__":
    print(DESCRIPTION)
    
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = input("请输入URL或用户UID: ").strip()

    # 判断是UID还是单个URL
    if target.isdigit():
        uid = target
        articles = get_user_articles(uid)
        
        if not articles:
            print("该用户没有发布过专栏。")
            exit()
            
        # 创建用户专属目录
        folder_name = f"user_{uid}_articles"
        os.makedirs(folder_name, exist_ok=True)
        
        print(f"\n开始批量下载 {len(articles)} 篇文章到目录: {folder_name}")
        for i, art in enumerate(articles):
            print(f"[{i+1}/{len(articles)}] 正在处理: {art['title']}")
            process_single_url(art['url'], save_dir=folder_name)
            time.sleep(0.5) # 稍微停顿，防止被封IP
        
        print(f"\n全部下载完成！保存在 {folder_name} 目录下。")
        
    else:
        # 单个URL模式
        print("识别为单篇转换模式...")
        process_single_url(target)
        print("转换完成！")
        
import shutil
if os.path.exists("__pycache__"):
    shutil.rmtree("__pycache__")