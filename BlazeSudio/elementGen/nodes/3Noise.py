from BlazeSudio.elementGen import Image
import random
import numpy as np

__all__ = [
    'PerlinNoise'
]

# Thanks so much to https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html for the awesome perlin noise code!
def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*np.pi*np.random.rand(res[0]+1, res[1]+1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return np.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)

def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (min(frequency*res[0], shape[0]), min(frequency*res[1], shape[1])))
        frequency *= 2
        amplitude *= persistence
    return noise

class NoisyImage(Image):
    def __init__(self, data=None, /, octaves=1, seed=0, scale=(10, 10)):
        self.octaves, self.seed = octaves, seed
        self.xScale, self.yScale = scale
        self.cache = {}
        super().__init__(data)
    
    def get(self, x, y):
        return self.getMap(x, y, x+1, y+1)[0][0]
    
    def getMap(self, x, y, xTo, yTo):
        cacheSearch = (x, y, xTo, yTo)
        if cacheSearch in self.cache:
            return self.cache[cacheSearch]
        w, h = int(xTo - x), int(yTo - y)
        np.random.seed(max(min(int(self.seed), 4294967295), 0))
        res = (max(1, w // 4), max(1, h // 4))
        noise_img = generate_fractal_noise_2d((w, h), res, self.octaves)
        
        end = [[(val, val, val) for i in j for val in (max(min(int((i + 1) * 127.5), 255), 0),)] for j in noise_img]

        if len(self.cache) > 127:
            self.cache.pop(list(self.cache.keys())[0])

        self.cache[cacheSearch] = end

        return end

def PerlinNoise(octaves, xScale, yScale, seed):
    """PerlinNoise
    Make some noise!

    Args:
        octaves (int): The number of octaves to use for the noise. Defaults to 1.
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
        base = random.randint(0, 4294967295) # 2**32-1
    
    return NoisyImage(octaves=octaves, seed=base, scale=(xScale, yScale))
