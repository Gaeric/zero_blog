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

logging.basicConfig(level=logging.DEBUG)

# 首先建立一个web server服务器
async def init():
    "Build web app"
    app = web.Application()

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 9000)
    logging.info('server started at http: //127.0.0.1:9000...')
    await site.start()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
loop.run_forever()
