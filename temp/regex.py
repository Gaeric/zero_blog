#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

test = re.compile(r'([a-zA-Z0-9._%+-]+)(@)([a-zA-Z0-9-]+)([a-zA-Z0-9.]{2,4})')

email_regex = re.compile(r'''(
^
([a-zA-Z0-9._%+_]+) # username
(@)                 # symbol
([a-zA-Z0-9-.]+)    # domain name
(\.[a-zA-Z]{2,4})    # 不能带空格 切记
$
)
''', re.VERBOSE)

email_regex = re.compile(r'''(
^
[a-zA-Z0-9._%+-]+ # username 中括号中特殊字符不用转译
@                 # symbol
[a-zA-Z0-9.-]+    # domain name
(\.[a-zA-Z{2,4}])
$
)''', re.VERBOSE)

email_regex.match('1062217098@qq.com')


test_regex = re.compile(r'''(
[a-zA-Z0-9._%+-]+ # username 中括号中特殊字符不用转译
@                 # symbol
[a-zA-Z0-9.-]+    # domain name
(\.[a-zA-Z]{2,4})
)''', re.VERBOSE)

test_regex = re.compile(r'''(
([a-zA-Z0-9_%+-]+) # username 中括号中特殊字符不用转译
(@)                # symbol
([a-zA-Z0-9\.-]+)    # domain name
)''', re.VERBOSE)

test_regex.match('1062217098@qq.com').group(1)

(\.[a-zA-Z]{2, 4})

emailRegex = re.compile(r'''(
([a-zA-Z0-9_%+-]+) # username
@ # @ symbol
[a-zA-Z0-9.-]+ # domain name
(\.[a-zA-Z]{2,4}) # dot-something
)''', re.VERBOSE)

emailRegex.match('1062217098@qq.com').group(1)

test_regex = re.compile(r'([a-zA-Z0-9._%+-]+)(@)([a-zA-Z0-9.-]+)(.[a-zA-Z]{2,4})')
