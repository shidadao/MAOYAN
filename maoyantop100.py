import json
from multiprocessing.pool import Pool

import requests
from requests.exceptions import RequestException
import re

def get_one_page(url):
    try:
        headers = {

            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
            'Cookie':'uuid=1A6E888B4A4B29B16FBA1299108DBE9CE9A5938E4519F96D55C9E0BBF6E2EDE7; _csrf=d7f70585a1bc5f83d3393851765c363b531c3430bfb72c14112a19a6dbd1d56c; _lxsdk_cuid=163f35c947cc8-0f6b1c3df4dfd4-b34356b-144000-163f35c947cc8; _lxsdk=1A6E888B4A4B29B16FBA1299108DBE9CE9A5938E4519F96D55C9E0BBF6E2EDE7; __mta=156627844.1528796320980.1528796511712.1528797426156.4; _lxsdk_s=163f35c947d-af5-6b9-a49%7C%7C8'
        }
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'scroe': item[5]+item[6]

        }

def write_to_file(content):

    with open('result.text', 'a', encoding='utf8') as f:

        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])#多线程的用法，否则就是直接(main,rang(10))
    pool.close()
    pool.join()#只要有pool.map就有这行
