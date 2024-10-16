from BlazeSudio.elementGen import Image as _Image
from noise import snoise2 as _snoise2

def PerlinNoise(octaves, xScale, yScale):
    """PerlinNoise
    Make some noise!

    Args:
        octaves (int): The number of octaves to use for the noise. Defaults to 6.
        xScale (number): The scale of the noise in the x direction. Defaults to 10.
        yScale (number): The scale of the noise in the y direction. Defaults to 10.

    Returns:
        Img (Image): The generated noise!
    """
    octaves = int(octaves)
    if octaves <= 0:
        octaves = 1
    xScale = max(float(xScale), 0.1)
    yScale = max(float(yScale), 0.1)
    imgSze = (100, 100)
    def getNoise(x, y):
        n = int((_snoise2(x / xScale, y / yScale, octaves)+1) * (255/2))
        return (n, n, n)
    imgDat = [
        [
            getNoise(x, y) for x in range(imgSze[0])
        ] for y in range(imgSze[1])
    ]
    return _Image(imgSze, imgDat)
