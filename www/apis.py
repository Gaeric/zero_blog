#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class APIError(Exception):
    '''the base APIError which contains error(required), data(optional) and
    message(optional).'''
    def __init__(self, error, data='', message=''):
        supper().__init__(message)
        self.error = error
        self.data = data
        self.message = message

