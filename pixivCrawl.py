import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

#获取图片链接
def get_href_l(i,tag,headers):
    #tag为ascll编码的api链接
    api_data = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode=all&p={i}&csw=0&s_mode=s_tag&type=all&lang=zh&version=3670dff3cbe6178471d67bac4335ff8561f58f5e'
    #tag为非ascll编码的api链接
    api_data2 = f'https://www.pixiv.net/ajax/search/artworks/{tag}?word={tag}&order=date_d&mode=all&p={i}&csw=0&s_mode=s_tag&type=all&lang=zh&version=a094faf1b53e4f7344e5e07ae1fdf06444a87965'
    #判断tag
    if '%' in tag:
        api_data = api_data2
    try:
        r = requests.get(api_data,headers=headers)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        data = r.json()
        id_l = []
        href_l = []
        for l in data['body']['illustManga']['data']:
            id = l['id']
            href = l['url']
            id_l.append(id)
            href_l.append(href)
        return id_l,href_l
    except Exception as e:
        print(f'获取第{i}页图片链接失败:{e}')
        return [],[]
def save(id_l,href_l,headers,pbar):
    for i in range(len(href_l)):
        r = requests.get(href_l[i],headers=headers)
        with open(f'out/test3/{id_l[i]}.jpg','wb') as f:
            f.write(r.content)
        pbar.update(1) #保存一张，更新进度条
def solve(i,tag,headers,pbar):
    id_l,href_l = get_href_l(i,tag,headers)
    if id_l and href_l:
        save(id_l,href_l,headers,pbar)
    else:
        print(f'第{i}页下载失败')
def main():
    tag = input("请输入搜索词:")
    cookie = input("请输入cookie:")
    #url编码
    tag = urllib.parse.quote(tag,encoding='utf-8')
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Referer':f'https://www.pixiv.net/tags/{tag}/artworks',
        'Cookie':f'{cookie}',
        'sec-ch-ua':'"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile':'?0',
        'sec-ch-ua-platform':'"Windows"',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site':'same-origin',
        'sec-fetch-user':'?1',
        'x-user-id':'82652303',
    }
    #创建线程池
    pool = ThreadPoolExecutor(max_workers=12)
    
    futures = []
    for i in range(1,500+1):
        pbar = tqdm(total=60,desc=f'第{i}页下载进度',unit='张') #进度条
        future = pool.submit(solve,i,tag,headers,pbar)
        time.sleep(10) #防止访问过快
    #等待所有任务完成
    for future in futures:
        future.result()

if __name__ == '__main__':
    main()