def Add(A, B):
    """Add
    Adds 2 things together.

    2 numbers: Adds them.
    2 booleans: OR's them.
    A colour and:
        A number: Adds the number to all the values in the colour (r, g & b).
        A colour: Adds the values of the colours together.
    else: Concatenates them.
    
    Args:
        A (Any)
        B (Any)
    
    Returns:
        Out (Any)
    """
    if isinstance(A, (float, int)) and isinstance(B, (float, int)):
        return float(A) + float(B)
    elif isinstance(A, bool) and isinstance(B, bool):
        return A or B
    elif isinstance(A, tuple) and isinstance(B, (float, int)):
        return tuple([max(min(i + B, 255), 0) for i in A])
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple([max(min(A[i] + B[i], 255), 0) for i in range(3)])
    else:
        return str(A) + str(B)

def Sub(A, B):
    """Subtract
    Subtracts a value from another value.

    2 numbers: A - B.
    2 booleans: XOR's them.
    A colour and:
        A number: Subtracts the number from all the values in the colour (r, g & b).
        A colour: Subtracts the values of the colours.
    else: Turns them into strings and removes all instance of B from A.
    
    Args:
        A (Any)
        B (Any)
    
    Returns:
        Out (Any)
    """
    if isinstance(A, (float, int)) and isinstance(B, (float, int)):
        return float(A) + float(B)
    elif isinstance(A, bool) and isinstance(B, bool):
        return A != B
    elif isinstance(A, tuple) and isinstance(B, (float, int)):
        return tuple([min(max(i - B, 0), 255) for i in A])
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple([min(max(A[i] - B[i], 0), 255) for i in range(3)])
    else:
        return str(A).replace(str(B), '')
