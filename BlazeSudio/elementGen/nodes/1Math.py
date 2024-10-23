from BlazeSudio.elementGen import Image as _Image

def Add(A, B):
    """Add
    Adds 2 things together.

    2 numbers: Adds them.
    2 booleans: OR's them.
    A colour and:
        A number: Adds the number to all the values in the colour (r, g & b).
        A colour: Adds the values of the colours together.
    An image and:
        An image: Adds the colours of the images together.
        A colour: Adds the colour to all the colours in the image.
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
    elif isinstance(A, _Image) and isinstance(B, _Image):
        return _Image([[Add(A.get(y, x), B.get(y, x)) for x in range(A.size[0])] for y in range(A.size[1])])
    elif isinstance(A, _Image) and isinstance(B, tuple):
        return _Image([[Add(A.get(y, x), B) for x in range(A.size[0])] for y in range(A.size[1])])
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
    An image and:
        An image: Subtracts the colours of the images.
        A colour: Subtracts the colour from all the colours in the image.
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
    elif isinstance(A, _Image) and isinstance(B, _Image):
        return _Image([[Sub(A.get(y, x),B.data[y][x]) for x in range(A.size[0])] for y in range(A.size[1])])
    elif isinstance(A, _Image) and isinstance(B, tuple):
        return _Image([[Sub(A.get(y, x),B) for x in range(A.size[0])] for y in range(A.size[1])])
    else:
        return str(A).replace(str(B), '')

def Inv(A):
    """Invert
    Inverts the value.

    A number: -A.
    A boolean: not A.
    A colour: Inverts the colour.
    An image: Inverts the image.
    else: Returns the value.
    
    Args:
        A (Any)
    
    Returns:
        Out (Any)
    """
    if isinstance(A, (float, int)):
        return -float(A)
    elif isinstance(A, bool):
        return not A
    elif isinstance(A, tuple):
        return tuple([255 - i for i in A])
    elif isinstance(A, _Image):
        return _Image([[Inv(A.get(y, x)) for x in range(A.size[0])] for y in range(A.size[1])])
    else:
        return A

def ToStr(A):
    """To String
    Converts the value to a string.

    Args:
        A (Any)
    
    Returns:
        Out (str)
    """
    return str(A)

def ToNum(A):
    """To Number
    Converts the value to a number, or 0 if input is not a number.

    Args:
        A (Any)
    
    Returns:
        Out (float)
    """
    try:
        return float(A)
    except:
        return 0

def ToImg(A):
    """To Image
    Converts the value to an image.

    A number: An image with the shade of the input number.
    A colour: An image with the colour of the input.
    An image: The input image.
    else: An empty image.

    Args:
        A (Any)
    
    Returns:
        Out (Image)
    """
    if isinstance(A, _Image):
        return A
    elif isinstance(A, (float, int)):
        return _Image([[(int(A), int(A), int(A))]])
    elif isinstance(A, tuple):
        return _Image([[A]])
    else:
        return _Image()
