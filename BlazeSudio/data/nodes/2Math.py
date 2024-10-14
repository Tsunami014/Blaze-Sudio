def Add(A, B):
    """Add
    Adds 2 numbers or texts together
    
    Args:
        A (Any)
        B (Any)
    
    Returns:
        Out (Any)
    """
    try:
        return float(A) + float(B)
    except (TypeError, ValueError):
        try:
            return A + B
        except (TypeError, ValueError):
            return str(A) + str(B)
