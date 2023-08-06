# test_thread_wrap.py
# For testing the thread_wrap decorator


# Imports
from time import sleep
from timeit import timeit


# Tests
def works_test():
    """
    ### Summary
    Tests if the thread_wrap decorator works as intended.
    """
    
    from naters_utils.functions import thread_wrap
    
    @thread_wrap("TestThread")
    def long_function():
        sleep(2)
    
    assert timeit(long_function, number=10) < 2


def methods_work_test():
    """
    ### Summary
    Tests if the thread_wrap decorator works as intended.
    """
    
    from naters_utils.functions import thread_wrap
    
    class LongFunction:
        length = 2
        @thread_wrap("TestThread")
        def long_function(self):
            sleep(self.length)
    
    assert timeit(LongFunction().long_function, number=10) < 2