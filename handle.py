
from aiohttp import web
import urllib

import json
import re
import os

from bilibili_download import download_bilibili_video
from youtube_download import download_youtube_video
from db import insert_data, delete_all ,delete_one

async def handle_video_download(request):
    # 解析请求参数
    try:
        data = await request.json()
        url = data.get('downloadUrl')
        action = data.get('action')
        filename = ""

        # 判斷用什麼方式下載(bilibili/youtube)
        if (re.match('bilibili', url)):
            # 下載bilibili影片
            video_title, author, view_count, filename = await download_bilibili_video(url, action)
            insert_data(video_title, author, view_count)
            pass
        else:
            # 下載youtube影片
            video_title, author, view_count, filename = await download_youtube_video(url, action)
            insert_data(video_title, author, view_count)
            pass

        # 对文件名进行 URL 编码
        encoded_filename = urllib.parse.quote(filename)  # URL 编码：'你好.mp3' -> '%E4%BD%A0%E5%A5%BD.mp3'

        # 设置下载文件名稱
        return web.FileResponse("video/"+filename, headers={
            'Content-Disposition': f'attachment; filename*=UTF-8\'\'{encoded_filename}'
        })
        # return web.json_response({
        #     "filename": filename,
        #     "file_url": "video/" + filename  # 提供文件的 URL，前端可以直接下载
        # })

    except:
        return json.dumps({'error': 'Invalid request format'})
    
async def handle_delete_all(request):
    # 指定目錄路徑
    video_dir = 'video/'

    # 列出目錄中的所有文件並刪除
    for filename in os.listdir(video_dir):
        file_path = os.path.join(video_dir, filename)
        if os.path.isfile(file_path):  # 確保是文件而非目錄
            os.remove(file_path)  # 刪除文件
            
    delete_all()
    return web.json_response({'message': 'All data deleted successfully'})

async def handle_delete_one(request):
    try:
        data = await request.json()
        id = data.get('id')
        delete_one(id)
        return web.json_response({'message': 'All data deleted successfully'})
    except:
        return json.dumps({'error': 'Invalid request format'})