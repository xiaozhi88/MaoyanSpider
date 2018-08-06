import requests
import re
import json



def get_one_page(url):
    '''
    获取top100页面信息
    :param url: 页面链接
    :return: 页面源代码
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    '''
    解析页面所需信息
    :param html:页面源代码
    :return: 排名,图片,标题,主演,上映时间,评分
    '''
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }


def write_to_file(content):
    '''
    提取信息写入文件
    :param content: 返回的提取信息
    :return: 写入后的文件
    '''
    with open('result.txt','a',encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content,ensure_ascii=False) + '\n')


def main(offset):
    '''
    设置参数,运行爬虫
    :param offset:
    :return:
    '''
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    items = parse_one_page(html)
    for item in items:
        write_to_file(item)




if __name__ == '__main__':
    for i in range(10):
        main(i*10)