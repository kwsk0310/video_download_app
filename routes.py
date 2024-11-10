from aiohttp import web

async def index(request):
    # 這裡對應 Flask 中的路由處理
    return web.Response(text="Hello, Aiohttp!")

def setup_routes(app):
    # 註冊路由
    app.router.add_get('/', index)