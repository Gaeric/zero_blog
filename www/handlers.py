#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zero'

"""
the Handle for Url
"""

from web_frame import get

@get('/')
async def index(request):
    # comment at step 1 Because db is not connected.
    # users = await User.findAll()
    # users = [{'id': '00156096303815290984ac46eb14ee9b526236bebe527a7000', 'email': 'test&example.com', 'passwd': '1234567890', 'admin': 0, 'name': 'Test', 'image': 'about:blank', 'create_at': 1560963038.15254}, {'id': '001561392888624d59a85c17c6043aa9b9d0187e4cedb2c000', 'email': 'nobody@example.com', 'passwd': 'nobody', 'admin': 0, 'name': 'nobody', 'image': 'about:nobody', 'create_at': 1561392888.62402}]
    users = "Hello, world!"

    # return {
    #     '__template__': 'test.html',
    #     'users': users
    # }

    return users
