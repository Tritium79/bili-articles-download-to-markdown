import requests
import argparse
import time

def get_user_articles(uid):
    articles = []
    page = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': f'https://space.bilibili.com/{uid}/article'
    }
    
    print(f"正在获取用户 {uid} 的文章列表...")
    
    while True:
        # B站专栏列表 API
        api_url = f"https://api.bilibili.com/x/space/article?mid={uid}&pn={page}&ps=30&sort=publish_time"
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            data = response.json()
            
            if data['code'] != 0:
                print(f"获取失败: {data['message']}")
                break
                
            art_list = data['data'].get('articles', [])
            if not art_list:
                break
                
            for art in art_list:
                articles.append({
                    'id': art['id'],
                    'title': art['title'],
                    'url': f"https://www.bilibili.com/read/cv{art['id']}"
                })
            
            print(f"已获取第 {page} 页，当前共 {len(articles)} 篇文章")
            page += 1
            time.sleep(1) # 频率限制，保护账号
        except Exception as e:
            print(f"请求出错: {e}")
            break
            
    return articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('uid', help='用户UID')
    args = parser.parse_args()
    res = get_user_articles(args.uid)
    for a in res:
        print(f"{a['id']} | {a['title']}")