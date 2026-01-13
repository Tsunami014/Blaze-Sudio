Rect
OpList (Rotate & tranform)
> Line


Rect + Line @ (rotate + transform)


Rect + Rotate
WHAT IF THEY WERE SEPARATE? (So the above line is wrong)

((Line @ Rotate) + Rect) @ Transform

- What about rotating around centre?
Have different pivot modes:
    Origin - pivot around (0, 0)
    BoundingCenter - pivot around the centre of all the bounding boxes combined (points func with input matrix transform that can also be used in the display funcs)
    LocalCenter - pivot around the average of all the centres of each object
    MassCenter - pivot around the combined centre of each object divided by its area
    Custom - pivot around a custom point
}
And have e.g. Rotate(45, pp=Origin) or Rotate(10, pp=(5, 15))
- What about resize to specific size?




Problems:
1. Filling - apply (Op.py 146) (problems: np.fill, np.all)
2. Elipses/Circles - applyTrans (Draw.py 221) (partial problem: Making new arrays (np.array))
3. drawPolyLine - applyTrans (Draw.py 38)
4. drawRect - applyTrans (Draw.py 156) (partial problem: abs)
5. Op List applying - apply (base.py 146) (solution: compile entire class (also fixes slowness with 'fix'))

Also todo later: Make a gui game maker like godot
