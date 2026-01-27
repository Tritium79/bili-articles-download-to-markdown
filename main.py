import argparse
import subprocess
import os
from bs4 import BeautifulSoup
import re

# 程序描述和作者信息
DESCRIPTION = "\n===========================\nB站专栏转Word工具\n ---------- \n可以将B站专栏文章转换为Word文档\n==========================="
AUTHOR = "@罗橙二（哔哩哔哩）"

if __name__ == "__main__":
    # 显示程序信息
    print(DESCRIPTION)
    print(f"作者: {AUTHOR}")
    print("=" * 27)
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='B站专栏处理工具')
    # 添加URL参数
    parser.add_argument('url', help='要处理的B站专栏URL')
    # 解析参数
    try:
        args = parser.parse_args()
    except SystemExit:
        # 如果没有提供参数，引导用户输入
        print("请输入B站专栏URL:")
        url = input().strip()
        if not url:
            print("错误: URL不能为空")
            exit(1)
        # 手动创建args对象
        class Args:
            def __init__(self, url):
                self.url = url
        args = Args(url)
    
    print(f"接收到的URL: {args.url}")
    
    # 定义文件名
    raw_html_file = 'raw_bilibili.html'
    formatted_html_file = 'formatted_bilibili.html'
    minified_html_file = 'minified_bilibili.html'
    
    # 调用fetch_html.py获取网页内容
    print("正在获取网页内容...")
    fetch_result = subprocess.run(
        ['python', 'fetch_html.py', args.url, '-o', raw_html_file],
        capture_output=True,
        text=True
    )
    
    print(f"fetch_html.py stdout: {fetch_result.stdout}")
    print(f"fetch_html.py stderr: {fetch_result.stderr}")
    
    if fetch_result.returncode != 0:
        print(f"获取网页内容失败: {fetch_result.stderr}")
        exit(1)
    
    # 检查文件是否存在
    if not os.path.exists(raw_html_file):
        print(f"文件不存在: {raw_html_file}")
        exit(1)
    
    # 从原始HTML文件提取标题
    print("正在读取网页标题...")
    title = "output"
    try:
        with open(raw_html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        soup = BeautifulSoup(html_content, 'html.parser')
        if soup.title:
            title = soup.title.string.strip()
            # 移除非法文件名字符
            title = re.sub(r'[\\/:*?"<>|]', '_', title)
        print(f"提取到网页标题: {title}")
    except Exception as e:
        print(f"读取网页标题失败: {e}")
    
    # 调用format_blbl_html.py处理HTML
    print("正在处理HTML内容...")
    format_result = subprocess.run(
        ['python', 'format_blbl_html.py', raw_html_file, '-o', formatted_html_file],
        capture_output=True,
        text=True
    )
    
    if format_result.returncode != 0:
        print(f"处理HTML内容失败: {format_result.stderr}")
        exit(1)
    
    # 检查文件是否存在
    if not os.path.exists(formatted_html_file):
        print(f"文件不存在: {formatted_html_file}")
        exit(1)
    
    # 调用minify_html.py简化HTML
    print("正在简化HTML内容...")
    minify_result = subprocess.run(
        ['python', 'minify_html.py', formatted_html_file, '-o', minified_html_file],
        capture_output=True,
        text=True
    )
    
    if minify_result.returncode != 0:
        print(f"简化HTML内容失败: {minify_result.stderr}")
        exit(1)
    
    # 检查文件是否存在
    if not os.path.exists(minified_html_file):
        print(f"文件不存在: {minified_html_file}")
        exit(1)
    
    # 调用html_to_word.py转换为Word
    print("正在将HTML转换为Word...")
    output_word_file = title+'.docx'
    
    # 首先尝试使用html2docx库进行转换，因为它能更好地处理HTML格式
    print("正在使用html2docx库转换HTML为Word...")
    word_result = subprocess.run(
        ['python', 'convert_html_to_word.py'],
        capture_output=True,
        text=True
    )
    
    print(f"convert_html_to_word.py stdout: {word_result.stdout}")
    print(f"convert_html_to_word.py stderr: {word_result.stderr}")
    
    if word_result.returncode != 0:
        print(f"html2docx转换失败，尝试使用传统方法: {word_result.stderr}")
        # 如果html2docx转换失败，回退到传统的转换方法
        word_result = subprocess.run(
            ['python', 'html_to_word.py', minified_html_file, '-o', output_word_file],
            capture_output=True,
            text=True
        )
        
        print(f"html_to_word.py stdout: {word_result.stdout}")
        print(f"html_to_word.py stderr: {word_result.stderr}")
        
        if word_result.returncode != 0:
            print(f"转换为Word失败: {word_result.stderr}")
            exit(1)
    else:
        print("使用html2docx库转换成功！")
        # 重命名生成的临时文件为期望的输出文件名
        import shutil
        temp_output = "temp_formatted_bilibili_html2docx.docx"
        if os.path.exists(temp_output):
            # 如果目标文件已存在，先删除
            if os.path.exists(output_word_file):
                os.remove(output_word_file)
            shutil.move(temp_output, output_word_file)
            print(f"已将临时文件重命名为: {output_word_file}")
    
    print(f"处理完成！Word文档已保存为: {output_word_file}")
    print("=" * 50)
    print(f"感谢使用 {DESCRIPTION}")
    print(f"作者: {AUTHOR}")