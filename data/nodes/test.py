# Add int@A int@B | int@Out #

def node(A, B):
    return {'Out': A + B}

# One | int@1 #
def node():
    return {'1': 1}

# Two | int@2 #
def node():
    return {'2': 2}
