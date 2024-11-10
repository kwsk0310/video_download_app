from aiohttp import web
import aiohttp_jinja2
import jinja2

from handle import handle_video_download, handle_delete_all, handle_delete_one
from db import get_data

# 設置模板目錄
async def index(request):
    videos = get_data()

    # 建立一個字典，包含要傳遞給模板的數據
    context = { 'videos' : videos }
    return aiohttp_jinja2.render_template('index.html', request, context)

# 設定靜態檔案路由
async def static(request):
    return web.FileResponse(f'static/{request.match_info["filename"]}')

# 建立應用
app = web.Application()

# 設定 Jinja2 模板引擎
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

# 設定路由
app.router.add_get('/', index)  # 根路由會渲染 index.html

app.router.add_static('/static', path='static', name='static')  # 設定靜態檔案路由

app.router.add_post('/api/download', handle_video_download)

app.router.add_post('/api/delete_all', handle_delete_all)

app.router.add_post('/api/delete_one', handle_delete_one)

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8080)