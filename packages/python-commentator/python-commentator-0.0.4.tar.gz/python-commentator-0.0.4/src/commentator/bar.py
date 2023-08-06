
def absolutely(n):
    """
    This function takes an integer or float as input and returns it's absolute value as output.
    """
    # If the input is negative, then it's absolute value is simply the negation of the input.
    if n < 0:
        return -n
    # If the input is already non-negative, then it's absolute value is simply itself.
    else:
        return n
