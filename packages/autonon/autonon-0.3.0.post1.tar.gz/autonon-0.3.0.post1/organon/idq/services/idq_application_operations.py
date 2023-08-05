"""
This module includes IdqApplicationOperations class.
"""
import threading

from organon.fl.core.helpers import guid_helper
from organon.fl.generic.interaction.fl_initializer import FlInitializer
from organon.fl.logging.helpers.log_helper import LogHelper


class IdqApplicationOperations:
    """Idq Application Operations"""

    APPLICATION_INITIALIZED = False
    __INITIALIZATION_LOCK = threading.Lock()

    @classmethod
    def initialize_app(cls, log_to_console: bool = False):
        """Initializes application."""
        with IdqApplicationOperations.__INITIALIZATION_LOCK:
            if not IdqApplicationOperations.APPLICATION_INITIALIZED:
                cls._initialize_fl(log_to_console)
                IdqApplicationOperations.register_types()
                IdqApplicationOperations.initialize_logging()
                IdqApplicationOperations.APPLICATION_INITIALIZED = True

    @classmethod
    def _initialize_fl(cls, log_to_console: bool):
        FlInitializer.application_initialize(log_to_console=log_to_console)

    @staticmethod
    def initialize_logging():
        """Initializes logging."""
        execution_id = guid_helper.new_guid(32)
        default_format = "[%(asctime)s] [%(threadName)s] %(levelname)-8s %(module_name)s:%(line_number)s : " \
                         "%(execution_id)s  - %(message)s"
        LogHelper.add_global_extra("execution_id", execution_id)
        LogHelper.set_default_format(default_format)

    @classmethod
    def register_types(cls):
        """Registers types to IOC"""
        # todo
