#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
由于搭建web框架需要定义装饰器，对装饰器的理解尚有些疑问，先做个review
"""

# 在使用装饰器之前可以前回顾闭包的知识

# 闭包：在一个外部函数中定义内部函数，这个外部函数返回内部函数，
# 且这个内部函数可以引用外部函数中的参数和局部变量；
# 当外部函数返回内部函数时，相关的参数和变量都保存在返回的函数中，这种程序结构为闭包。
# 如下什示例：
def count():
    fs = []
    for i in range(1, 4):
        # 在循环的过程中这个函数实脚被定义了三次
        def f():
            # 这个函数引用了外部变量i，它返回的是外部变量i的平方
            return i * i
        fs.append(f)
    return fs

# 运行count，可得： [<function count.<locals>.f at 0x7f00b46d80d0>, <function count.<locals>.f at 0x7f00b46d8158>, <function count.<locals>.f at 0x7f00b46d81e0>]
# 说明定义了三个函数
f1, f2, f3 = count()
#’执行可知f1 f2 f3得出的结果均为9

# 上面也可以换一种写法
def count():
    i = 0
    def f():
        return i * i
    fs = []
    for i in range(1, 4):
        fs.append(f)
        # fs.append(f()) 如果换成f()，那么每次处理的时候都会计算当前函数返回值，这个时候会得到[1, 4, 9]
    return fs

#@ [<function count.<locals>.f at 0x7f00b46d80d0>, <function count.<locals>.f at 0x7f00b46d80d0>, <function count.<locals>.f at 0x7f00b46d80d0>]
#  同一个函数引用了三次
# 虽然可以得到相同的结果，但是实脚的处理过程仍有差别

# 不引用变量i，而是引用函数入参，可以达到另一种效果
def count():
    def f(i):
        def g():
            return i * i
        return g
    fs = []
    for i in range (1, 4):
        fs.append(f(i))
    return fs
# [<function count.<locals>.f.<locals>.g at 0x7f00b46d82f0>, <function count.<locals>.f.<locals>.g at 0x7f00b46d8048>, <function count.<locals>.f.<locals>.g at 0x7f00b46d8378>]
# 因为参数i发生了变化，f(i)被引用了三次，这时返回了三个g，
# >>> f1, f2, f3 = count()
# >>> f1.__name__ , f2.__name__, f3.__name__
# ('g', 'g', 'g')

# 因为g引用了函数f的入参i，但是入参i在函数调用时已经确定，所以其执行结果为[1, 4, 9]’
# >>> f1(), f2(), f3()
# (1, 4, 9)

# 下面来理解装饰
# https://foofish.net/python-decorator.html
# 所谓装饰器，就是在不改变原有函数定义和功能的前提下，为函数增加功能的方法
# 我们的需求至始至终都是：增加这个函数的功能

# 装饰器本质上是一个 Python 函数或类，它可以让其他函数或类在不需要做任何代码修改的前提下增加额外功能，装饰器的返回值也是一个函数/类对象。
# 它常用于有切面需求的场景，比如：插入日志、性能测试、事务处理、缓存、权限校验等场景，装饰器是解决这类问题的绝佳设计。有了装饰器，我们就可以抽离出大量与函数功能本身无关的雷同代码到装饰器中并继续重用

# 以增加日志作为我们的需求
# 假设有一个正常的功能函数bar，我们需要在其调用前后加上日志

def bar():
    print('Ok, everything is well')

# 现在我们要为bar前后加上日志，但是我们又不想改变bar本身的逻辑，那么我们定义一个返回函数的函数
def log(func):
    print('%s is running' % func.__name__)
    return func

# 显然，我们现在可以使用log(bar)增加bar的日志，同时只需要将log(bar)的返回值赋给bar，就可以让bar向以前一样运行
# 我们会考虑到，因为目前的log函数调用时就会直接打印，然后返回了要装饰的函数本身，这个函数本身没有得到增强，不合要求
# 我们期望返回经过装饰的函数，原函数的所有功能不变，但是有些新增的东西
# 让我们重写log
def log(func):
    # 这一次我们返回装饰后的函数，替代掉原函数
    def wrapper():
        print('%s is running' % func.__name__)
        return func() # 这里返回的是函数调用，如果返回函数func，那么和上面的情况就类似，没有做到修饰func的效果
    return wrapper

bar = log(bar)
bar()

# 现在log是一个最简单的装饰器了，我们用返回的函数wrapper替代掉了func，调用wrapper()的时候，我们期望增加的信息会打印，func()也会运行；但是要注意，现在运行的函数其实已经变成了：wrapper

# >>> bar = log(bar)
# >>> bar.__name__
# 'wrapper'


# 那么，接下来，如果func带了参数呢？
def bar(name):
    print("hello, %s" % name)

def log(func):
    # 加一个参数
    def wrapper(name):
        print("%s is running" % func.__name__)
        return func(name)
    return wrapper

# >>> bar = log(bar)
# >>> bar('zero')
# bar is running
# hello, zero
# >>>

# 装饰函数也许需要重用呢，参数的数量和类型也许不固定呢，我们知道(*args, **kw)可以接受所有参数
# 则定义装饰函数如下：
def log(func):
    # 任意参数
    def wrapper(*args, **kw):
        print('%s is running' % func.__name__)
        return func(*args, **kw)
    return wrapper

# 如果装饰函数需要带参数呢
def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print("%s: %s is running" % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator

# 运行结果如下：
# >>> log_d = log('log_level')
# >>> bar = log_d(bar)
# >>> bar('zero')
# log_level: bar is running
# hello, zero
# >>>

# 等效结果
# >>> bar = (log("log_level"))(bar) # 不是lisp，加个括号不要紧 :)
# >>> bar('zero')
# log_level: bar is running
# hello, zero

# 但是它还有一个问题：
# 因为调用的实际不是原来的函数，bar的元信息发生了变化，Python内置的functools.wraps解决这个问题
import functools

def log(func):
    # 任意参数
    @functools.wraps # 将func的信息传递给了被装饰的wrapper
    def wrapper(*args, **kw):
        print('%s is running' % func.__name__)
        return func(*args, **kw)
    return wrapper

def log(text):
    def decorator(func):
        @functools.wraps # 因为最后取代func运行的实际是wrapper，故在这里装饰
        def wrapper(*args, **kw):
            print("%s: %s is running" % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


# >>> bar.__name__
# 'wrapper'
# >>>




# @ 语法糖不用解释
# 在定义函数bar时 @ 装饰函数即可
