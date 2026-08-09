class Logger:
    def log(*args, **kwargs):
        print(*args, **kwargs)


def log(*args, **kwargs):
    Logger.log(*args, **kwargs)