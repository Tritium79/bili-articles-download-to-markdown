import argparse
import os
from bs4 import BeautifulSoup


def minify_html(input_file, output_file):
    """
    简化HTML文件，删除多余的标签属性和修饰

    参数:
    input_file (str): 输入的HTML文件路径
    output_file (str): 输出的简化HTML文件路径

    返回:
    bool: 成功返回True，失败返回False
    """
    try:
        # 读取HTML文件
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 处理图片标签结构
        for pic_div in soup.find_all('div', class_='opus-para-pic'):
            # 找到图片标签
            img_tag = pic_div.find('img', class_='b-img__inner')
            if img_tag:
                # 保留src属性，删除其他属性
                src = img_tag.get('src')
                new_img = soup.new_tag('img')
                new_img['src'] = src
                # 替换整个div结构为简化的img标签
                pic_div.replace_with(new_img)

        # 递归处理所有标签
        for tag in soup.find_all(True):
            # 删除所有以data-v-开头的属性
            attrs_to_remove = [attr for attr in tag.attrs if attr.startswith('data-v-')]
            for attr in attrs_to_remove:
                del tag.attrs[attr]

            # 可以在这里添加更多的简化规则
            # 例如：删除style属性
            if 'style' in tag.attrs:
                del tag.attrs['style']

        # 获取简化后的HTML内容
        minified_html = soup.prettify()

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)

        # 写入文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified_html)

        print(f"成功简化HTML并保存到: {output_file}")
        return True

    except Exception as e:
        print(f"处理HTML失败: {e}")
        return False


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='简化HTML文件，删除多余标签和修饰')
    parser.add_argument('input', help='输入的HTML文件路径')
    parser.add_argument('-o', '--output', default='minified.html', help='输出的简化HTML文件名(默认: minified.html)')

    args = parser.parse_args()

    # 调用函数简化HTML
    minify_html(args.input, args.output)