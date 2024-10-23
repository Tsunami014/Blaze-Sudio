from BlazeSudio.elementGen import Image as _Image
from noise import snoise2 as _snoise2
from random import randint as _randint

def PerlinNoise(octaves, xScale, yScale, seed):
    """PerlinNoise
    Make some noise!

    Args:
        octaves (int): The number of octaves to use for the noise. Defaults to 6.
        xScale (number): The scale of the noise in the x direction. Defaults to 10.
        yScale (number): The scale of the noise in the y direction. Defaults to 10.
        seed (int): The seed for the noise, 0 = random. Defaults to 0.

    Returns:
        Img (Image): The generated noise!
    """
    octaves = int(octaves)
    if octaves <= 0:
        octaves = 1
    xScale = max(float(xScale), 0.1)
    yScale = max(float(yScale), 0.1)
    base = float(seed)
    if base == 0:
        base = _randint(-999999, 999999)
    def getNoise(x, y):
        n = int((_snoise2(x / xScale, y / yScale, octaves, base=base)+1) * (255/2))
        return (n, n, n)
    img = _Image()
    img.get = getNoise
    return img
