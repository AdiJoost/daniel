from config.configManager import getConfig
from config.rootPath import getRootPath
from datetime import datetime
from log.logLevel import LogLevel

class Logger():
    logLevel = LogLevel[getConfig("logLevel")]
    chattyLevel = LogLevel[getConfig("chattyLevel")]

    def __init__(self, filename: str="application", loggerName: str="Logger") -> None:
        self.filename = filename
        self.loggerName = loggerName
        self.filepath = getRootPath().joinpath("log", f"{filename}.log")

    def debug(self, message) -> None:
        if LogLevel.DEBUG.value >= self.logLevel.value:
            self._log(message, "DEBUG")
        if LogLevel.DEBUG.value >= self.chattyLevel.value:
            print(message)

    def info(self, message) -> None:
        if LogLevel.INFO.value >= self.logLevel.value:
            self._log(message, "INFO")
        if LogLevel.INFO.value >= self.chattyLevel.value:
            print(message)

    def warn(self, message) -> None:
        if LogLevel.WARN.value >= self.logLevel.value:
            self._log(message, "WARN")
        if LogLevel.WARN.value >= self.chattyLevel.value:
            print(message)

    def error(self, message) -> None:
        if LogLevel.ERROR.value >= self.logLevel.value:
            self._log(message, "ERROR")
        if LogLevel.ERROR.value >= self.chattyLevel.value:
            print(message)

    def _log(self, message: str, level: str) -> None:
        now = datetime.now()
        with open(self.filepath, "a", encoding="UTF-8") as file:
            file.write(f"[{now}]{self.loggerName}.{level}:{message}\n")

    @classmethod
    def getLogLevel(cls) -> LogLevel:
        return cls.logLevel
    
    @classmethod
    def getChattyLevel(cls) -> LogLevel:
        return cls.chattyLevel

    @classmethod
    def setLogLevel(cls, logLevel: LogLevel) -> None:
        cls.logLevel = logLevel

    @classmethod
    def setChattyLevel(cls, chattyLevel: LogLevel) -> None:
        cls.chattyLevel = chattyLevel