import argparse
from bs4 import BeautifulSoup
import os

def format_blbl_html(input_file, output_file):
    """
    从B站专栏HTML文件中提取特定内容并保存
    
    参数:
    input_file (str): 输入的HTML文件路径
    output_file (str): 输出的HTML文件路径
    
    返回:
    bool: 成功返回True，失败返回False
    """
    try:
        # 读取HTML文件
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找特定元素
        # 对应document.querySelector("#app > div.opus-detail > div.bili-opus-view > div.opus-module-content")
        target_element = soup.select_one('#app > div.opus-detail > div.bili-opus-view > div.opus-module-content')
        
        if not target_element:
            print("未找到目标元素")
            return False
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # 保存提取的内容
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(target_element))
            
        print(f"成功提取内容并保存到: {output_file}")
        return True
    
    except IOError as e:
        print(f"文件操作失败: {e}")
        return False
    except Exception as e:
        print(f"处理失败: {e}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='从B站专栏HTML中提取特定内容')
    parser.add_argument('input_file', help='输入的HTML文件路径')
    parser.add_argument('-o', '--output', default='formatted_output.html', help='输出文件名(默认: formatted_output.html)')
    
    args = parser.parse_args()
    
    # 调用函数处理HTML
    format_blbl_html(args.input_file, args.output)