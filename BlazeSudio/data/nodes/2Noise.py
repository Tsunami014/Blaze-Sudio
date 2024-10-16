from BlazeSudio.elementGen import Image as _Image
from noise import snoise2 as _snoise2

def PerlinNoise():
    """PerlinNoise
    Make some noise!

    Returns:
        Img (Image): The generated noise!
    """
    octaves = 6
    imgSze = (100, 100)
    def getNoise(x, y):
        n = int((_snoise2(x / 10, y / 10, octaves)+1) * (255/2))
        return (n, n, n)
    imgDat = [
        [
            getNoise(x, y) for x in range(imgSze[0])
        ] for y in range(imgSze[1])
    ]
    return _Image(imgSze, imgDat)
