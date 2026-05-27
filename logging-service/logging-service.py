from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
from re import L
class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"



class LogRecord:
    def __init__(self, message: str, log_level: LogLevel, thread_name: str):
        self.timestamp = datetime.now()
        self.message = message
        self.log_level = log_level
        self.thread_name = thread_name

class Formatter(ABC):
    @abstractmethod
    def format(self, log: LogRecord) -> str:
        pass

class PlainTextFormatter(Formatter):
    def format(self, log: LogRecord):
        return str(log.timestamp) + " " + log.thread_name + " " + log.log_level.name + ": " + log.message

class Sink(ABC):
    @abstractmethod
    def send(self, message: str):
        pass

class FileSink(Sink):
    def __init__(self, file: str):
        self.file = file
    def send(self, message: str):
        with open(self.file, "w") as file:
            file.write(message)


class Destination:
    def __init__(self, sink: Sink, formatter: Formatter, min_level: LogLevel):
        self.sink = sink
        self.formatter = formatter
        self.min_level = min_level
    def send_log(self, log: LogRecord):
        if self.meets_min_level(log.log_level):
            formatted = self.formatter.format(log)
            self.sink.send(formatted)

    def meets_min_level(self, log_level: LogLevel):
        levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARN, LogLevel.ERROR, LogLevel.FATAL]
        min_level = levels.index(self.min_level)
        level = levels.index(log_level)
        if level >= min_level:
            return True
        else:
            return False

class Logger:
    def __init__(self, destinations: list[Destination]):
        self.destinations = destinations
    def create_log_record(self, message, log_level: LogLevel, thread_name: str):
        record = LogRecord(message, log_level, thread_name)
        for destination in self.destinations:
            destination.send_log(record)

file_sink = FileSink('output.txt')
plain_text_formatter = PlainTextFormatter()
min_level = LogLevel.DEBUG
file_destination = Destination(file_sink, plain_text_formatter, min_level)
logger = Logger([file_destination])
logger.create_log_record("created a log record", LogLevel.DEBUG, "this thread")