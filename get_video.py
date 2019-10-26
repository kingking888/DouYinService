#coding:utf-8
'''
    author:linkin
    date:2019-10-24
    github:www.github.com/01ly
    info:通过 视频ID 或者分享链接 获取 无水印视频 下载链接 及视频信息
'''

import requests


def get_video(api,url=None,vid=None,json=True):
	params ={
		'url':url,
		'vid':vid,
	}
	response = requests.get(api,params=params)
	data = response.json() if json else response.text 
	return data


if __name__ == '__main__':

	# 接口
	api_base = 'http://api.linkin.site/FlaskDY'
	video_info_api = f'{api_base}/video'
	nowatermark_video_api = f'{api_base}/video/v1'

	# 示例
	# 抖音视频分享的短链接
	video_share_url = 'http://v.douyin.com/9nwexQ/'
	# 抖音视频aweme_id 
	video_id = '6589060762247892237'

	# 模拟手机 浏览器头部
	headers = {
		'user-agent':'Mozilla/5.0 (iPhone 84; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.0 MQQBrowser/7.8.0 Mobile/14G60 Safari/8536.25 MttCustomUA/2 QBWebViewType/1 WKType/1',
	}

	# 1. 只使用 分享链接
	# 获取视频信息
	data = get_video(video_info_api,url=video_share_url)
	print(f'获取到的视频分享链接为{video_share_url} 的视频信息:\n{data}\n')
	# 获取无水印视频链接
	n_url = get_video(nowatermark_video_api,url=video_share_url,json=False)
	print(f'获取到的视频分享链接为{video_share_url} 的无水印视频链接为:\n{n_url}\n')

	# 2. 只使用 视频id
	# 获取视频信息
	data = get_video(video_info_api,vid=video_id)
	print(f'获取到的 视频aweme_id为{video_id} 的视频信息:\n{data}\n')
	# 获取无水印视频链接
	n_url = get_video(nowatermark_video_api,vid=video_id,json=False)
	print(f'获取到的视频分享链接为{video_share_url} 的无水印视频链接为:\n{n_url}\n')

	# 3.下载无水印视频
	share_url = 'http://v.douyin.com/x1y5Gw/'
	n_url = get_video(nowatermark_video_api,url=share_url,json=False)
	response = requests.get(n_url,headers=headers)
	with open('demo.mp4','wb') as f:
		f.write(response.content)
	print(f'视频下载成功.')




