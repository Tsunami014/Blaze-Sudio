__all__ = [
    'AnyInput',
    'NumInput',
    'BoolInput',
    'ColourInput',
    'Output'
]

def AnyInput(Val):
    """AnyInput
    Output any specific value.

    Args:
        Val (Any): The value to output. Could be anything! @NoNode

    Returns:
        Val (Any): The input value! @NoSidebar
    """
    return Val

def NumInput(Val):
    """NumInput
    Output any specific number.

    Args:
        Val (Number): The value to output. Any number! @NoNode

    Returns:
        Val (Number): The input value! @NoSidebar
    """
    return Val

def BoolInput(Val):
    """BoolInput
    Output either True or False.

    Args:
        Val (Bool): The value to output, either True or False. @NoNode

    Returns:
        Val (Bool): The input! @NoSidebar
    """
    return Val

def ColourInput(Val):
    """ColourInput
    Output a colour.

    Args:
        Val (Colour): The colour to output in RGB! @NoNode

    Returns:
        Val (Colour): The colour chosen! @NoSidebar
    """
    return Val

def Output(Val):
    """Output
    Output any value! Like the return statement for the entire program.

    Args:
        Val (Any): The output value.
    """
    pass
