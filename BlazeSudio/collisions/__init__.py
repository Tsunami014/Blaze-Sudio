from BlazeSudio.collisions.collisions import *

class ShapeCombiner:
    @classmethod
    def bounding_box(cls, *shapes: Rect) -> Shapes:
        """
        Makes a new shape which is the bounding box of all the shapes combined.

        Returns:
            Shapes: A Shapes object containing one rectangle (if there are any shapes in shapes; else nothing) which is the bounding box around every input shape.
        """
        if not shapes:
            return Shapes()
        rs = [s.rect() for s in shapes]
        mins, maxs = [
            min(i[0] for i in rs),
            min(i[1] for i in rs)
        ], [
            max(i[2] for i in rs),
            max(i[3] for i in rs)
        ]
        return Shapes(Rect(
            *mins,
            maxs[0]-mins[0],
            maxs[1]-mins[1]
        ))

    @classmethod
    def to_rects(cls, *shapes: Rect) -> Shapes:
        """
        Combines adjacent rectangles.
        What this means is if you have 2 rectangles exactly touching they will combine to one
        ```
        +-+-+      +---+
        | | |  ->  |   |
        +-+-+      +---+
        ```
        This will only work if the combination would exactly encompass each shape without any room for air and would be a rectangle.
        For a more general combination, try using `.to_polygons()` instead.

        Returns:
            Shapes: A Shapes object with the rectangles from the input shapes combined
        """
        if not shapes:
            return Shapes()
        merged = True
        while merged:
            merged = False
            # Sort shapes by x-coordinate
            shapes = sorted(shapes, key=lambda x: x.x)
            outshapes1 = []
            
            while shapes:
                rect = shapes.pop(0)
                for i in shapes:
                    if rect.y == i.y and rect.h == i.h and (rect.x + rect.w >= i.x):
                        rect.w = max(rect.x + rect.w, i.x + i.w) - rect.x
                        shapes.remove(i)
                        merged = True
                        break
                outshapes1.append(rect)
            
            # Sort shapes by y-coordinate
            outshapes1 = sorted(outshapes1, key=lambda x: x.y)
            outshapes2 = []
            
            while outshapes1:
                rect = outshapes1.pop(0)
                for i in outshapes1:
                    if rect.x == i.x and rect.w == i.w and (rect.y + rect.h >= i.y):
                        rect.h = max(rect.y + rect.h, i.y + i.h) - rect.y
                        outshapes1.remove(i)
                        merged = True
                        break
                outshapes2.append(rect)
            
            shapes = outshapes2
        
        return Shapes(*shapes)

    @classmethod
    def to_polygons(cls, *shapes: Shape) -> Shapes:
        """
        Combine all the input shapes with a unary union.

        Returns:
            Shapes: The union of all the shapes.
        """
        if not shapes:
            return Shapes()
        def reformat(obj):
            if isinstance(obj, ClosedShape):
                return obj
            elif isinstance(s, Line):
                return Polygon(obj.p1, obj.p2, obj.p2, obj.p1)
            # TODO: More
        reform = [reformat(s) for s in shapes]
        shapes = [reform[i] for i in range(len(reform)) if reform[i]]
        outshps = []
        while shapes:
            s = shapes.pop(0)
            colls = [i.collides(s) for i in outshps]
            if any(colls):
                for i in range(len(colls)):
                    if colls[i]:
                        newpts = []
                        oshps = [s, outshps[i]]
                        lns = [j.toLines() for j in oshps]
                        direc = 1
                        check = 0
                        checked = []
                        # TODO: When objs are covered
                        ps = [any(k.collides(Point(*j)) for k in oshps if k != s) for j in s.toPoints()]
                        j = ps.index(False)
                        while True:
                            if (check, j) not in checked:
                                checked.append((check, j))
                                ln = lns[check][j]
                                p1 = ln.p1 if direc == 1 else ln.p2
                                p2 = ln.p2 if direc == 1 else ln.p1
                                newpts.append(p1)
                                wheres = []
                                for other in range(len(oshps)):
                                    if other != check:
                                        if ln.collides(oshps[other]):
                                            for k in range(len(lns[other])):
                                                if ln.collides(lns[other][k]):
                                                    ws = ln.whereCollides(lns[other][k])
                                                    wheres.extend(zip(ws, [(other, k) for _ in range(len(ws))]))
                                if wheres != []:
                                    wheres.sort(key=lambda x: (x[0][0]-p1[0])**2+(x[0][1]-p1[1])**2)
                                    newpts.append(wheres[0][0])
                                    # Correct direction handling
                                    if oshps[check].collides(Point(*lns[wheres[0][1][0]][wheres[0][1][1]].p2)):
                                        direc = -1
                                    else:
                                        direc = 1
                                    check = wheres[0][1][0]
                                    j = wheres[0][1][1]
                                else:
                                    newpts.append(p2)
                            else:
                                break
                            j = (j + direc) % len(lns[check])
                        outshps[i] = Polygon(*newpts)
            else:
                outshps.append(s)
        return Shapes(*outshps)
