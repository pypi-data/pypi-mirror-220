# test_isntinstance.py
# For testing isntinstance


# Tests
def works_test():
    """
    ### Summary
    Tests is isntinstance works as intended.
    """
    
    # Imports
    from naters_utils.objects import isntinstance
    
    # Test method
    assert isntinstance(1, int) == False
    assert isntinstance(1, str) == True
    assert isntinstance(1, float) == True
    assert isntinstance(1, bool) == True