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

from web_frame import add_static, add_routes
