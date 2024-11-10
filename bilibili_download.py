import asyncio
from bilibili_api import video, Credential, HEADERS
import httpx
import ffmpeg
from moviepy.editor import VideoFileClip, AudioFileClip

import re
import os

SESSDATA = ""
BILI_JCT = ""
BUVID3 = ""

# FFMPEG 路径，查看：http://ffmpeg.org/
FFMPEG_PATH = "ffmpeg"

def get_video_id(video_url):
    match = re.search(r'BV\w+', video_url)
    bvid = match.group(0)
    if not bvid:
        return -1
    return bvid

async def download_url(url: str, out: str, info: str):
    # 下载函数
    async with httpx.AsyncClient(headers=HEADERS) as sess:
        resp = await sess.get(url)
        length = resp.headers.get('content-length')
        with open(out, 'wb') as f:
            process = 0
            for chunk in resp.iter_bytes(1024):
                if not chunk:
                    break

                process += len(chunk)
                print(f'下载 {info} {process} / {length}')
                f.write(chunk)

async def download_bilibili_video(video_url, action):
    bvid = get_video_id(video_url)
    # 如果没有找到bvid，则返回-1
    if bvid == -1:
        return -1
    # 建立video物件
    credential = Credential(sessdata=SESSDATA, bili_jct=BILI_JCT, buvid3=BUVID3)
    videoObject = video.Video(bvid=bvid, credential=credential)
    info = await videoObject.get_info()
    
    author = info['owner']['name']
    view_count = info['stat']['view']
    title = info['title']

    # 正則表達式過濾非法字符
    illegal_chars = r'[\\/:*?"<>|]'
    # 使用 re.sub 替换非法字符为单个空格
    sanitized_title = re.sub(illegal_chars, ' ', title)
    # 替换多个连续的空格为单个空格
    sanitized_title = re.sub(r'\s+', ' ', sanitized_title)
    # 去掉开头和结尾的空格（可选）
    sanitized_title = sanitized_title.strip()
    video_title = sanitized_title

    if action == 'downloadVideo':
        filename = video_title + '.mp4'
        # 获取视频下载链接
        download_url_data = await videoObject.get_download_url(0)
        # 解析视频下载信息
        detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
        streams = detecter.detect_best_streams()
        # MP4 流下载
        await download_url(streams[0].url, "video/video_temp.m4s", "视频流")
        await download_url(streams[1].url, "video/audio_temp.m4s", "音频流")
        
        try:
            # 載入視頻和音頻文件
            video_clip = VideoFileClip("video/video_temp.m4s")
            audio_clip = AudioFileClip("video/audio_temp.m4s")

            # 將音頻附加到視頻上
            video_clip = video_clip.set_audio(audio_clip)

            # 輸出為 MP4 文件
            video_clip.write_videofile("video/" + filename, codec="libx264", audio_codec="aac")

            print(f"合并完成: {filename}")
        except ffmpeg.Error as e:
            print(f"合并失败: {e}")
        # 删除临时文件
        os.remove("video/video_temp.m4s")
        os.remove("video/audio_temp.m4s")

    elif action == 'downloadAudio':
        filename = video_title + '.mp3'
        # 获取视频下载链接
        download_url_data = await videoObject.get_download_url(0)
        # 解析视频下载信息
        detecter = video.VideoDownloadURLDataDetecter(data=download_url_data)
        streams = detecter.detect_best_streams()
        # MP4 流下载
        await download_url(streams[1].url, "video/audio_temp.m4s", "音频流")

        try:
            # 載入音頻文件
            audio_clip = AudioFileClip("video/audio_temp.m4s")

            # 輸出為 MP3 文件
            audio_clip.write_audiofile("video/" + filename, codec="libmp3lame")

            print(f"合并完成: {filename}")
        except ffmpeg.Error as e:
            print(f"合并失败: {e}")
        # 删除临时文件
        os.remove("video/audio_temp.m4s")

    return video_title, author, view_count, filename

    

# asyncio.run(download_bilibili_video("https://www.bilibili.com/video/BV1hktDesEH4/?spm_id_from=333.999.0.0", "audio"))