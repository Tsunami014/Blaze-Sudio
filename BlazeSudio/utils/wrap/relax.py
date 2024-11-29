import math, random
import BlazeSudio.collisions as colls

__all__ = [
    'Relaxation'
]

class Relaxation:
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
    
    def update(self):
        if all(i[1] == self.joints[0][1] for i in self.joints):
            self.unstraighten()
            return # self.unstraighten() calls self.update() to keep it correct, so we don't need to continue now
        
        repulsion_strength = 0.7
        
        self.joints[-1] = self.joints[0]
        newjs = self.joints.copy()
        for i in range(len(self.joints)-1):
            # Push away from others
            idx = 0
            for seg in self.collSegments:
                if seg.p1 != self.joints[i] and seg.p2 != self.joints[i]:
                    closestP = seg.closestPointTo(colls.Point(*self.joints[i]))
                    dx = closestP[0] - self.joints[i][0]
                    dy = closestP[1] - self.joints[i][1]
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist > 0: # To avoid division by zero
                        force_mag = repulsion_strength/dist
                        force_mag *= abs(i-idx)/(len(self.joints)/2)
                        fx, fy = force_mag*dx, force_mag*dy
                        newjs[i] = (self.joints[i][0]-fx, self.joints[i][1]-fy)
                        newjs[idx] = (self.joints[idx][0]+fx, self.joints[idx][1]+fy)
                        newjs[idx+1] = (self.joints[idx+1][0]+fx, self.joints[idx+1][1]+fy)
                    idx += 1
        
        # self.joints = newjs.copy()
        
        # for _ in range(10):
        #     # Split the difference between the 2 points
        #     for i in range(len(self.joints) - 1):
        #         x, y = self.joints[i + 1][0] - self.joints[i][0], self.joints[i + 1][1] - self.joints[i][1]
        #         dist = math.sqrt(x**2 + y**2)
        #         # ang = math.degrees(math.atan2(y, x)) - 90
        #         if dist > 0:  # Avoid division by zero
        #             # ang2 = ang
        #             # for constraint in self.segProps[i]:
        #             #     ang2 = constraint.angle(ang2, i, self)
        #             correction_factor = (self.jointDists[i] - dist) / dist
        #             # dx = (x+math.cos(ang-ang2)*dist) * correction_factor / 2  # Split correction equally between the two points
        #             # dy = (y+math.sin(ang-ang2)*dist) * correction_factor / 2
        #             dx = x * correction_factor / 2  # Split correction equally between the two points
        #             dy = y * correction_factor / 2
        #             newjs[i] = (self.joints[i][0] - dx, self.joints[i][1] - dy)
        #             newjs[i + 1] = (self.joints[i + 1][0] + dx, self.joints[i + 1][1] + dy)
            
        # Apply the constraints
        
        # Bring everything else together to keep at the same distance (TODO: sharing the distance between the points around i)

        # Restrain each joint one by one, pulling both sides of the chain inwards from the displacement to keep them the same
        # self.joints = newjs.copy()
        # for i in range(len(self.joints)):
        #     i = (i+len(self.joints)//2) % len(self.joints) # Start from the centre
        #     for j in range(i, len(self.joints)-1):
        #         x, y = self.joints[j+1][0] - self.joints[j][0], self.joints[j+1][1] - self.joints[j][1]
        #         ang = math.degrees(math.atan2(y, x))-90
        #         for constraint in self.segProps[j]:
        #             ang = constraint.angle(ang, j, self)
        #         newjs[j + 1] = colls.rotate(self.joints[j], (self.joints[j][0], self.joints[j][1] + self.jointDists[j]), ang)
        #     for j in range(i, 0, -1):
        #         x, y = self.joints[j][0] - self.joints[j-1][0], self.joints[j][1] - self.joints[j-1][1]
        #         ang = math.degrees(math.atan2(y, x))-90
        #         for constraint in self.segProps[j-1]:
        #             ang = constraint.angle(ang, j-1, self)
        #         newjs[j-1] = colls.rotate(self.joints[j], (self.joints[j][0], self.joints[j][1] - self.jointDists[j-1]), ang)

        self.joints = newjs

        #Pulls both sides inwards so it's equal 
        # for i in range(len(self.joints) - 1):
        #     diffs = [(0, 0), (0, 0)]
        #     if i != 0:
        #         x, y = self.joints[i][0] - self.joints[i-1][0], self.joints[i][1] - self.joints[i-1][1]
        #         ang = math.degrees(math.atan2(y, x)) - 90
        #         for constraint in self.segProps[i-1]:
        #             ang = constraint.angle(ang, i-1, self)
        #         new = colls.rotate(self.joints[i-1], (self.joints[i-1][0], self.joints[i-1][1] + self.jointDists[i-1]), ang)
        #         diffs[0] = (new[0]-self.joints[i-1][0], new[1]-self.joints[i-1][1])
        #     x, y = self.joints[i+1][0] - self.joints[i][0], self.joints[i+1][1] - self.joints[i][1]
        #     ang = math.degrees(math.atan2(y, x)) - 90
        #     for constraint in self.segProps[i]:
        #         ang = constraint.angle(ang, i, self)
        #     new = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1] + self.jointDists[i]), ang)
        #     diffs[1] = (new[0]-self.joints[i][0], new[1]-self.joints[i][1])

        #     # diffs = [(diffs[0][0]*connection_strength, diffs[0][1]*connection_strength), (diffs[1][0]*connection_strength, diffs[1][1]*connection_strength)]

        #     self.joints = [(a[0]-diffs[0][0], a[1]-diffs[0][1]) for a in self.joints[:i]] + [self.joints[i]] + [(a[0]-diffs[1][0], a[1]-diffs[1][1]) for a in self.joints[i+1:]]
        
        # Apply constraints and real segment properties
        # TODO: Instead of this, have in the loop above pulling the rest of the shape together instead of the start pulling the next one etc.

        # Restrain each segment separately (?) then average and stick them together
        # segs = self.segments
        # for idx, seg in enumerate(segs):
        #     x, y = seg[1][0] - seg[0][0], seg[1][1] - seg[0][1]
        #     ang = math.degrees(math.atan2(y, x))-90
        #     for constraint in self.segProps[idx]:
        #         ang = constraint.angle(ang, idx, self)
        #     segs[idx] = (seg[0], colls.rotate(seg[0], (seg[0][0], seg[0][1] + self.jointDists[idx]), ang))
        
        # self.joints = [segs[0][0]] + [
        #     ((i[1][0] + j[0][0]) / 2, (i[1][1] + j[0][1]) / 2) for i, j in zip(segs[:-1], segs[1:])
        # ] + [segs[-1][1]]
        
        # Restrain the joints one by one
        for i in range(len(self.joints) - 1):
            x, y = self.joints[i+1][0] - self.joints[i][0], self.joints[i+1][1] - self.joints[i][1]
            ang = math.degrees(math.atan2(y, x))-90
            for constraint in self.segProps[i]:
                ang = constraint.angle(ang, i, self)
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1] + self.jointDists[i]), ang)
    
    def straighten(self):
        for i in range(len(self.joints)-1):
            self.joints[i+1] = colls.rotate(self.joints[i], (self.joints[i][0], self.joints[i][1]+self.jointDists[i]), 90)
    
    def unstraighten(self):
        totd = self.joints[0][0]-self.joints[-1][0]
        if totd == 0:
            return
        d = totd / 2
        centre = (
            sum(i[0] for i in self.joints)/len(self.joints),
            sum(i[1] for i in self.joints)/len(self.joints),
        )
        self.joints = [
            colls.rotate(centre, (centre[0], centre[1]+d), ((i[0]-self.joints[-1][0])/totd)*360) for i in self.joints
        ]
        self.update()
    
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
        s = Relaxation(10)
        s.joints = self.joints.copy()
        s.jointDists = self.jointDists.copy()
        s.segProps = [i.copy() for i in self.segProps]
        return s
