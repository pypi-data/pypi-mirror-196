"""
This module is for logging and includes LogHelper class.
"""
import logging
import sys
from typing import List, Dict, Any


class Levels:
    """Class for constant values of logging levels """
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class LogCallerInfo:
    """Stores FrameInfo information"""

    def __init__(self):
        self.frame = None
        self.package_name = None
        self.module_name = None
        self.class_name = None
        self.func_name = None
        self.file_name = None
        self.line_number = None


class OrganonFormatter(logging.Formatter):
    """
    Custom logging formatter class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_format = args[0]
        self.level_formats = {
            Levels.NOTSET: None,
            Levels.INFO: None,
            Levels.DEBUG: None,
            Levels.WARNING: None,
            Levels.ERROR: None,
            Levels.CRITICAL: None
        }

    def format(self, record):
        """Formats a log according to level of message"""
        # pylint: disable=protected-access
        original_fmt = self._style._fmt
        self._style._fmt = self.__get_format(record.levelno)
        result = super().format(record)
        self._style._fmt = original_fmt
        return result

    def __get_format(self, levelno: int):
        """Returns format corresponding to given level"""
        if levelno in self.level_formats and self.level_formats[levelno] is not None:
            return self.level_formats[levelno]
        return self.default_format

    def set_default_format(self, format_str: str):
        """Sets default format"""
        self.default_format = format_str

    def set_level_format(self, level, format_str: str):
        """Sets format string of a level
        :param level: Level of which format string will be set (Levels.DEBUG, Levels.INFO etc)
        :param format_str: Format string to be set to given level
        :type format_str: str
        """
        if level in self.level_formats:
            self.level_formats[level] = format_str


class LogHelper:
    """
    Includes static methods for logging.
    """
    Levels = Levels
    level = Levels.INFO
    default_format = "[%(asctime)s] [%(threadName)s] %(levelname)-8s %(module_name)s:%(line_number)s - %(message)s"
    default_file = "application.log"
    log_formatter = OrganonFormatter(default_format, "%Y-%m-%d %H:%M:%S")
    global_extras: Dict[str, Any] = {}
    handlers: List[logging.Handler] = []

    @staticmethod
    def initialize(format_str: str = default_format, file_path: str = default_file, log_to_console: bool = True,
                   log_level: int = Levels.INFO):
        """
        Adds file and console_apps handlers. Sets minimum log level and log format
        :param format_str: Format of logs.
        :type format_str: str
        :param file_path: Path to log file.
        :type file_path: str
        :param log_to_console: Set to true if logs should be printed to console_apps
        :type log_to_console: bool
        :param log_level: Minimum level of messages to be logged. (Default=LogHelper.Levels.INFO)
        :type log_level: int
        """
        LogHelper.reset()
        LogHelper.set_level(log_level)
        LogHelper.set_default_format(format_str)
        LogHelper.add_default_file_handler(file_path)
        if log_to_console:
            LogHelper.add_default_console_handler()

    @staticmethod
    def reset():
        """Resets settings"""
        LogHelper.handlers = []
        LogHelper.set_default_format(LogHelper.default_format)
        LogHelper.set_level(LogHelper.Levels.INFO)

    @staticmethod
    def set_level(level):
        """
        Sets level of loggers
        :param level: logging levels (LogHelper.Levels.INFO, LogHelper.Levels.DEBUG etc.)
        """
        LogHelper.level = level

    @staticmethod
    def add_default_file_handler(file_path: str):
        """
        Sets file where logs will appear
        :param file_path: path to log file
        :type file_path: str
        """
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        if LogHelper.log_formatter:
            file_handler.setFormatter(LogHelper.log_formatter)
        LogHelper.add_handler(file_handler)

    @staticmethod
    def add_default_console_handler():
        """
        Add console_apps handler to loggers
        """
        stream_handler = logging.StreamHandler()
        if LogHelper.log_formatter:
            stream_handler.setFormatter(LogHelper.log_formatter)
        LogHelper.add_handler(stream_handler)

    @staticmethod
    def set_default_format(format_str: str):
        """Sets default format of log formatter"""
        LogHelper.log_formatter.set_default_format(format_str)

    @staticmethod
    def set_level_format(level, format_str: str):
        """Sets format string of a level
        :param level: Level of which format string will be set (Levels.DEBUG, Levels.INFO etc)
        :param format_str: Format string to be set to given level
        :type format_str: str
        """
        LogHelper.log_formatter.set_level_format(level, format_str)

    @staticmethod
    def add_global_extra(key: str, value):
        """
        Adds a global extra, that is a global value to be logged with every log.
        """
        LogHelper.global_extras[key] = value

    @staticmethod
    def add_handler(handler: logging.Handler, use_default_format: bool = True):
        """Adds extra handlers to loggers"""
        if use_default_format:
            handler.setFormatter(LogHelper.log_formatter)
        LogHelper.handlers.append(handler)
        loggers = LogHelper.get_all_loggers()
        for logger in loggers:
            logger.addHandler(handler)

    @staticmethod
    def get_all_loggers():
        """Returns all loggers"""
        return [logging.getLogger(name) for name in logging.root.manager.loggerDict]  # pylint: disable=no-member

    @staticmethod
    def __get_logger(name: str):
        """Creates a logger"""
        root_logger = logging.getLogger(name)
        root_logger.setLevel(LogHelper.level)
        if len(root_logger.handlers) == 0:
            for handler in LogHelper.handlers:
                root_logger.addHandler(handler)

        return root_logger

    @staticmethod
    def info(message: str):
        """
        Logs a message with level "INFO".
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.info(message, extra=LogHelper.__get_extras(log_caller))

    @staticmethod
    def debug(message):
        """
        Logs a message with level "DEBUG".
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.debug(message, extra=LogHelper.__get_extras(log_caller))

    @staticmethod
    def warning(message):
        """
        Logs a message with level 'WARNING'.
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.warning(message, extra=LogHelper.__get_extras(log_caller))

    @staticmethod
    def error(message):
        """
        Logs a message with level 'ERROR'.
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.error(message, extra=LogHelper.__get_extras(log_caller))

    @staticmethod
    def exception(message):
        """
        Logs a message with level 'ERROR' and also logs stack trace. Should only be called in an exception handler.
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.exception(message, extra=LogHelper.__get_extras(log_caller))
        # message = ExceptionFormattingHelper.format_exception(exception)

    @staticmethod
    def critical(message):
        """
        Logs a message with level 'CRITICAL'.
        :param message: Message to be logged.
        :type message: str
        """
        log_caller = get_log_caller_info()
        logger = LogHelper.__get_logger(log_caller.module_name)
        logger.critical(message, extra=LogHelper.__get_extras(log_caller))

    @staticmethod
    def __get_extras(log_caller_info: LogCallerInfo, except_list: List[str] = None):
        """
        Adds extra values while logging to be used in format of log formatter
        :param log_caller_info:
        :param except_list: names of attributes in log_caller_info which should not exist in log message
        :return: dictionary of extra values
        """
        extras = {}
        for attr in log_caller_info.__dict__:
            attr_val = getattr(log_caller_info, attr)
            if attr_val is not None:
                if except_list is not None and attr in except_list:
                    extras[attr] = ""
                else:
                    extras[attr] = attr_val
            else:
                extras[attr] = ""

        for key, value in LogHelper.global_extras.items():
            # global_extras_str += "{0} ".format(str(value))
            extras[key] = value

        return extras


if hasattr(sys, '_getframe'):
    currentframe = lambda stack_index: sys._getframe(stack_index + 1)  # pylint: disable=protected-access
else:
    def currentframe(stack_index):
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception:  # pylint: disable=broad-except
            return sys.exc_info()[stack_index].tb_frame.f_back


def get_log_caller_info(stack_index: int = 2) -> LogCallerInfo:
    """
    Creates a LogCallerInfo instance using stack frame info
    :param stack_index: index of FrameInfo in stack
    :return: Stack Frame info where log is called
    """
    info = LogCallerInfo()
    frm = currentframe(stack_index)

    f_locals = frm.f_locals
    if "self" in f_locals:
        info.class_name = f_locals["self"].__class__.__qualname__
    info.frame = frm
    info.package_name = frm.f_globals["__package__"]
    info.module_name = frm.f_globals["__name__"]
    f_code = frm.f_code
    info.func_name = f_code.co_name
    info.line_number = frm.f_lineno
    info.file_name = f_code.co_filename
    return info
