from fore_cloudreach.auth import Auth
from fore_cloudreach.template import Template
from fore_cloudreach.ingester import Ingester
from fore_cloudreach.errors import AuthenticationError, ReadingMapFileError, EmptyMapFileError, ReportCreationError
#import pkg_resources
from importlib.metadata import version

token = None
gcreds = None
debug_mode = False

def switch_debug_mode(mode=False) -> bool:
    """
    **debug_mode** control the logging verbosity 

    Args:
        mode: boolean
        If missing the default value is False. Set the current value for the global variable `debug_mode`;

    returns:
        boolean 
        Shows the current mode: True the debug logging is ON and False for debug logging is OFF;
    """

    global debug_mode 
    debug_mode = mode
    print(f"The debug logging mode set to: {debug_mode}")

    return  debug_mode


def get_package_version():
    """
    Returning the current version of the package
    """
    v = version('fore_cloudreach')
    print(f"The package 'fore_cloudreach' version: {v}")
    
    return v