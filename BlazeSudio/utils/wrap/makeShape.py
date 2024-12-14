import math
import numpy as np
import pygame
import BlazeSudio.collisions as colls
from BlazeSudio.utils.wrap.skeleton import FastSkeleton

__all__ = [
    'MakeShape',
    'ShapeFormatError',
    'OverConstrainedError'
]

def theta(L, r):
    return 2.0 * math.asin(0.5 * L / r)

def d_theta(L, r):
    r2 = r * r
    return -2.0 * L / (r2 * math.sqrt(4.0 - L * L / r2))

class ShapeFormatError(ValueError):
    """
    The shape is not in the correct format!
    """

class OverConstrainedError(ValueError):
    """
    The expression has been overly constrained and will not output a closed circle!
    """

class MakeShape:
    def __init__(self, width):
        self.joints = [(0, 0), (width, 0)]
        self.jointDists = [width]
        self.setAngs = [None]
        self.lastRadius = None
    
    @property
    def segments(self) -> list[tuple[tuple[int], tuple[int]]]:
        return [(self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1)]
    
    @property
    def collSegments(self) -> list[colls.Line]:
        return [colls.Line(self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1)]
    
    @property
    def width(self):
        return sum(self.jointDists)
    
    @width.setter
    def width(self, newWidth):
        d = 0
        for i in range(len(self.joints)-1):
            oldD = d
            x, y = self.joints[i+1][0]-self.joints[i][0], self.joints[i+1][1]-self.joints[i][1]
            d += math.sqrt(x**2+y**2)
            if d > newWidth:
                ang = math.degrees(math.atan2(y, x))-90
                newdist = newWidth-d-oldD
                self.joints = [*self.joints[:i], colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+newdist), ang)]
                self.jointDists = [*self.jointDists[:i], newdist]
                self.setAngs = [*self.setAngs[:i], self.setAngs[i]]
                break
        else:
            x, y = self.joints[i+1][0]-self.joints[i][0], self.joints[i+1][1]-self.joints[i][1]
            ang = math.degrees(math.atan2(y, x))-90
            newdist = newWidth-d
            self.joints.append(colls.rotate(self.joints[-1], (self.joints[-1][0], self.joints[-1][1]+newdist), ang))
            self.jointDists.append(newdist)
            self.setAngs.append(None)
    
    def insert_straight(self, x):
        self.straighten()
        if self.joints[-1][0] < x < self.joints[0][0]:
            if x in (i[0] for i in self.joints):
                return False
            for idx in range(len(self.joints)-1):
                if self.joints[idx+1][0] < x:
                    self.joints.insert(idx+1, (x, self.joints[idx][1]))
                    self.setAngs.insert(idx+1, self.setAngs[idx])
                    self.recalculate_dists()
                    return True
        return False
    
    def recalculate_dists(self):
        prevj = None
        self.jointDists = []
        for j in self.joints:
            if prevj is None:
                prevj = j
                continue
            self.jointDists.append(math.sqrt((prevj[0]-j[0])**2+(prevj[1]-j[1])**2))
            prevj = j
    
    def recentre(self, newx, newy):
        centre = (
            sum(i[0] for i in self.joints)/len(self.joints),
            sum(i[1] for i in self.joints)/len(self.joints),
        )
        diff = (
            newx-centre[0],
            newy-centre[1],
        )
        self.joints = [
            (i[0]+diff[0], i[1]+diff[1]) for i in self.joints
        ]

    def _find_radius(self, epsilon=0.0000002, max_iters=1000, returnIterations=False):
        min_theta = 1.0 - epsilon
        max_theta = 1.0 + epsilon

        desired_angle = 360
        DA_ratio = desired_angle / 360

        sum_length = sum(self.jointDists)
        max_length = max(self.jointDists)

        min_radius = 0.5 * max_length
        max_radius = (0.5 * sum_length) / DA_ratio

        iterations = 0

        while True:
            sum_theta = 0.0
            iterations += 1
            radius = 0.5 * (min_radius + max_radius)

            for L in self.jointDists:
                sum_theta += theta(L, radius)

            sum_theta /= (2 * math.pi) * DA_ratio

            if min_theta <= sum_theta <= max_theta:
                break
            elif sum_theta < 1.0:
                max_radius = radius
            else:
                min_radius = radius
            
            if max_iters is not None and iterations > max_iters:
                if sum_theta < 1.0:
                    too = 'small'
                else:
                    too = 'large'
                raise TimeoutError(
                    'Maximum iterations reached! Radius was too %s. Couldn\'t put the points on a circle, try a different arrangement of points'%too
                )

        self.lastRadius = radius

        if returnIterations:
            return radius, iterations

        return radius
    
    def makeShape(self): # Thanks SO MUCH to https://math.stackexchange.com/questions/1930607/maximum-area-enclosure-given-side-lengths
        # TODO: Multiple constraints in a row
        # TODO: Paralell constraints

        if len(self.jointDists) < 3:
            raise ShapeFormatError("Need at least three line lengths.")

        max_length = max(self.jointDists)
        sum_length = sum(self.jointDists)

        if max_length > sum_length - max_length:
            raise ShapeFormatError("Not a valid polygon; one of the line segments is too long.\n")

        radius = self._find_radius()

        startingi = 0
        got = 0
        for i in range(len(self.setAngs)):
            if self.setAngs[i] is not None:
                if got == 0:
                    startingi = i
                    got = 1
                elif got == 2:
                    raise OverConstrainedError(
                        'Cannot have multiple constraints not in a row!'
                    )
            elif got == 1:
                got = 2
        
        phi = -0.5 * theta(self.jointDists[startingi], radius)
        if got != 0:
            phi += math.radians(self.setAngs[startingi])

        x0 = radius * math.cos(phi)
        y0 = -radius * math.sin(phi)

        njs = []

        for i in range(len(self.jointDists)):
            L = self.jointDists[(i+startingi) % len(self.jointDists)]
            x = x0 - radius * math.cos(phi)
            y = y0 + radius * math.sin(phi)
            phi += theta(L, radius)
            njs.append((x, y))
        self.joints = [njs[i-startingi] for i in range(len(njs))] + [njs[-startingi]]

    def straighten(self):
        self.lastRadius = None
        for i in range(len(self.joints)-1):
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), 90)
    
    def generateBounds(self, hei, large=True, main=True, small=True):
        if self.lastRadius is None:
            self.makeShape()
        
        collObj = None
        
        if large:
            collObj = colls.Polygon(*self.joints)
            shapelyObj = colls.collToShapely(collObj)
            lgeObj = colls.shapelyToColl(shapelyObj.buffer(hei))
        else:
            lgeObj = None
        
        if main:
            if collObj is None:
                collObj = colls.Polygon(*self.joints)
            mnObj = collObj
        else:
            mnObj = None
        
        if small:
            xs, ys = zip(*self.joints)
            minx, miny = min(xs), min(ys)
            sur = pygame.Surface((max(xs)-minx, max(ys)-miny))
            pygame.draw.polygon(sur, (255, 255, 255), [(i[0]-minx, i[1]-miny) for i in self.joints])
            arr = pygame.surfarray.pixels3d(sur)
            skel = FastSkeleton()(np.all(arr == np.array([255, 255, 255]), axis=-1))
            smlObj = colls.Shapes(
                *[
                    colls.Line((int(u[0])+minx, int(u[1])+miny), (int(v[0])+minx, int(v[1])+miny)) for u, v in skel.edges()
                ]
            )
            # smlObj = colls.NoShape()
            # centre = colls.shapelyToColl(pygeoops.centerline(shapelyObj, -0.5))
            # if not colls.checkShpType(centre, colls.ShpGroups.GROUP):
            #     centre = colls.Shapes(centre)
        else:
            smlObj = None
        
        return lgeObj, mnObj, smlObj
    
    def delete(self, idx):
        self.lastRadius = None
        self.joints.pop(idx)
        if idx != len(self.joints):
            #self.jointDists[idx-1] += self.jointDists.pop(idx)
            self.jointDists.pop(idx)
            self.setAngs.pop(idx)
    
    def __iter__(self):
        return ((self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1))
    
    def __len__(self):
        return len(self.joints)-1
    
    def copy(self):
        s = MakeShape(10)
        s.joints = self.joints.copy()
        s.jointDists = self.jointDists.copy()
        s.setAngs = self.setAngs.copy()
        s.lastRadius = self.lastRadius
        return s
