import time

class Logger:

    def __init__(self):
        self.__show_time = False

    def log(*args, **kwargs):
        print(*args, **kwargs)

    def log2(clazz, *args, **kwargs):
        local = time.localtime()
        print(f"${local.tm_hour}:${local.tm_min}:${local.tm_sec} - [${clazz.__class__.__name__}]", *args, **kwargs)

    def log3(self, *args, **kwargs):
        local = time.localtime()
        print(f"${local.tm_hour}:${local.tm_min}:${local.tm_sec} - [${self.__class__.__name__}]", *args, **kwargs)

    def logInfo(self, *args, **kwargs) -> None:
        local = time.localtime()
        print(f"[INFO] {local.tm_hour}:{local.tm_min}:{local.tm_sec} - [{self.__class__.__name__}]", *args, **kwargs)

    def logWarning(self, *args, **kwargs) -> None:
        local = time.localtime()
        print(f"[WARN] {local.tm_hour}:{local.tm_min}:{local.tm_sec} - [{self.__class__.__name__}]", *args, **kwargs)


    def logError(self, *args, **kwargs) -> None:
        local = time.localtime()
        print(f"[ERROR] {local.tm_hour}:{local.tm_min}:{local.tm_sec} - [{self.__class__.__name__}]", *args, **kwargs)


    def logDebug(self, *args, **kwargs) -> None:
        local = time.localtime()
        print(f"[DEBUG] {local.tm_hour}:{local.tm_min}:{local.tm_sec} - [{self.__class__.__name__}]", *args, **kwargs)
        self.__log()

    def __log(self, level, *args, **kwargs) -> None:
        local = time.localtime()
        time_str = ""
        if (self.__show_time):
            f"{local.tm_hour}:{local.tm_min}:{local.tm_sec}"
        print(f"[{level}] {time_} - [{self.__class__.__name__}]", *args, **kwargs)
