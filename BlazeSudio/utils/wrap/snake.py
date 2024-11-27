import math
import BlazeSudio.collisions as colls

__all__ = [
    'Snake'
]

class Snake:
    def __init__(self, width):
        self.joints = [[0, 0], [width, 0]]
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
    
    def update(self):
        # Force parameters
        repulsion_strength = 0.3
        convergence_strength = 0.5

        # Apply repulsion between non-adjacent points
        for i in range(len(self.joints)):
            for j in range(i + 2, len(self.joints)):  # Only non-adjacent
                dx = self.joints[j][0] - self.joints[i][0]
                dy = self.joints[j][1] - self.joints[i][1]
                dist = math.sqrt(dx**2 + dy**2)
                if dist > 0:  # Avoid division by zero
                    force_mag = repulsion_strength / dist
                    fx, fy = force_mag * dx, force_mag * dy
                    self.joints[i] = (self.joints[i][0] - fx, self.joints[i][1] - fy)
                    self.joints[j] = (self.joints[j][0] + fx, self.joints[j][1] + fy)

        # Enforce joint distance constraints
        for i in range(len(self.joints) - 1):
            x, y = self.joints[i + 1][0] - self.joints[i][0], self.joints[i + 1][1] - self.joints[i][1]
            current_dist = math.sqrt(x**2 + y**2)
            if current_dist > 0:  # Avoid division by zero
                correction_factor = (self.jointDists[i] - current_dist) / current_dist
                dx = x * correction_factor / 2  # Split correction equally between the two points
                dy = y * correction_factor / 2
                self.joints[i] = (self.joints[i][0] - dx, self.joints[i][1] - dy)
                self.joints[i + 1] = (self.joints[i + 1][0] + dx, self.joints[i + 1][1] + dy)
        
        # Apply constraints and real segment properties
        for i in range(len(self.joints) - 1):
            x, y = self.joints[i + 1][0] - self.joints[i][0], self.joints[i + 1][1] - self.joints[i][1]
            ang = math.degrees(math.atan2(y, x)) - 90
            for constraint in self.segProps[i]:
                ang = constraint(ang, i, self)
            self.joints[i + 1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1] + self.jointDists[i]), ang)

        # Convergence force for endpoints
        start, end = self.joints[0], self.joints[-1]
        mid_point = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        convergence_force = (
            convergence_strength * (mid_point[0] - end[0]),
            convergence_strength * (mid_point[1] - end[1])
        )
        self.joints[0] = (self.joints[0][0] - convergence_force[0], self.joints[0][1] - convergence_force[1])
        self.joints[-1] = (self.joints[-1][0] + convergence_force[0], self.joints[-1][1] + convergence_force[1])
    
    def straighten(self):
        for i in range(len(self.joints)-1):
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), 90)
    
    def delete(self, idx):
        self.joints.pop(idx)
        if idx != len(self.joints):
            self.jointDists.pop(idx)
            self.segProps.pop(idx)
    
    def __iter__(self):
        return ((self.joints[i], self.joints[i+1]) for i in range(len(self.joints)-1))
    
    def __len__(self):
        return len(self.joints)-1
    
    def copy(self):
        s = Snake(10)
        s.joints = self.joints.copy()
        s.jointDists = self.jointDists.copy()
        s.segProps = [i.copy() for i in self.segProps]
        return s
