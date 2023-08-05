"""
This module includes AfeApplicationOperations class.
"""
import threading

from organon.afe.core.businessobjects.afe_static_objects import AfeStaticObjects
from organon.fl.core.helpers import guid_helper
from organon.fl.generic.interaction.fl_initializer import FlInitializer
from organon.fl.logging.helpers.log_helper import LogHelper


class AfeApplicationOperations:
    """
    AfeApplicationOperations
    """

    APPLICATION_INITIALIZED = False
    __INITIALIZATION_LOCK = threading.Lock()

    @classmethod
    def initialize_app(cls, log_to_console: bool = True):
        """Initializes application."""
        with AfeApplicationOperations.__INITIALIZATION_LOCK:
            if not AfeApplicationOperations.APPLICATION_INITIALIZED:
                cls._on_init(log_to_console)
                AfeApplicationOperations.APPLICATION_INITIALIZED = True
        AfeApplicationOperations._toggle_log(log_to_console)

    @classmethod
    def _on_init(cls, log_to_console: bool):
        cls._initialize_fl(log_to_console)
        cls.register_types()
        AfeStaticObjects.set_defaults()
        AfeApplicationOperations.initialize_logging()

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
    def finalize_app(cls):
        """Finalizes application."""

    @classmethod
    def register_types(cls):
        """
        Registers ioc items
        :return: nothing
        """

    @staticmethod
    def _toggle_log(log_to_console):
        """Enables/Disables logging to console"""
        LogHelper.initialize(log_to_console=log_to_console)
