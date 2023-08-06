# test_none_list.py
# For testing NoneList


# Tests
def works_test():
    """
    ### Summary
    Tests if NoneList works as intended
    """
    
    # Imports
    from naters_utils.iterables import NoneList
    
    # Create list
    list_ = NoneList(10)
    assert list_ == [None] * 10
    
    # Append 1
    list_.append(1)
    assert list_ == [1] + [None] * 9
    
    # Extend with 2, 3, & 4
    list_.extend([2, 3, 4])
    assert list_ == [*range(1, 5)] + [None] * 6
    
    # Check length
    assert len(list_) == 4
    
    # Remove 2
    list_.remove(2)
    assert list_ == [1, None, 3, 4] + [None] * 6
    
    # Pop 3
    assert list_.pop(2) == 3
    assert list_ == [1, None, None, 4] + [None] * 6
    
    # Clear list
    list_.clear()
    assert list_ == [None] * 10