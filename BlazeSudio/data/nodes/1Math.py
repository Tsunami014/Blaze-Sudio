def Add(A, B):
    """Add
    Adds 2 things together.

    2 numbers: Adds them.
    2 booleans: OR's them.
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
    else:
        return str(A) + str(B)

def Sub(A, B):
    """Subtract
    Subtracts a value from another value.

    2 numbers: A - B.
    2 booleans: XOR's them.
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
    else:
        return str(A).replace(str(B), '')
