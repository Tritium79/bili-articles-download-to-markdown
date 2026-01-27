import os
import re
import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches
import docx
try:
    from html2docx import html2docx
except ImportError:
    print("html2docx库未安装，将跳过此转换方法")
    exit(1)


def convert_html_to_docx(html_content, output_file):
    """
    使用html2docx库将HTML内容转换为Word文档
    
    参数:
    html_content (str): HTML内容
    output_file (str): 输出的Word文件路径
    
    返回:
    bool: 成功返回True，失败返回False
    """
    try:
        # 使用html2docx库转换
        buf = html2docx(html_content, title="Converted Document")
        
        # 将结果保存到文件
        with open(output_file, "wb") as f:
            f.write(buf.getvalue())
        
        print(f"成功使用html2docx转换HTML为Word并保存到: {output_file}")
        return True
        
    except Exception as e:
        print(f"使用html2docx转换失败: {e}")
        return False


def download_images_and_update_html(input_file, base_dir="images"):
    """
    下载HTML中的图片并更新HTML内容，优先使用本地已存在的图片
    """
    # 读取HTML文件
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 修复代码块：如果pre标签有codecontent属性，则将内容放入code标签中
    for pre_tag in soup.find_all('pre'):
        codecontent = pre_tag.get('codecontent')
        if codecontent and codecontent.strip():
            # 找到或创建code标签
            code_tag = pre_tag.find('code')
            if not code_tag:
                code_tag = soup.new_tag('code')
                pre_tag.append(code_tag)
            
            # 将codecontent的内容设置到code标签中
            code_tag.string = codecontent
    
    # 创建图片保存目录
    img_dir = os.path.join(os.path.dirname(input_file), base_dir)
    os.makedirs(img_dir, exist_ok=True)
    
    # 获取目录中已有的图片文件列表
    existing_files = set(os.listdir(img_dir))
    
    # 查找所有图片标签
    for img_tag in soup.find_all('img'):
        img_src = img_tag.get('src') or img_tag.get('data-src')
        if img_src:
            # 处理相对URL
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            elif not img_src.startswith(('http://', 'https://')):
                img_src = 'https://i0.hdslb.com' + img_src
            
            # 从URL中提取文件名
            original_filename = os.path.basename(img_src.split('?')[0])
            if '.' not in original_filename or len(original_filename) < 3:
                # 如果原始文件名没有扩展名或太短，从内容类型推断
                try:
                    response_head = requests.head(img_src, timeout=5)
                    content_type = response_head.headers.get('content-type', '')
                    ext = '.jpg'  # 默认扩展名
                    if 'png' in content_type.lower():
                        ext = '.png'
                    elif 'gif' in content_type.lower():
                        ext = '.gif'
                    elif 'jpeg' in content_type.lower():
                        ext = '.jpg'
                    
                    original_filename = f"{hash(img_src)}{ext}"
                except:
                    original_filename = f"{hash(img_src)}.jpg"
            
            # 检查本地是否已有对应图片
            local_img_path = os.path.join(img_dir, original_filename)
            
            # 检查现有文件中是否有匹配的
            matched_existing_file = None
            for existing_file in existing_files:
                if original_filename == existing_file or \
                   original_filename.split('.')[0] == existing_file.split('.')[0]:  # 检查文件名（不含扩展名）
                    matched_existing_file = existing_file
                    local_img_path = os.path.join(img_dir, matched_existing_file)
                    break
            
            # 如果本地没有对应图片，则下载
            if matched_existing_file is None:
                try:
                    # 下载图片
                    response = requests.get(img_src, timeout=10)
                    response.raise_for_status()
                    
                    # 获取文件扩展名
                    ext = '.jpg'  # 默认扩展名
                    content_type = response.headers.get('content-type', '')
                    if 'png' in content_type.lower():
                        ext = '.png'
                    elif 'gif' in content_type.lower():
                        ext = '.gif'
                    elif 'jpeg' in content_type.lower() or 'jpg' in content_type.lower():
                        ext = '.jpg'
                    
                    # 使用合适的文件名保存
                    filename = os.path.basename(img_src.split('?')[0])
                    if not filename or len(filename) < 3:
                        filename = f"image_{hash(img_src)}{ext}"
                    elif not filename.endswith((ext,)):
                        # 如果原始文件名没有正确的扩展名，添加它
                        if '.' in filename:
                            # 替换扩展名
                            name_part = filename.rsplit('.', 1)[0]
                            filename = f"{name_part}{ext}"
                        else:
                            filename = f"{filename}{ext}"
                    
                    local_img_path = os.path.join(img_dir, filename)
                    
                    # 保存图片
                    with open(local_img_path, 'wb') as img_file:
                        img_file.write(response.content)
                    
                    print(f"图片已下载并更新路径: {local_img_path}")
                    
                except Exception as e:
                    print(f"下载图片失败 {img_src}: {e}")
                    continue  # 如果下载失败，跳过这张图片
            else:
                print(f"使用本地已存在的图片: {local_img_path}")
            
            # 将图片嵌入为base64数据URI，以确保html2docx能正确处理
            import base64
            try:
                with open(local_img_path, 'rb') as img_file:
                    img_data = img_file.read()
                    img_base64 = base64.b64encode(img_data).decode('utf-8')
                    
                    # 根据文件扩展名确定MIME类型
                    mime_type = 'image/jpeg'  # 默认类型
                    if local_img_path.lower().endswith('.png'):
                        mime_type = 'image/png'
                    elif local_img_path.lower().endswith('.gif'):
                        mime_type = 'image/gif'
                    elif local_img_path.lower().endswith('.jpg') or local_img_path.lower().endswith('.jpeg'):
                        mime_type = 'image/jpeg'
                    
                    img_tag['src'] = f'data:{mime_type};base64,{img_base64}'
            except Exception as e:
                print(f"无法读取本地图片文件 {local_img_path}: {e}")
                # 如果无法读取本地文件，尝试使用原始URL
                img_tag['src'] = img_src
    
    return str(soup)


if __name__ == "__main__":
    # 默认处理之前生成的格式化HTML文件
    input_file = "minified_bilibili.html"
    output_file = "temp_formatted_bilibili_html2docx.docx"
    
    if not os.path.exists(input_file):
        print(f"输入文件不存在: {input_file}")
        exit(1)
    
    # 下载图片并更新HTML
    updated_html = download_images_and_update_html(input_file)
    
    # 转换为Word文档
    success = convert_html_to_docx(updated_html, output_file)
    
    if success:
        print("HTML到Word转换成功！")
    else:
        print("HTML到Word转换失败！")
        exit(1)