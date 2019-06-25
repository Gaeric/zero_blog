#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zero'

'''
A async web application
'''

import logging
import asyncio
import os
import time

from datetime import datetime
from aiohttp import web

from web_frame import add_routes

logging.basicConfig(level=logging.DEBUG)

async def logger_factory(app, handler):
    async def logger(request):
        logging.info(f'Request: {request.method} {request.path}')
        return (await handler(request))
    return logger

async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info(f'request json: {str(request.__data__)}')
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info(f'request form: {str(request.__data__)}')
        return (await handler(request))
    return parse_data

async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, defalut=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
        else:
            # app['__templateing__'] 是用于jinja2模板的方法
            # resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
            template = r
            logging.info(f'Template of Response is: {template}')
            resp = web.Response(body=template.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t > 100 and t < 600:
                return web.Response(t, str(m))
        # default
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        logging.inof("Response handler end.")
        return resp
    return response


# 首先建立一个web server服务器
# 然后导入路由和URL处理函数，对请求进行响应

async def init():
    "Build web app"
    app = web.Application(middlewares=[
        logger_factory, response_factory
    ])

    # 添加路由
    add_routes(app, 'handlers')

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 9000)
    logging.info('server started at http: //127.0.0.1:9000...')
    await site.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()
