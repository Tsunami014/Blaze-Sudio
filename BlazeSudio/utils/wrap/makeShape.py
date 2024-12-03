import math
import BlazeSudio.collisions as colls

__all__ = [
    'MakeShape',
    'ShapeFormatError'
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

class MakeShape:
    def __init__(self, width):
        self.joints = [(0, 0), (width, 0)]
        self.jointDists = [width]
        self.segProps = [[]]
    
    @property
    def segments(self) -> list[tuple[tuple[int], tuple[int]]]:
        return [(self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1)]
    
    @property
    def collSegments(self) -> list[colls.Line]:
        return [colls.Line(self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1)]
    
    @property
    def width(self):
        return sum(
            math.sqrt((self.joints[i][0]-self.joints[i+1][0])**2+(self.joints[i][1]-self.joints[i+1][1])**2) for i in range(len(self.joints)-1)
        )
    
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
                self.segProps = [*self.segProps[:i], self.segProps[i].copy()]
                break
        else:
            x, y = self.joints[i+1][0]-self.joints[i][0], self.joints[i+1][1]-self.joints[i][1]
            ang = math.degrees(math.atan2(y, x))-90
            newdist = newWidth-d
            self.joints.append(colls.rotate(self.joints[-1], (self.joints[-1][0], self.joints[-1][1]+newdist), ang))
            self.jointDists.append(newdist)
            self.segProps.append([])
    
    def insert_straight(self, x):
        self.straighten()
        if self.joints[0][-1] < x < self.joints[0][0]:
            if x in (i[0] for i in self.joints):
                return False
            for idx in range(len(self.joints)-1):
                if self.joints[idx+1][0] < x:
                    self.joints.insert(idx+1, (x, self.joints[idx][1]))
                    self.segProps.insert(idx+1, self.segProps[idx].copy())
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

    def _find_radius(self, epsilon=0.0000002, returnIterations=False):
        min_theta = 1.0 - epsilon
        max_theta = 1.0 + epsilon

        ds = self.jointDists

        sum_length = sum(ds)
        max_length = max(ds)

        min_radius = 0.5 * max_length
        max_radius = 0.5 * sum_length

        iterations = 0

        while True:
            sum_theta = 0.0
            iterations += 1
            radius = 0.5 * (min_radius + max_radius)

            for L in ds:
                sum_theta += theta(L, radius)

            sum_theta /= 2 * math.pi

            if min_theta <= sum_theta <= max_theta:
                break
            elif sum_theta < 1.0:
                max_radius = radius
            else:
                min_radius = radius

        if returnIterations:
            return radius, iterations

        return radius
    
    def makeShape(self): # Thanks SO MUCH to https://math.stackexchange.com/questions/1930607/maximum-area-enclosure-given-side-lengths
        line_lengths = self.jointDists

        if len(line_lengths) < 3:
            raise ShapeFormatError("Need at least three line lengths.")

        max_length = max(line_lengths)
        sum_length = sum(line_lengths)

        if max_length > sum_length - max_length:
            raise ShapeFormatError("Not a valid polygon; one of the line segments is too long.\n")

        radius = self._find_radius(line_lengths)

        phi = -0.5 * theta(line_lengths[0], radius)

        x0 = radius * math.cos(phi)
        y0 = -radius * math.sin(phi)

        njs = []

        for L in line_lengths:
            x = x0 - radius * math.cos(phi)
            y = y0 + radius * math.sin(phi)
            phi += theta(L, radius)
            njs.append((x, y))
        self.joints = njs + [(0, 0)]

    def straighten(self):
        for i in range(len(self.joints)-1):
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), 90)
    
    def delete(self, idx):
        self.joints.pop(idx)
        if idx != len(self.joints):
            #self.jointDists[idx-1] += self.jointDists.pop(idx)
            self.jointDists.pop(idx)
            self.segProps.pop(idx)
    
    def __iter__(self):
        return ((self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1))
    
    def __len__(self):
        return len(self.joints)-1
    
    def copy(self):
        s = MakeShape(10)
        s.joints = self.joints.copy()
        s.jointDists = self.jointDists.copy()
        s.segProps = [i.copy() for i in self.segProps]
        return s
