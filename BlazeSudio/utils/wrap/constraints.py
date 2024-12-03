__all__ = [
    'BaseConstraint',
    'OverConstrainedError',

    'SpecificAngle'
]

class OverConstrainedError(ValueError):
    """
    The expression has been overly constrained and will not output a closed circle!
    """

class BaseConstraint:
    def angle(self, ang, idx, main):
        return ang
    
    def __str__(self):
        return f'<{__class__.__name__} Constraint>'
    def __repr__(self): return str(self)

class SpecificAngle(BaseConstraint):
    def __init__(self, angle):
        self.ang = angle
    
    def angle(self, ang, idx, main):
        return round((ang-self.ang) / 180) * 180 + self.ang
    
    def __str__(self):
        return f'<SpecificAngle Constraint @ {self.ang}>'
