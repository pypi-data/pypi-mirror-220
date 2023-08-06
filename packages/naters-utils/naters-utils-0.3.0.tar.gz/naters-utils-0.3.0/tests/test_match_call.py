# test_match_call.py
# For testing match call


# Tests
def works_test():
    """
    ### Summary
    Tests if match call works as intended.
    """
    
    # Imports
    from naters_utils.functions import MatchCall

    # Define functions
    math = MatchCall()
    @math.case("add")
    def add(a, b):
        return a + b
    @math.case("subtract")
    def subtract(a, b):
        return a - b
    @math.case("multiply")
    def multiply(a, b):
        return a * b
    @math.case("divide")
    def divide(a, b):
        return a / b
    
    # Test functionality
    assert math("add", 1, 2) == 3
    assert math("subtract", 1, 2) == -1
    assert math("multiply", 1, 2) == 2
    assert math("divide", 1, 2) == 0.5


def no_arg_match_test():
    """
    ### Summary
    Tests if the match call works as intended without arg matches
    """
    
    # Imports
    from naters_utils.functions import MatchCall

    # Define functions
    math = MatchCall()
    @math.case()
    def add(a, b):
        return a + b
    @math.case()
    def subtract(a, b):
        return a - b
    @math.case()
    def multiply(a, b):
        return a * b
    @math.case()
    def divide(a, b):
        return a / b
    
    # Test functionality
    result = math("add", 1, 2)
    assert result == 3
    assert math("subtract", 1, 2) == -1
    assert math("multiply", 1, 2) == 2
    assert math("divide", 1, 2) == 0.5


def works_with_objects_test():
    """
    ### Summary
    Tests if match call works with objects
    """
    
    # Imports
    from naters_utils.functions import MatchCall

    # Define class
    class Math:
        __call__ = MatchCall()
        @__call__.case()
        def add(self, a, b):
            return a + b
        @__call__.case()
        def subtract(self, a, b):
            return a - b
        @__call__.case()
        def multiply(self, a, b):
            return a * b
        @__call__.case()
        def divide(self, a, b):
            return a / b
    math = Math()
    
    # Test functionality
    assert math("add", 1, 2) == 3
    assert math("subtract", 1, 2) == -1
    assert math("multiply", 1, 2) == 2
    assert math("divide", 1, 2) == 0.5