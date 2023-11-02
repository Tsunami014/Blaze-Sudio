# https://github.com/BilHim/minecraft-world-generation/blob/main/src/Minecraft%20Terrain%20Generation%20in%20Python%20-%20By%20Bilal%20Himite.ipynb

# Imports and parameters
# print('Importing...')

from random import randint
import numpy as np
from matplotlib import pyplot as plt
from skimage.draw import polygon
from PIL import Image
from noise import snoise3
from skimage import exposure
from scipy import ndimage
from scipy.spatial import Voronoi
from scipy.special import expit
from scipy.interpolate import interp1d
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.morphology import binary_dilation

try:
    from utils.conversation_parse import parseKWs
except:
    from conversation_parse import parseKWs

class Map:
    def __init__(self, *args, **kwargs):
        self.size = args[0] or kwargs.get('size')
        self.g = MapGen(*args, **kwargs)
        self.conf = self.g.outs
        self.map = self.conf[0][0]
        self.trees = self.tolist(self.conf[1])
        self.structures = []
        # self.generate_structures()
    def __call__(self, w, h, x=0, y=0):
        return [i[x:x+w] for i in self.map[y:y+h]]
    def get_structs(self, w, h, x=0, y=0):
        #return [i[x:x+w] for i in self.trees[y:y+h]]
        return [i[x:x+w] for i in self.structures[y:y+h]]

    def tolist(self, nl, do_tolist=True):
        if do_tolist: nl = [[(int(j[0]), int(j[1])) for j in i] for i in nl]
        out = np.zeros((self.size, self.size))
        for j in nl:
            for i in j:
                out[i[0]][i[1]] = 1
        return [[int(j) for j in i] for i in out]

    def generate_structures(self):
        print('Generating structures... (0/%i)' % (round(len(self.map))/10))
        outs = []
        done = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if (x, y) not in done:
                    l = floodfill(self.map, x, y)
                    outs.append(l)
                    done.extend(l)
            if x % 10 == 0: print('Generating structures... (%i/%i)' % (round(x / 10), round(len(self.map)/10)))
        print('Generating structures: sorting and choosing...')
        outs.sort(key=lambda x: len(x), reverse=True)
        self.structures = self.tolist([outs[0]])

def floodfill(matrix, x, y):
    tofill = [(x, y)]
    filled = []
    start = matrix[x][y]
    while tofill:
        x, y = tofill.pop(0)
        if matrix[x][y] == start and (x, y) not in filled:
            filled.append((x, y))
            #recursively invoke flood fill on all surrounding cells:
            if x > 0:
                tofill.append((x-1, y))
            if x < len(matrix[y]) - 1:
                tofill.append((x+1, y))
            if y > 0:
                tofill.append((x, y-1))
            if y < len(matrix) - 1:
                tofill.append((x, y+1))
    return filled

biome_names = [
    "desert",
    "savanna",
    "tropical_woodland",
    "tundra",
    "seasonal_forest",
    "rainforest",
    "temperate_forest",
    "temperate_rainforest",
    "boreal_forest"
    ]
biome_colours = [
    [255, 255, 178],
    [184, 200, 98],
    [188, 161, 53],
    [190, 255, 242],
    [106, 144, 38],
    [33, 77, 41],
    [86, 179, 106],
    [34, 61, 53],
    [35, 114, 94]
    ]
tree_densities = [4000, 1500, 8000, 1000, 10000, 25000, 10000, 20000, 5000]
housing_densities = [1, 1, 8000, 1000, 10000, 2500, 1000, 2000, 50000]

sea_colour = np.array([12, 14, 255])

class MapGen:
    def voronoi(self, points): # voroni diagram
        # Add points at edges to eliminate infinite ridges
        edge_points = self.size*np.array([[-1, -1], [-1, 2], [2, -1], [2, 2]])
        new_points = np.vstack([points, edge_points])
        
        # Calculate Voronoi tessellation
        vor = Voronoi(new_points)
        
        return vor
    
    def voronoi_map(self, vor):
        # Calculate Voronoi map
        vor_map = np.zeros((self.size, self.size), dtype=np.uint32)

        for i, region in enumerate(vor.regions):
            # Skip empty regions and infinte ridge regions
            if len(region) == 0 or -1 in region: continue
            # Get polygon vertices    
            x, y = np.array([vor.vertices[i][::-1] for i in region]).T
            # Get pixels inside polygon
            rr, cc = polygon(x, y)
            # Remove pixels out of image bounds
            in_box = np.where((0 <= rr) & (rr < self.size) & (0 <= cc) & (cc < self.size))
            rr, cc = rr[in_box], cc[in_box]
            # Paint image
            vor_map[rr, cc] = i

        return vor_map

    def relax(self, points, k=10):   #Lloyd's relaxation algorithm
        new_points = points.copy()
        for _ in range(k):
            vor = self.voronoi(new_points)
            new_points = []
            for __, region in enumerate(vor.regions):
                if len(region) == 0 or -1 in region: continue
                poly = np.array([vor.vertices[i] for i in region])
                center = poly.mean(axis=0)
                new_points.append(center)
            new_points = np.array(new_points).clip(0, self.size)
        return new_points
    
    def noise_map(self, res, seed, octaves=1, persistence=0.5, lacunarity=2.0):
        scale = self.size/res
        return np.array([[
            snoise3(
                (x+0.1)/scale,
                y/scale,
                seed+self.map_seed,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity
            )
            for x in range(self.size)]
            for y in range(self.size)
        ])
    
    def histeq(self, img,  alpha=1):
        img_cdf, bin_centers = exposure.cumulative_distribution(img)
        img_eq = np.interp(img, bin_centers, img_cdf)
        img_eq = np.interp(img_eq, (0, 1), (-1, 1))
        return alpha * img_eq + (1 - alpha) * img
    
    def average_cells(self, vor, data):
        """Returns the average value of data inside every voronoi cell"""
        size = vor.shape[0]
        count = np.max(vor)+1

        sum_ = np.zeros(count)
        count = np.zeros(count)

        for i in range(size):
            for j in range(size):
                p = vor[i, j]
                count[p] += 1
                sum_[p] += data[i, j]

        average = sum_/count
        average[count==0] = 0

        return average

    def fill_cells(self, vor, data):
        size = vor.shape[0]
        image = np.zeros((size, size))

        for i in range(size):
            for j in range(size):
                p = vor[i, j]
                image[i, j] = data[p]

        return image

    def colour_cells(self, vor, data, dtype=int):
        size = vor.shape[0]
        image = np.zeros((size, size, 3))

        for i in range(size):
            for j in range(size):
                p = vor[i, j]
                image[i, j] = data[p]

        return image.astype(dtype)
    
    def quantize(self, data, n):
        bins = np.linspace(-1, 1, n+1)
        return (np.digitize(data, bins) - 1).clip(0, n-1)
    
    def gradient(self, im_smooth):
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.arange(-1,2).astype(float)
        kernel = - kernel / 2

        gradient_x = ndimage.convolve(gradient_x, kernel[np.newaxis])
        gradient_y = ndimage.convolve(gradient_y, kernel[np.newaxis].T)

        return gradient_x, gradient_y

    def sobel(self, im_smooth):
        gradient_x = im_smooth.astype(float)
        gradient_y = im_smooth.astype(float)

        kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])

        gradient_x = ndimage.convolve(gradient_x, kernel)
        gradient_y = ndimage.convolve(gradient_y, kernel.T)

        return gradient_x, gradient_y

    def compute_normal_map(self, gradient_x, gradient_y, intensity=1):
        width = gradient_x.shape[1]
        height = gradient_x.shape[0]
        max_x = np.max(gradient_x)
        max_y = np.max(gradient_y)

        max_value = max_x

        if max_y > max_x:
            max_value = max_y

        normal_map = np.zeros((height, width, 3), dtype=np.float32)

        intensity = 1 / intensity

        strength = max_value / (max_value * intensity)

        normal_map[..., 0] = gradient_x / max_value
        normal_map[..., 1] = gradient_y / max_value
        normal_map[..., 2] = 1 / strength

        norm = np.sqrt(np.power(normal_map[..., 0], 2) + np.power(normal_map[..., 1], 2) + np.power(normal_map[..., 2], 2))

        normal_map[..., 0] /= norm
        normal_map[..., 1] /= norm
        normal_map[..., 2] /= norm

        normal_map *= 0.5
        normal_map += 0.5

        return normal_map

    def get_normal_map(self, im, intensity=1.0):
        sobel_x, sobel_y = self.sobel(im)
        normal_map = self.compute_normal_map(sobel_x, sobel_y, intensity)
        return normal_map

    def get_normal_light(self, height_map_):
        normal_map_ = self.get_normal_map(height_map_)[:,:,0:2].mean(axis=2)
        normal_map_ = np.interp(normal_map_, (0, 1), (-1, 1))
        return normal_map_

    def apply_height_map(self, im_map, smooth_map, height_map, land_mask):
        normal_map = self.get_normal_light(height_map)
        normal_map =  normal_map*land_mask + smooth_map/2*(~land_mask)

        normal_map = np.interp(normal_map, (-1, 1), (-192, 192))

        normal_map_colour = np.repeat(normal_map[:, :, np.newaxis], 3, axis=-1)
        normal_map_colour = normal_map_colour.astype(int)

        out_map = im_map + normal_map_colour
        return out_map, normal_map
    
    def get_boundary(self, vor_map, kernel=1):
        boundary_map = np.zeros_like(vor_map, dtype=bool)
        n, m = vor_map.shape
        
        clip = lambda x: max(0, min(self.size-1, x))
        def check_for_mult(a):
            b = a[0]
            for i in range(len(a)-1):
                if a[i] != b: return 1
            return 0
        
        for i in range(n):
            for j in range(m):
                boundary_map[i, j] = check_for_mult(vor_map[
                    clip(i-kernel):clip(i+kernel+1),
                    clip(j-kernel):clip(j+kernel+1),
                ].flatten())
                
        return boundary_map
    
    def bezier(self, x1, y1, x2, y2, a):
        p1 = np.array([0, 0])
        p2 = np.array([x1, y1])
        p3 = np.array([x2, y2])
        p4 = np.array([1, a])

        return lambda t: ((1-t)**3 * p1 + 3*(1-t)**2*t * p2 + 3*(1-t)*t**2 * p3 + t**3 * p4)

    def bezier_lut(self, x1, y1, x2, y2, a):
        t = np.linspace(0, 1, 256)
        f = self.bezier(x1, y1, x2, y2, a)
        curve = np.array([f(t_) for t_ in t])

        return interp1d(*curve.T)

    def filter_map(self, h_map, smooth_h_map, x1, y1, x2, y2, a, b):
        f = self.bezier_lut(x1, y1, x2, y2, a)
        output_map = b*h_map + (1-b)*smooth_h_map
        output_map = f(output_map.clip(0, 1))
        return output_map

    def filter_inbox(self, pts):
        inidx = np.all(pts < self.size, axis=1)
        return pts[inidx]

    def generate_trees(self, n):
        trees = np.random.randint(0, self.size-1, (n, 2))
        trees = self.relax(trees, k=10).astype(np.uint32)
        trees = self.filter_inbox(trees)
        return trees
    
    def create_trees(self, river_land_mask, adjusted_height_river_map, biome_masks, densities):
        print('Generating Height Map Filters: Trees and Vegetation... (may take a while...)')

        def place_trees(n, mask, a=0.5):
            trees= self.generate_trees(n)
            rr, cc = trees.T

            output_trees = np.zeros((self.size, self.size), dtype=bool)
            output_trees[rr, cc] = True
            output_trees = output_trees*(mask>a)*river_land_mask*(adjusted_height_river_map<0.5)

            output_trees = np.array(np.where(output_trees == 1))[::-1].T    
            return output_trees
        return [np.array(place_trees(densities[i], biome_masks[i]))
                for i in range(len(biome_names))]
    
    def one(self):
        # Voronoi diagram
        print('Creating Voronoi diagram...')

        points = np.random.randint(0, self.size, (514, 2))
        vor = self.voronoi(points)
        vor_map = self.voronoi_map(vor)

        if self.useall:
            fig = plt.figure(dpi=150, figsize=(4, 4))
            plt.scatter(*points.T, s=1)

        # Lloyd's relaxation
        print('Relaxing...')
        points = self.relax(points, k=100)
        vor = self.voronoi(points)
        vor_map = self.voronoi_map(vor)

        if self.useall:
            fig = plt.figure(dpi=150, figsize=(4, 4))
            plt.scatter(*points.T, s=1)


        # Perlin noise / Simplex noise

        # Bluring the boundaries
        print('Bluring the boundaries (with noise)...')
        boundary_displacement = 8
        boundary_noise = np.dstack([self.noise_map(32, 200, octaves=8), self.noise_map(32, 250, octaves=8)])
        boundary_noise = np.indices((self.size, self.size)).T + boundary_displacement*boundary_noise
        boundary_noise = boundary_noise.clip(0, self.size-1).astype(np.uint32)

        blurred_vor_map = np.zeros_like(vor_map)

        for x in range(self.size):
            for y in range(self.size):
                j, i = boundary_noise[x, y]
                blurred_vor_map[x, y] = vor_map[i, j]

        if self.useall:
            fig, axes = plt.subplots(1, 2)
            fig.set_dpi(150)
            fig.set_size_inches(8, 4)
            axes[0].imshow(vor_map)
            axes[1].imshow(blurred_vor_map)

        vor_map = blurred_vor_map

        # Choosing Biomes
        ## Temperature–Precipitation maps
        print('Choosing biomes: Temperature–Precipitation maps...')

        temperature_map = self.noise_map(2, 10)
        precipitation_map = self.noise_map(2, 20)

        if self.useall:
            fig, axes = plt.subplots(1, 2)
            fig.set_dpi(150)
            fig.set_size_inches(8, 4)

            axes[0].imshow(temperature_map, cmap="rainbow")
            axes[0].set_title("Temperature Map")

            axes[1].imshow(precipitation_map, cmap="YlGnBu")
            axes[1].set_title("Precipitation Map")


        # Histogram Equalization
        print('Histogram equalization...')

        if self.useall:
            fig, axes = plt.subplots(1, 2)
            fig.set_dpi(150)
            fig.set_size_inches(8, 4)

            axes[0].hist(temperature_map.flatten(), bins=64, color="blue", alpha=0.66, label="Precipitation")
            axes[0].hist(precipitation_map.flatten(), bins=64, color="red", alpha=0.66, label="Temperature")
            axes[0].set_xlim(-1, 1)
            axes[0].legend()

        hist2d = np.histogram2d(
            temperature_map.flatten(), precipitation_map.flatten(),
            bins=(512, 512), range=((-1, 1), (-1, 1))
        )[0]

        hist2d = np.interp(hist2d, (hist2d.min(), hist2d.max()), (0, 1))
        hist2d = expit(hist2d/0.1)

        if self.useall:
            axes[1].imshow(hist2d, cmap="plasma")

            axes[1].set_xticks([0, 128, 256, 385, 511])
            axes[1].set_xticklabels([-1, -0.5, 0, 0.5, 1])
            axes[1].set_yticks([0, 128, 256, 385, 511])
            axes[1].set_yticklabels([1, 0.5, 0, -0.5, -1])

        uniform_temperature_map = self.histeq(temperature_map, alpha=0.33)
        uniform_precipitation_map = self.histeq(precipitation_map, alpha=0.33)

        if self.useall:
            fig, axes = plt.subplots(1, 2)
            fig.set_dpi(150)
            fig.set_size_inches(8, 4)

            axes[0].hist(uniform_temperature_map.flatten(), bins=64, color="blue", alpha=0.66, label="Precipitation")
            axes[0].hist(uniform_precipitation_map.flatten(), bins=64, color="red", alpha=0.66, label="Temperature")
            axes[0].set_xlim(-1, 1)
            axes[0].legend()

        hist2d = np.histogram2d(
            uniform_temperature_map.flatten(), uniform_precipitation_map.flatten(),
            bins=(512, 512), range=((-1, 1), (-1, 1))
        )[0]

        hist2d = np.interp(hist2d, (hist2d.min(), hist2d.max()), (0, 1))
        hist2d = expit(hist2d/0.1)

        if self.useall:
            axes[1].imshow(hist2d, cmap="plasma")

            axes[1].set_xticks([0, 128, 256, 385, 511])
            axes[1].set_xticklabels([-1, -0.5, 0, 0.5, 1])
            axes[1].set_yticks([0, 128, 256, 385, 511])
            axes[1].set_yticklabels([1, 0.5, 0, -0.5, -1])

        temperature_map = uniform_temperature_map
        precipitation_map = uniform_precipitation_map

        # Averaging Cells
        print('Averaging cells...')

        temperature_cells = self.average_cells(vor_map, temperature_map)
        precipitation_cells = self.average_cells(vor_map, precipitation_map)

        temperature_map = self.fill_cells(vor_map, temperature_cells)
        precipitation_map = self.fill_cells(vor_map, precipitation_cells)

        if self.useall:
            fig, ax = plt.subplots(1 ,2)
            fig.set_dpi(150)
            fig.set_size_inches(8, 4)

            ax[0].imshow(temperature_map, cmap="rainbow")
            ax[0].set_title("Temperature")

            ax[1].imshow(precipitation_map, cmap="Blues")
            ax[1].set_title("Precipitation")


        # Quantization
        print('Quantizing...')

        n = 256

        quantize_temperature_cells = self.quantize(temperature_cells, n)
        quantize_precipitation_cells = self.quantize(precipitation_cells, n)

        quantize_temperature_map = self.fill_cells(vor_map, quantize_temperature_cells)
        quantize_precipitation_map = self.fill_cells(vor_map, quantize_precipitation_cells)

        temperature_cells = quantize_temperature_cells
        precipitation_cells = quantize_precipitation_cells

        temperature_map = quantize_temperature_map
        precipitation_map = quantize_precipitation_map

        # Temperature–Precipitation graph
        print('Applying Temperature–Precipitation graph...')

        im = np.array(Image.open("TP_map.png"))[:, :, :3]
        biomes = np.zeros((256, 256))

        for i, colour in enumerate(biome_colours):
            indices = np.where(np.all(im == colour, axis=-1))
            biomes[indices] = i
            
        biomes = np.flip(biomes, axis=0).T

        if self.useall:
            fig = plt.figure(dpi=150, figsize=(4, 4))
            plt.imshow(biomes)
            plt.title("Temperature–Precipitation graph")
        return temperature_cells, precipitation_cells, biomes, vor_map
    
    def two(self, temperature_cells, precipitation_cells, biomes, vor_map):
        # Biome map
        print('Making biome map...')

        n = len(temperature_cells)
        biome_cells = np.zeros(n, dtype=np.uint32)

        for i in range(n):
            temp, precip = temperature_cells[i], precipitation_cells[i]
            biome_cells[i] = biomes[temp, precip]
            
        biome_map = self.fill_cells(vor_map, biome_cells).astype(np.uint32)
        biome_colour_map = self.colour_cells(biome_map, biome_colours)

        if self.useall:
            fig = plt.figure(figsize=(5, 5), dpi=150)
            plt.imshow(biome_colour_map)

        #Height Map
        print('Generating height...')

        height_map = self.noise_map(4, 0, octaves=6, persistence=0.5, lacunarity=2)
        land_mask = height_map > 0

        if self.useall:
            fig = plt.figure(dpi=150, figsize=(5, 5))
            plt.imshow(land_mask, cmap='gray')

        land_mask_colour = np.repeat(land_mask[:, :, np.newaxis], 3, axis=-1)
        masked_biome_colour_map = land_mask_colour*biome_colour_map + (1-land_mask_colour)*sea_colour

        if self.useall:
            fig = plt.figure(dpi=150, figsize=(5, 5))
            plt.imshow(masked_biome_colour_map)
        return masked_biome_colour_map, biome_map, land_mask, biome_colour_map, height_map
    
    def three(self, masked_biome_colour_map, biome_map, land_mask, height_map):
        biome_height_map, normal_map = self.apply_height_map(masked_biome_colour_map, height_map, height_map, land_mask)

        if self.useall:
            fig, ax = plt.subplots(1 ,2)
            fig.set_dpi(150)
            fig.set_size_inches(10, 5)

            ax[0].imshow(masked_biome_colour_map)
            ax[0].set_title("Biomes")

            ax[1].imshow(biome_height_map)
            ax[1].set_title("Biomes with normal")

        # Height Map Detail
        print('Generating height map detail...')

        height_map = self.noise_map(4, 0, octaves=6, persistence=0.5, lacunarity=2)
        smooth_height_map = self.noise_map(4, 0, octaves=1, persistence=0.5, lacunarity=2)

        if self.useall:
            fig, ax = plt.subplots(1 ,2)
            fig.set_dpi(150)
            fig.set_size_inches(10, 5)

            ax[0].imshow(height_map, cmap="gray")
            ax[0].set_title("Height Map")

            ax[1].imshow(smooth_height_map, cmap="gray")
            ax[1].set_title("Smooth Height Map")

        # Height Map Filters
        ## Bézier Curves
        print('Generating Height Map Filters: Bézier Curves...')

        # f = bezier_lut(0.8, 0.1, 0.9, 0.05, 0.05)
        # t = np.linspace(0, 1, 1000)
        # y = f(t)

        # from matplotlib.gridspec import GridSpec

        # fig = plt.figure(dpi=120, figsize=(8, 8/3))
        # gs = GridSpec(1, 3)

        # ax1 = plt.subplot(gs[:,:1])
        # ax1.plot(t, y)
        # ax1.set_xlim(0, 1)
        # ax1.set_ylim(0, 1)
        # ax1.set_title("Boreal Filter")

        # ax2 = plt.subplot(gs[:,1:])
        # ax2.plot(height_map[100].clip(0, 1))
        # ax2.plot(boreal_map[100])
        # ax2.set_ylim(0, 1)
        # ax2.set_title("Example")

        # plt.savefig("figures/figure_13/9.jpg")

        ## Filters
        print('Generating Height Map Filters: Filters...')

        biome_height_maps = [
            # Desert
            self.filter_map(height_map, smooth_height_map, 0.75, 0.2, 0.95, 0.2, 0.2, 0.5),
            # Savanna
            self.filter_map(height_map, smooth_height_map, 0.5, 0.1, 0.95, 0.1, 0.1, 0.2),
            # Tropical Woodland
            self.filter_map(height_map, smooth_height_map, 0.33, 0.33, 0.95, 0.1, 0.1, 0.75),
            # Tundra
            self.filter_map(height_map, smooth_height_map, 0.5, 1, 0.25, 1, 1, 1),
            # Seasonal Forest
            self.filter_map(height_map, smooth_height_map, 0.75, 0.5, 0.4, 0.4, 0.33, 0.2),
            # Rainforest
            self.filter_map(height_map, smooth_height_map, 0.5, 0.25, 0.66, 1, 1, 0.5),
            # Temperate forest
            self.filter_map(height_map, smooth_height_map, 0.75, 0.5, 0.4, 0.4, 0.33, 0.33),
            # Temperate Rainforest
            self.filter_map(height_map, smooth_height_map, 0.75, 0.5, 0.4, 0.4, 0.33, 0.33),
            # Boreal
            self.filter_map(height_map, smooth_height_map, 0.8, 0.1, 0.9, 0.05, 0.05, 0.1)
        ]

        ## Biome masks
        print('Generating Height Map Filters: Biome masks...')

        biome_count = len(biome_names)
        biome_masks = np.zeros((biome_count, self.size, self.size))

        for i in range(biome_count):
            biome_masks[i, biome_map==i] = 1
            biome_masks[i] = gaussian_filter(biome_masks[i], sigma=16)

        # Remove ocean from masks
        blurred_land_mask = land_mask
        blurred_land_mask = binary_dilation(land_mask, iterations=32).astype(np.float64)
        blurred_land_mask = gaussian_filter(blurred_land_mask, sigma=16)

        biome_masks = biome_masks*blurred_land_mask

        if self.useall:
            plt.figure(dpi=150, figsize=(5, 5))
            plt.imshow(biome_masks[6], cmap="gray")

        ## Applying Filters
        print('Generating Height Map Filters: Applying filters...')

        adjusted_height_map = height_map.copy()

        for i in range(len(biome_height_maps)):
            adjusted_height_map = (1-biome_masks[i])*adjusted_height_map + biome_masks[i]*biome_height_maps[i]

        biome_height_map = self.apply_height_map(masked_biome_colour_map, height_map, height_map, land_mask)
        new_biome_height_map = self.apply_height_map(masked_biome_colour_map, adjusted_height_map, adjusted_height_map, land_mask)

        if self.useall:
            fig, ax = plt.subplots(1 ,2)
            fig.set_dpi(150)
            fig.set_size_inches(10, 5)

            ax[0].imshow(adjusted_height_map)
            ax[0].set_title("Before")

            ax[1].imshow(new_biome_height_map[0])
            ax[1].set_title("After")
        return adjusted_height_map, biome_masks
    
    def four(self, biome_map, vor_map, adjusted_height_map, land_mask, biome_colour_map):
        ## Rivers
        ## Boundaries
        print('Generating Height Map Filters: Rivers... (may take a while...)')

        biome_bound = self.get_boundary(biome_map, kernel=5)
        cell_bound = self.get_boundary(vor_map, kernel=2)

        river_mask = self.noise_map(4, 4353, octaves=6, persistence=0.5, lacunarity=2) > 0

        new_biome_bound = biome_bound*(adjusted_height_map<0.5)*land_mask
        new_cell_bound = cell_bound*(adjusted_height_map<0.05)*land_mask

        rivers = np.logical_or(new_biome_bound, new_cell_bound)*river_mask

        loose_river_mask = binary_dilation(rivers, iterations=8)
        rivers_height = gaussian_filter(rivers.astype(np.float64), sigma=2)*loose_river_mask

        adjusted_height_river_map = adjusted_height_map*(1-rivers_height) - 0.05*rivers

        river_land_mask = adjusted_height_river_map >= 0
        land_mask_colour = np.repeat(river_land_mask[:, :, np.newaxis], 3, axis=-1)
        rivers_biome_colour_map = land_mask_colour*biome_colour_map + (1-land_mask_colour)*sea_colour

        if self.useall:
            plt.figure(dpi=150, figsize=(5, 5))
            plt.imshow(rivers_biome_colour_map)
        
        # TODO: make the rivers separate from the oceans, after this glue them together
        return rivers_biome_colour_map, river_land_mask, adjusted_height_river_map
    
    def five(self, river_land_mask, adjusted_height_river_map, biome_masks):
        ## Trees and Vegetation
        trees = self.create_trees(river_land_mask, adjusted_height_river_map, biome_masks, tree_densities)
        # Example
        if self.useall:
            low_density_trees = self.generate_trees(1000, self.size)
            medium_density_trees = self.generate_trees(5000, self.size)
            high_density_trees = self.generate_trees(25000, self.size)

            plt.figure(dpi=150, figsize=(10, 3))
            plt.subplot(131)
            plt.scatter(*low_density_trees.T, s=1)
            plt.title("Low Density Trees")
            plt.xlim(0, 256)
            plt.ylim(0, 256)

            plt.subplot(132)
            plt.scatter(*medium_density_trees.T, s=1)
            plt.title("Medium Density Trees")
            plt.xlim(0, 256)
            plt.ylim(0, 256)

            plt.subplot(133)
            plt.scatter(*high_density_trees.T, s=1)
            plt.title("High Density Trees")
            plt.xlim(0, 256)
            plt.ylim(0, 256)
            plt.figure(dpi=150, figsize=(5, 5))

            for k in range(len(biome_names)):
                plt.scatter(*trees[k].T, s=0.15, c="red")
        return trees

    def __init__(self, size, map_seed=762345, n=256, **kwargs):
        """
        Generates a map! :)

        Parameters
        ----------
        size : int
            The size of the map to generate!
            PLEASE NOTE: I am not fully sure what this specifically does. From testing I have found
            out a possibility that it is just the resolution of the map and not actually zoomed in.
        map_seed : int, optional
            The seed of the map, by default 762345
        n : int, optional
            I don't know what this is, may/may not be linked to the size above, by default 256
        
        Kwargs
        ------
        useall : bool, optional
            Whether or not to use matplotlib to save all steps of the process or just the finished result, by default False (just show finished result)
        showAtEnd : bool, optional
            Whether or not to show using matplotlib the finished result (and possibly the rest of the steps, see `useall`), by default False
        generateTrees : bool, optional
            Whether or not to generate trees. If no then will output blanks where the trees output should be below, defaults to True

        Returns
        -------
        tuple(list[numpy arrays/lists], numpy array)
            [
                out (rounded and scaled from 1-10, list), 
                colour_map (numpy array, out before rounding and scaling, also contains colours), 
                rivers_biome_colour_map, (numpy array, ???),
                adjusted_height_river_map, (numpy array, ???),
                river_land_mask (numpy array, ???),
                biome_masks (numpy array, ???)
            ], trees (list[numpy array (for each biome name)], this has all the biomes and the trees positions in them.)
        """
        # setting params
        if map_seed == None: self.map_seed = randint(0, 999999)
        else: self.map_seed = map_seed
        np.random.seed(self.map_seed)
        parseKWs(kwargs, ['useall', 'showAtEnd', 'generateTrees'])
        self.useall = kwargs.get('useall', False)
        self.size = size
        
        temperature_cells, precipitation_cells, biomes, vor_map, = self.one()

        masked_biome_colour_map, biome_map, land_mask, biome_colour_map, height_map = self.two(temperature_cells, precipitation_cells, biomes, vor_map)

        adjusted_height_map, biome_masks = self.three(masked_biome_colour_map, biome_map, land_mask, height_map)

        rivers_biome_colour_map, river_land_mask, adjusted_height_river_map = self.four(biome_map, vor_map, adjusted_height_map, land_mask, biome_colour_map)

        if kwargs.get('generateTrees', True):
            trees = self.five(river_land_mask, adjusted_height_river_map, biome_masks)
        else:
            trees = []

        # colour_map = apply_height_map(rivers_biome_colour_map, adjusted_height_river_map, adjusted_height_river_map, river_land_mask)
        # plt.imshow(colour_map[0])

        # im = Image.fromarray(colour_map[0].clip(0, 255).astype(np.uint8))
        # im.save("figures/10.png")

        colour_map = self.apply_height_map(rivers_biome_colour_map, adjusted_height_river_map, adjusted_height_river_map, river_land_mask)

        if kwargs.pop('showAtEnd', False):
            plt.imshow(colour_map[0])

            plt.show()
        gray_map = np.dot(colour_map[0][...,:3], [0.2989, 0.5870, 0.1140])  # Convert to grayscale
        norm_map = gray_map / 255.0  # Normalize to [0, 1]
        scaling_factor = 10
        height_map = norm_map * scaling_factor  # Convert to heights
        out = [[round(j) for j in i] for i in height_map]
        self.outs = ([out, colour_map, rivers_biome_colour_map, adjusted_height_river_map, river_land_mask, biome_masks], trees)

if __name__ == '__main__':
    size = 1500
    n = 256
    inp = input('Input nothing to use random seed, input "." to use a preset good seed, or input your own INTEGER seed > ')
    if inp == '':
        map_seed = randint(0, 999999)
    elif inp == '.':
        map_seed = 762345
    else:
        map_seed = int(inp)
    useall = input('Type anything here to show all steps in terrain generation, or leave this blank and press enter to just show the finished product. > ') != ''
    outs, trees = MapGen(size, map_seed, n, useall=useall, showAtEnd=True).outs
    print(outs[0])
