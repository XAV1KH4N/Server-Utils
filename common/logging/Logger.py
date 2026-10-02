import time

class Logger:

    Show_time = False

    def logInfo(self, *args, **kwargs) -> None:
        self.__log("INFO", *args, **kwargs)

    def logWarning(self, *args, **kwargs) -> None:
        self.__log("WARN", *args, **kwargs)

    def logError(self, *args, **kwargs) -> None:
        self.__log("ERROR", *args, **kwargs)

    def logDebug(self, *args, **kwargs) -> None:
        self.__log("DEBUG", *args, **kwargs)

    def __log(self, level, *args, **kwargs) -> None:
        local = time.localtime()
        time_str = ""
        if (Logger.Show_time):
            time_str = f" {local.tm_hour}:{local.tm_min}:{local.tm_sec}"
        print(f"[{level}]{time_str} - [{self.__class__.__name__}]", *args, **kwargs)
