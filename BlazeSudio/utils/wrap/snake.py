import math
import BlazeSudio.collisions as colls

__all__ = [
    'Snake'
]

class Snake:
    def __init__(self, width):
        self.joints = [[0, 0], [width, 0]]
        self.jointDists = [width]
    
    @property
    def segments(self):
        return [(self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1)]
    
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
                break
        else:
            x, y = self.joints[i+1][0]-self.joints[i][0], self.joints[i+1][1]-self.joints[i][1]
            ang = math.degrees(math.atan2(y, x))-90
            newdist = newWidth-d
            self.joints.append(colls.rotate(self.joints[-1], (self.joints[-1][0], self.joints[-1][1]+newdist), ang))
            self.jointDists.append(newdist)
    
    def insert_straight(self, x):
        self.straighten()
        if self.joints[0][-1] < x < self.joints[0][0]:
            for idx in range(len(self.joints)-1):
                if self.joints[idx+1][0] < x:
                    self.joints.insert(idx+1, (x, self.joints[idx][1]))
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
    
    def update(self):
        for i in range(len(self.joints)-1):
            x, y = self.joints[i+1][0]-self.joints[i][0], self.joints[i+1][1]-self.joints[i][1]
            ang = math.degrees(math.atan2(y, x))-90
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), ang)
    
    def straighten(self):
        for i in range(len(self.joints)-1):
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), 90)
    
    def __iter__(self):
        return ((self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1))
    
    def __len__(self):
        return len(self.joints)-1
    
    def copy(self):
        s = Snake(self.width, self.joints.copy())
        s.offsets = self.offsets
        return s

"""class Snake:
    def __init__(self, width, joints=[]):
        self.width = width
        self.offsets = [[0, 0], [0, 0], [0, 0]]
        self.joints = joints
    
    @property
    def segments(self):
        l = []
        l2 = [0, *self.joints, self.width]
        for i in range(len(l2)-1):
            l.append((l2[i], l2[i+1]))
        return l
    
    def __iter__(self):
        return iter(self.segments)
    
    def copy(self):
        s = Snake(self.width, self.joints.copy())
        s.offsets = self.offsets
        return s"""
