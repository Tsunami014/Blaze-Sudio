__all__ = [
    'BaseConstraint',
    'OverConstrainedError',

    'SpecificAngle'
]

class OverConstrainedError(ValueError):
    """
    The expression has been overly constrained and will not output a closed circle!
    """
    def __init__(self): # TODO: Add info
        super().__init__(self.__doc__)

class BaseConstraint:
    def __str__(self):
        return f'<{__class__.__name__} Constraint>'
    def __repr__(self): return str(self)

class SpecificAngle(BaseConstraint):
    def __init__(self, angle):
        self.angle = angle
    
    def __call__(self, ang, idx, main):
        return round((ang-self.angle) / 180) * 180 + self.angle
    
    def __str__(self):
        return f'<SpecificAngle Constraint @ {self.angle}>'
