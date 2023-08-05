"""
This module keeps the functions that are used in Framework Library initialization.
"""
import threading

from organon.fl.core.businessobjects.fl_core_static_objects import FlCoreStaticObjects
from organon.fl.logging.helpers.log_helper import LogHelper

FL_INIT_LOCK = threading.Lock()


class FlInitializer:
    """Class for fl application operations"""
    @classmethod
    def application_initialize(cls, log_to_console: bool = False):
        """
        Gives the signal for application initialization the application by passing True value to the
        application_initialize_called variable.
        :return: nothing
        """
        with FL_INIT_LOCK:
            if not FlCoreStaticObjects.application_initialize_called:
                cls._on_init(log_to_console)
                FlCoreStaticObjects.application_initialize_called = True

    @classmethod
    def _on_init(cls, log_to_console: bool):
        LogHelper.initialize(log_to_console=log_to_console)
        cls.register_types()

    @classmethod
    def register_types(cls):
        """
        Registers the IoC items according to its ioc key, abstract type and concrete type.
        :return:nothing
        """
