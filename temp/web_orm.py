#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orm for Mysql
"""

import requests
import os
import time
import logging
import json
import asyncio
from aiohttp import web
import aiomysql

logging.basicConfig(level=logging.INFO)

# 建立连接池，带入可选关键字参数，方便使用配置文件进行定制
async def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('prot', 3306),
        password=kw['password'], # 竟然忘了获取密码
        user=kw.get('user', 'root'),
        db=kw.get('db', 'db'),
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop)


# 数据库 select 函数，从连接池中获取连接并查询内容
# 成功返回查询结果集 rs 并关闭 cursor
async def select(sql, args, size=None):
    #TODO 不清楚作用的语句注释保留，查明后删除或批注
    # log(sql, args)
    global __pool
    with (await __pool) as conn:
        # conn 和 cursor是pymysql的标准用法
        cur = await conn.cursor(aiomysql.DictCursor)
        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs


# 数据库 Insert、delete、update 通用函数
# 从连接池中获取连接创建cursor执行相应操作，完成操作后关闭连接
# 成功返回操作的行数'affected'，失败抛异常
async def execute(sql, args):
    #TODO 不清楚作用的语句注释保留，查明后删除或批注
    # log(sql)
    with (await __pool) as conn:
        try:
            cur = await conn.cursor()
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
        except BaseException:
            raise
        return affected

# 下面定义orm
# 注意orm是对象关系映射，其中用到了metaclass相关的方法
# 以用户视角，从上层调用角度考虑orm的调用方法，有助于理解其中的设计概念

# 首先，我们要将数据库的一张表和一个类联系起来，直接操作对象，而不是拼接sql语句
# 假设一张user表，它有两个字段，第一个字段是id，第二个字段是name；
# id字段是整型，且是这张表的主键
# 而name字段是字符串型
# 这个表可以做出常规的增删改查

# 我们需要设计一个class为User
# 那么首先User会有两个属性，代表其两个字段，分别为id和name
# 其中id为整型，且是这张表的主键
# 而name为字符串型
# User有增删改查四种方法，可以对数据进行操作

# User只是众多表中的一张，但是其余的表有基本相似的结构
# 一张表有多个字段，每个字段有其属性，表本身能够增删改查
# 为了便于复用，于是定义出的通用的Model

# 预设orm及调用方法
# from orm import Model, StringField, IntegerField
#
# class User(Model):
#     __table__ = 'users'
#     # 表名为users，其中有两个字段
#     # 第一个字段为id，自增id，字段的属性为integer
#     # 第二个字段为name，是用户名，字段属性为string
#     id = IntegerField(primary=True)
#     name = StringField()
#
# # 其调用方法如下：
# # 创建实例
# user = User(id=2, name='zero')
# # 插入数据库
# user.insert()
# # 查询所有User对象
# users=User.findAll()

# 实际定义orm

# 根据我们对orm的设想，User的定义和调用如下：
# 导入Model做为User的基类，StringField和IntegerField定义字段的属性
# comment from orm import Model, StringField, IntegerField
# comment
# comment # 首先User继承自Model
# comment class User(Model):
# comment     # 对应的数据库表为users表
# comment     __talbe__ = 'users'
# comment     # 第一个字段为id，属性为整型， 且其为主键
# comment     id = IntegerField(primary_key=True)
# comment     # 第二个字段为name，属性为字符串型
# comment     name = StringField()
# comment
# comment # 其使用方法如下：
# comment user = User(id=2, name='zero')
# comment # 插入和查询对所有表通用，则定义在Model中
# comment user.insert()
# comment users=User.findAll()

# 首先定义Field
# 类可以起到模板的作用，使用__init__方法将部分属性强制绑定
# Field是StringField和IntegerField的基类，其继承制object
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        # 字段名称、字段类型、自段是否为主键是一个字段的基本属性
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)

# field_a = Field(name = 'test', column_type='int', primary_key=False, default=None)

# 根据Field定义出各种属性
# 诸如：StringField BooleanField IntegerField FloatField TextField
# 默认参数的定义和使用，及其注意事项
class StringField(Field):
    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

class IntegerField(Field):
    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class FloatField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)

class TextField(Field):
    def __init__(self, name=None, default=None):
        super().__init__(name, 'text', False, default)

# boolean不可能是主键
class BooleanField(Field):
    def __init__(self, name=None, default=False):
        super().__init__(name, 'bool', None, default)

# metaclass定义元类
class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):

        if name == 'Model': # 这里跳过对Model这个类的修改，当类为Model时，直接由type创建
            return type.__new__(cls, name, bases, attrs)

        tableName = attrs.get('__table__', None) or name # 获取表名，如果没有__table__字段，则定义为class的name
        logging.info('found model: %s (table: %s)' % (name, tableName))

        mappings = dict()
        fields = []
        primaryKey = None
        for k, v in attrs.items():
            if isinstance(v, Field):
                # 已存在的映射关系
                logging.info('  found mapping: %s ==> %s' % (k, v))
                # 所有的映射关系都存储在mappings列表中
                mappings[k] = v
                if v.primary_key:
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    # 将映射关系分为了主键primary_key和fields
                    fields.append(k)

        if not primaryKey:
            raise RuntimeError('Primary key not found.')
        for k in mappings.keys():
            # 从类属性中删除mappings中存在的映射属性，避免出现运行时错误
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ','.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ','.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ','.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOfDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('usign defalut value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    async def find(cls, pk):
        '''find object by primary key.'''
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        # conn.cursor(aiomysql.DictCursor)返回结果为字典
        return cls(**rs[0])

    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        '''Find objects by where clause.'''
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append("?, ?")
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        '''find number by select and where'''
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            args.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 因为我们从创建了orm，每个User的实例都对应着sql中的一行数据，
    # 如果要增加、删除或修改这条数据，只需要对这个实例进行操作即可，方法的对系为user这个实例
    # 但如果要进行查询，则必须对这个库中的内容进行搜索，方法的对象为User这个class

    async def save(self):
        args = list(map(self.getValueOfDefault, self.__fields__))
        args.append(self.getValueOfDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)
