# iterables.py
# Holds iterable utils


# Imports
from __future__ import annotations

from typing import Any, Iterable

from .objects import isntinstance


# Metadata
__all__ = ["dynamic_iterable", "NoneList"]
__version__ = "1.0.2"


# Definitions
class NoneList(list):
    """
    ### Summary
    A list of a fixed length, but with elements set to a default of None
    
    ### Usage:
    >>> from naters_utils.iterables import NoneList
    >>> my_list = NoneList(5)
    >>> my_list
    [None, None, None, None, None]
    >>> my_list.append("Hello")
    ["Hello", None, None, None, None]
    """
    
    def __init__(self, length: int):
        """
        ### Summary
        Creates a list of fixed length, but with elements set to a default of None
        
        ### Parameters:
            length: int # The length of the list
        
        ### Usage:
        >>> from naters_utils.iterables import NoneList
        >>> my_list = NoneList(5)
        >>> my_list
        [None, None, None, None, None]
        >>> my_list.append("Hello")
        ["Hello", None, None, None, None]
        """
        
        if isntinstance(length, int):
            raise TypeError("length must be an integer")
        
        self.length = length
        
        super().__init__([None] * length)
    
    
    # Dunder overrides
    def __len__(self) -> int:
        return self.length - self.count(None)
    
    
    # List method overrides
    def append(self, obj: Any) -> None:
        # Check if list is full
        if len(self) + 1 > self.length:
            raise IndexError("list is full")
        
        # Add item to list
        self[self.index(None)] = obj
    
    
    def extend(self, iterable: Iterable) -> None:
        # Check if list is full
        if len(self) + len(iterable) == self.length:
            raise IndexError("list is full")
        
        # Add items to list
        for item in iterable:
            self.append(item)
    
    
    def pop(self, index: int) -> Any:
        # Make sure index is an integer
        if isntinstance(index, int):
            raise TypeError("index must be an integer")
        
        # Get item value
        value = self[index]
        
        # Reset value
        self[index] = None
        
        # Return value
        return value
    
    
    def remove(self, value: Any) -> None:
        self[self.index(value)] = None
    
    
    def clear(self) -> None:
        for i in range(self.length):
            self[i] = None
    
    
    def sort(self, key: Any = None, reverse: bool = False) -> None:
        raise NotImplementedError("sort is not supported on NoneList")