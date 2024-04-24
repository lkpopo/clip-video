from flask import Flask, request, jsonify
import requests
import os
import subprocess

app = Flask(__name__)

# 定义用户的token
valid_api_keys = ['Admin', 'Mr Zhang', 'Mr Zhou']
# 定义剪辑的进度. 0：正在剪辑，1：剪辑完成
Editing_Progress = 0


# 将视频下载服务器后进行剪辑
def download_video(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)


@app.route('/check-progress', methods=['POST'])
def check_progress():
    if Editing_Progress:
        return jsonify({'result': 'Editing complete!'})
    return jsonify({'result': 'Editing... ...'})


@app.route('/submit-clip-request', methods=['POST'])
def submit_clip_request():
    # 获取用户提交的数据
    data = request.json
    token = data.get('token')
    video_url = data['video_url']
    start_time = data['start_time']
    end_time = data['end_time']

    # 验证用户身份
    if token not in valid_api_keys:
        return jsonify({'error': 'Invalid User Token'}), 401

    # 生成剪辑请求的URL
    clip_request_url = f'http://localhost:5000/clip-video?video_url={video_url}&start_time={start_time}&end_time={end_time}'
    print("get video")
    return jsonify({'clip_request_url': clip_request_url})


@app.route('/clip-video', methods=['GET'])
def clip_video():
    # 获取剪辑请求的参数
    video_url = request.args.get('video_url')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    # 设置剪辑后视频的路径，方便用户进行下载
    output_file = 'static/clipped_video.mp4'
    if not os.path.exists('static'):
        os.makedirs('static')
    # 下载需要剪辑的视频
    download_video(video_url, 'temp_video.mp4')

    subprocess.run(
        ['ffmpeg', '-i', 'temp_video.mp4', '-ss', start_time, '-to', end_time, '-c:v', 'copy', '-c:a', 'copy',
         output_file], check=True)

    # 删除临时下载的视频文件
    os.remove('temp_video.mp4')

    # 返回剪辑后视频的URL
    clipped_video_url = f'/static/clipped_video.mp4'
    return jsonify({'clipped_video_url': 'http://localhost:5000' + clipped_video_url})


if __name__ == '__main__':
    app.run(debug=True)
