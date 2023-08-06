# test_func_cache.py
# Tests for func cache


# Imports
from random import randint


# Tests
def works_test():
    """
    ### Summary
    Tests if the cache works as intended.
    """
    
    # Imports
    from naters_utils.functions import func_cache

    # Define function
    @func_cache()
    def add(*nums):
        return sum(nums)
    
    # Run function
    nums = [randint(1, 10)] * randint(1, 10)
    result = add(*nums)
    
    # Assert results are equal
    assert add(*nums) == result


def methods_work_test():
    """
    ### Summary
    Tests if the cache works as intended with objects.
    """
    
    # Imports
    from naters_utils.functions import func_cache

    # Define class
    class Adder:
        @func_cache()
        def add(self, *nums):
            return sum(nums)
    
    adder = Adder()
    
    # Run function
    nums = [randint(1, 10)] * randint(1, 10)
    result = adder.add(*nums)
    
    # Assert results are equal
    assert adder.add(*nums) == result