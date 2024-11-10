import yt_dlp
import asyncio
from moviepy.editor import VideoFileClip, AudioFileClip

import re
import os

# from db import update_data

def is_number(s=""):
    try:
        s = int(s[:-1])
        return s
    except Exception as e:
        return -1

async def download_youtube_video(video_url, action):
    ydl_opts = {
        'quiet': True,
        'skip_download': True, # 不下載影片，只擷取信息
        'noplaylist': True, # 不下載整個播放清單
    }

    # 取得影片信息，並創造一個新的Youtube物件
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        # 用這個物件的功能，取得影片的標題、觀看數、作者等資訊
        title = info_dict.get('title', None)
        view_count = info_dict.get('view_count', None)
        author = info_dict.get('uploader', None)

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
        ydl_opts_v = {
            'format': 'bestvideo',  # 下載最佳音訊
            'no-post-overwrites': True,  # 避免後處理
            'no-ffmpeg': True,  # 不使用 ffmpeg
            'outtmpl': 'video/video_temp.m4s', # 設定下載路徑
        }
        ydl_opts_a = {
            'format': 'bestaudio',  # 下載最佳音訊
            'extractaudio': True,   # 提取音訊
            'audio-quality': '0',   # 最佳音質
            'no-post-overwrites': True,  # 避免後處理
            'no-ffmpeg': True,  # 不使用 ffmpeg
            'outtmpl': 'video/audio_temp.m4s', # 設定下載路徑
        }
        try:
            # 取得影片信息，並創造一個新的Youtube物件
            with yt_dlp.YoutubeDL(ydl_opts_v) as ydl:
                ydl.download([video_url])
            with yt_dlp.YoutubeDL(ydl_opts_a) as ydl:
                ydl.download([video_url])

            # 載入視頻和音頻文件
            video_clip = VideoFileClip("video/video_temp.m4s")
            audio_clip = AudioFileClip("video/audio_temp.m4s")

            # 將音頻附加到視頻上
            video_clip = video_clip.set_audio(audio_clip)

            # 輸出為 MP4 文件
            video_clip.write_videofile("video/" + filename, codec="libx264", audio_codec="aac")

            print(f"合并完成: {filename}")
        except Exception as e:
            print(f"Error: {e}")
        # 删除临时文件
        os.remove("video/video_temp.m4s")
        os.remove("video/audio_temp.m4s")

    elif action == 'downloadAudio':
        filename = video_title + '.mp3'
        ydl_opts = {
            'format': 'bestaudio',  # 下載最佳音訊
            'extractaudio': True,   # 提取音訊
            'audio-quality': '0',   # 最佳音質
            'no-post-overwrites': True,  # 避免後處理
            'no-ffmpeg': True,  # 不使用 ffmpeg
            'outtmpl': 'video/audio_temp.m4s', # 設定下載路徑
        }
        try:
            # 取得影片信息，並創造一個新的Youtube物件
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # 載入音頻文件
            audio_clip = AudioFileClip("video/audio_temp.m4s")

            # 輸出為 MP3 文件
            audio_clip.write_audiofile("video/" + filename, codec="libmp3lame")

            print(f"轉檔完成: {filename}")
        except Exception as e:
            print(f"Error: {e}")
        os.remove("video/audio_temp.m4s")

    return video_title, author, view_count, filename

    
# asyncio.run(download_youtube_video('https://www.youtube.com/watch?v=yIkVTnt5kxs', 'downloadAudio'))