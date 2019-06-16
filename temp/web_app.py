#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搭建Web-App骨架
由于过程中有warning，最终参考aiohttp下的lowlevel_srv.py
"""
import os
import time
import json
import logging
import asyncio
from datetime import datetime
from aiohttp import web

# 注意logging模块中可能会有部分Message，不要随意改写Format
logging.basicConfig(level=logging.INFO)

# async/await 使用协程，编写异步应用的推荐方式
async def index(request):
    # Add content_type
    return web.Response(body='<h1>zero\'s Blog</h1>'.encode('utf-8'), content_type='text/html')


async def init(loop):
    server = web.Server(index)
    srv = await loop.create_server(server, '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000 ...')
    return srv


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(init(loop))
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
