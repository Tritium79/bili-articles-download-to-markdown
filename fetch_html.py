import requests
import argparse
import os

def fetch_html(url, output_file):
    """
    从指定URL获取HTML内容并保存到本地文件
    
    参数:
    url (str): 要获取的网页URL
    output_file (str): 保存HTML内容的本地文件路径
    
    返回:
    bool: 成功返回True，失败返回False
    """
    try:
        # 添加浏览器请求头模拟真人访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://www.bilibili.com/'
        }
        
        # 发送GET请求获取网页内容
        response = requests.get(url, headers=headers, timeout=10)
        # 检查响应状态码
        response.raise_for_status()
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"成功获取HTML并保存到: {output_file}")
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"获取HTML失败: {e}")
        return False
    except IOError as e:
        print(f"写入文件失败: {e}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='从网页获取HTML内容并保存到本地')
    parser.add_argument('url', help='要获取的网页URL')
    parser.add_argument('-o', '--output', default='output.html', help='输出文件名(默认: output.html)')
    
    args = parser.parse_args()
    
    # 调用函数获取HTML
    fetch_html(args.url, args.output)