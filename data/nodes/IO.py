# Value any@Value | Out #

def node(Value):
    return {'Out': Value}

# NumInp str@Name int@Default | Out #

def node(Name, Default):
    return {'Out': Default}

# TextInp str@Name str@Default | Out #

def node(Name, Default):
    return {'Out': Default}

# AnyInp str@Name any@Default | Out #

def node(Name, Default):
    return {'Out': Default}
