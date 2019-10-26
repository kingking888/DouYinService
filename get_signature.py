#coding:utf-8
'''
    author:linkin
    date:2019-10-24
    github:www.github.com/01ly
    info:抖音js加密签名参数 _signature 的解密获取功能
'''

import requests,re

def get_matches_from_url_page(url,pattern,headers):
    res = requests.get(url,headers=headers)
    rel = re.findall(pattern,res.text)
    if rel:
        return rel[0]

if __name__ == "__main__":

    # signature 签名解密接口 nonce 为解密需要传入的参数 用户user_id 或者 视频aweme_id
    api = 'http://api.spiders.pub/FlaskDY/sign/{nonce}'

    headers = {
        'user-agent': 'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://www.iesdouyin.com/share/user/88445518961'
    }

    # 以下 params 参数的其他参数均可 通过访问页面解析 获取，此处只为测试 _signature 签名的有效性
    # 示例一
    # 获取热门视频5个，接口如下
    nonce = '6589060762247892237'  # 需要传入解密js函数的参数(有且只有一个)，可以是用户的user_id,或者是抖音视频的aweme_id,此处为视频aweme_id
    url = api.format(nonce=nonce)
    response = requests.get(url)
    sign = response.json().get('_signature')
    print(f'>> nonce为：{nonce}时，获取到 signature 解密值为：\n{sign}\n')
    
    example_api = 'https://www.iesdouyin.com/web/api/v2/aweme/hotlist/?'
    params = {
        'app_id':1128,  #固定值
        'cursor':0,     # 当前游标
        'count':5,      # 设置获取的视频个数
        'parent_rid':'20191024200659010155098157110CEB',    #获取到的parent_rid，需要解析页面获取
        'aweme_id':nonce,
        '_signature':sign,
        'whale_id':nonce,
    }
    print(f'请求参数:{params}')
    response = requests.get(example_api,headers=headers,params=params)
    print(f'>> 获取到的接口数据为：\n{response.json()}\n')

    # # 示例二
    # # 获取迪丽热巴 前20个抖音视频，接口如下
    nonce = '88445518961'  # 需要传入解密js函数的参数(有且只有一个)，此处为用户 user_id,不是抖音ID
    url = api.format(nonce=nonce)
    response_2 = requests.get(url)
    sign = response_2.json().get('_signature')
    print(f'>> nonce为：{nonce}时，获取到 signature 解密值为：\n{sign}\n')

    example_api = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?'
    user_api = 'https://www.iesdouyin.com/share/user/88445518961'
    params = {
        'user_id': nonce,
        'sec_uid':'',
        'count': 20,
        'max_cursor': 0,
        'aid': 1128,
        '_signature': sign,
        'dytk': get_matches_from_url_page(user_api,'dytk: \'(.+)\'',headers),
    }
    print(f'请求参数:{params}')
    while 1:
        response = requests.get(example_api, headers=headers, params=params)
        data = response.json()
        if data['aweme_list']:
            print(f'>> 获取到的接口数据为：\n{data}\n')
            break