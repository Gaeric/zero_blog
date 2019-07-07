#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zero'

"""
the Handle for Url
"""

import time
import logging
import re
import hashlib
import json

from aiohttp import web

from web_frame import get
from web_frame import post
from models import next_id
from models import User
from models import Blog
from apis import APIValueError
from apis import APIError

COOKIE_NAME = 'zerosession'
_COOKIE_KEY = 'some_key'

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    expires = str(int(time.time() + max_age))
    s = f'{user.id}-{user.passwd}-{expires}-{_COOKIE_KEY}'
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

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

@get('/api/users')
async def api_get_users():
    # 数据库和前面的models的定义中这个字段是create_at
    users = await User.findAll(orderBy='create_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)

# {}用于匹配指定次数时，中间绝对不能出现空格
email_regex = re.compile(r'''(
^
([a-zA-Z0-9._%+_]+) # username
(@)                 # symbol
([a-zA-Z0-9-.]+)    # domain name
(\.[a-zA-Z]{2,4})    # 不能带空格 切记
$
)
''', re.VERBOSE)

sha1_regex = re.compile(r'^[0-9a-f]{40}$')

@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not email_regex.match(email):
        raise APIValueError('email')
    if not passwd or not sha1_regex.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = f'{uid}:{passwd}'
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
                # image='http://www.gravatar.com/avatar/%s?d=mm&s=120'
               image = 'some_info :%s' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid eamil.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exists.')
    user = users[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

async def auth_factory(app, handler):
    async def auth(request):
        logging.info(f'check User: {request.method} {request.path}')
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info(f'set current user: {user.email}')
                request.__user__ = user
        return await handler(request)
    return auth

async def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = f'{uid}-{user.passwd}-{expires}-{_COOKIE_KEY}'
        if sha1 != hashlib.sha1(s.encode('utf-8').hexdigest()):
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }
