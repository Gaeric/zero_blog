#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
这里我们来写一个基于aiohttp的web框架
一个web框架应该干什么呢？
就目前来得，它应该能够接收请求(request)
解析请求并处理
然后进行响应(response)
"""

# 我们现从使用者的角度看看具体要做什么
async def handle_url_xxx(request):
    """异步处理请求的函数"""
    pass

# 传入参数从request获取
url_param = request.match_info['key']
query_params = parse_qs(request.query_strng)

# 构造reponse
text = render('template', data)
return web.Response(text.encode('utf-8'))

# 那我们设定框架，可以处理但带参数的URL：
@get('/blog/{id}')
def get_blog(id):
    """..."""
    pass

# 处理query_string参数(通过**kw或命名关键字参数接随):
@get('/api/comments')
def api_comments(*, page='1'):
    pass

# 返回模板
return {
    '__template__': 'index.html',
    'data': '...'
}

# 定义装饰器get
import functools
import asyncio
import inspect
import logging

# 定义装饰器get
def get(path):
    """Define decorator @get('/path')"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

# DONE: PASS
@get('zero')
def hello(name):
    print('hello, %s' % name)

# 定义装饰器post
def post(path):
    """ Define decorator @post('/path') """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

# DONE: PASS
@post('zaeric')
def overtime(time):
    print('overtime: %s' % time)

# 定义RequestHandler

class RequestHandler(object):
    def __init__(self, app, fn):
        self._app = app
        self._fuc = fn
        ...

    async def __call__(self, request):
        kw = ... # 获取参数
        r = await self._func(**kw)
        return r

def add_route(app, fn):
    method = getattr(fn, '__mehtod__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    # inspect.signature（fn)： 返回一个inspect.Signature类型的对象，值为fn这个函数的所有参数
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
    logging.info('add route %s %s ==> %s(%s)' % (method, path, fn.__name__, ', '.join(inspect.signature(fn).parameters.keys())))
    app.router.add_route(method, path, RequestHandler(app, fn))

add_route(app, handles.index)
add_route(app, handles.blog)
add_route(app, handles.create_comment)

# 自动扫描的写法
add_routes(app, 'handles')

def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n+1:]
        mod = getattr(__import__(model_name[:n], globals(), locals(), [name]), name)

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)

app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])

init_jinja2(app, filters=dict(datetime=datetime_filter))
add_routes(app, 'handlers')
add_static(app)

# middleware是一个拦截器，一个URL在被处理之前，可以经过一系列的middleware处理
async def logger_factory(app, handler):
    async def logger(request):
        # 记录日志
        logging.info('Request: %s %s' % (requests.method, request.path))
        # 处理请求
        return (await handler(request))
    return logger

async def response_factory(app, handler):
    async def response(requests):
        # result
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            ...
