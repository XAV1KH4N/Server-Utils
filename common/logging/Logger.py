import sys
import time, timeit

class Logger:
    def log(*args, **kwargs):
        print(*args, **kwargs)

    def log2(clazz, *args, **kwargs):
        local = time.localtime()
        print(f"${local.tm_hour}:${local.tm_min}:${local.tm_sec} - [${clazz.__class__.__name__}]", *args, **kwargs)

    def log3(self, *args, **kwargs):
        local = time.localtime()
        print(f"${local.tm_hour}:${local.tm_min}:${local.tm_sec} - [${self.__class__.__name__}]", *args, **kwargs)

def log(*args, **kwargs):
    Logger.log(*args, **kwargs)

def log2(clazz, *args, **kwargs):
    Logger.log(clazz, *args, **kwargs)