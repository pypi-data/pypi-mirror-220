# objects.py
# Holds object related utils


# Imports
from typing import Any


# Metadata
__all__ = ["isntinstance"]
__version__ = "1.0.0"


def isntinstance(obj: Any, types: type | tuple[type]) -> bool:
    """
    ### Summary
    The opposite of isinstance.  
    I just got tired of typing `not isinstance` lol.
    
    ### Parameters:
        obj: Any # The object to check
        types: type | tuple[type] # The type(s) to check for
    
    ### Returns:
        bool # If the object is not an instance
    
    ### Usage:
    >>> from naters_utils import isntinstance
    >>> isntinstance("1", int)
    True
    """
    
    return not isinstance(obj, types)