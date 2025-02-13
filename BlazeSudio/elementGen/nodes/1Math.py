from BlazeSudio.elementGen import Image

__all__ = [
    'Add',
    'Sub',
    'Avg',
    'Inv'
]

class ImgWOp(Image):
    def __init__(self, func, A, B):
        self.func = func
        self.A = A
        self.B = B
        self.bothimg = isinstance(B, Image)
    
    def get(self, x, y):
        if self.bothimg:
            return self.func(self.A.get(x, y), self.B.get(x, y))
        return self.func(self.A.get(x, y), self.B)
    
    def getMap(self, x, y, xTo, yTo):
        if self.bothimg:
            li1, li2 = self.A.getMap(x, y, xTo, yTo), self.B.getMap(x, y, xTo, yTo)
            return [[self.func(li1[y][x], li2[y][x]) for x in range(len(li1[y]))] for y in range(len(li1))]
        li = self.A.getMap(x, y, xTo, yTo)
        return [[self.func(li[y][x], self.B) for x in range(len(li[y]))] for y in range(len(li))]

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
    elif isinstance(A, Image) and isinstance(B, (Image, tuple)):
        return ImgWOp(Add, A, B)
    elif isinstance(A, tuple) and isinstance(B, Image):
        return ImgWOp(Add, B, A)
    else:
        return str(A) + str(B)

def Sub(A, B):
    """Subtract
    Subtracts a value from another value.

    2 numbers: A - B.
    2 booleans: NAND's them.
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
        return float(A) - float(B)
    elif isinstance(A, bool) and isinstance(B, bool):
        return not A and B
    elif isinstance(A, tuple) and isinstance(B, (float, int)):
        return tuple([min(max(i - B, 0), 255) for i in A])
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple([min(max(A[i] - B[i], 0), 255) for i in range(3)])
    elif isinstance(A, Image) and isinstance(B, (Image, tuple)):
        return ImgWOp(Sub, A, B)
    elif isinstance(A, tuple) and isinstance(B, Image):
        return ImgWOp(Sub, B, A)
    else:
        return str(A).replace(str(B), '')

def Avg(A, B):
    """Average
    Averages 2 values.

    2 numbers: (A + B) / 2.
    2 booleans: XOR's them.
    A colour and:
        A number: Average all values in colour with that number (i.e. (colour[idx] + num) / 2).
        A colour: Average all values in colour with the other (i.e. (colour[idx] + othercolour[idx]) / 2).
    An image and:
        An image: Average the colours of each pixel.
        A colour: Average each pixel's colour with that colour.
    else: Turns them into strings and finds the ASCII value halfway between each character (and turns it into a string).
    
    Args:
        A (Any)
        B (Any)
    
    Returns:
        Out (Any)
    """
    if isinstance(A, (float, int)) and isinstance(B, (float, int)):
        return (float(A) + float(B)) / 2
    elif isinstance(A, bool) and isinstance(B, bool):
        return A != B
    elif isinstance(A, tuple) and isinstance(B, (float, int)):
        return tuple([(i+B)//2 for i in A])
    elif isinstance(A, tuple) and isinstance(B, tuple):
        return tuple([(A[i]+B[i])//2 for i in range(3)])
    elif isinstance(A, Image) and isinstance(B, (Image, tuple)):
        return ImgWOp(Avg, A, B)
    elif isinstance(A, tuple) and isinstance(B, Image):
        return ImgWOp(Avg, B, A)
    else:
        A, B = str(A), str(B)
        return ''.join(repr(chr((ord(A[i])+ord(B[i]))//2))[1:-1] for i in range(min(len(A), len(B))))

class InvImg(Image):
    def __init__(self, img):
        self.img = img
    
    def get(self, x, y):
        return 255 - self.img.get(x, y)
    
    def getMap(self, x, y, xTo, yTo):
        out = self.img.getMap(x, y, xTo, yTo)
        return [[(255-j[0], 255-j[1], 255-j[2]) for j in i] for i in out]

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
    elif isinstance(A, Image):
        return InvImg(A)
    else:
        return A
