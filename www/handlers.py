#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zero'

"""
the Handle for Url
"""

import time
import logging

from web_frame import get
from models import User
from models import Blog

@get('/')
async def index(request):
    # Test the server work well.
    # users = await User.findAll()
    # users = [{'id': '00156096303815290984ac46eb14ee9b526236bebe527a7000', 'email': 'test&example.com', 'passwd': '1234567890', 'admin': 0, 'name': 'Test', 'image': 'about:blank', 'create_at': 1560963038.15254}, {'id': '001561392888624d59a85c17c6043aa9b9d0187e4cedb2c000', 'email': 'nobody@example.com', 'passwd': 'nobody', 'admin': 0, 'name': 'nobody', 'image': 'about:nobody', 'create_at': 1561392888.62402}]

    return {
        # '__template__': 'test.html',
        '__template__': '__base__.html'
        # 'users': users
    }

@get('/blog/readme')
async def readme(request):
    return {
        '__template__': 'readme.html'
    }

@get('/blog')
def blog(request):
    summary = "Build world setp by setp"
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Python', summary=summary, created_at=time.time()-7200)
    ]

    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }
