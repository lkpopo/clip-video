
import requests

# 提交剪辑请求
clip_request_data = {
    'video_url': 'http://vjs.zencdn.net/v/oceans.mp4',
    'start_time': '00:00:10',
    'end_time': '00:00:20'
}
response = requests.post('http://localhost:5000/submit-clip-request', json=clip_request_data)
clip_request_url = response.json()['clip_request_url']

print('----',clip_request_url)

# 发送GET请求触发剪辑
response = requests.get(clip_request_url)
clipped_video_url = response.json()['clipped_video_url']
print("Clipped video URL:", clipped_video_url)
