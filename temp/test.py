#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
# import aiomysql

import web_orm
from models import User, Blog, Comment

async def test(loop):
    #TODO 创建其它用户，并成功登录
    await web_orm.create_pool(user='root', password='********', db='zero_blog', loop=loop)

    u = User(name='Test', email='test&example.com', passwd='1234567890', image='about:blank')

    await u.save()

async def test_example(loop):
    pool = await aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='lantian123',
        db='zero_blog',
        loop=loop
    )

loop = asyncio.get_event_loop()
# loop.run_until_complete(test_example(loop))
loop.run_until_complete(test(loop))
