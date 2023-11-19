try:
    from graphics.GUI.inputbox import *
    from graphics.GUI.pyguix import *
    from graphics.GUI.textboxify import *
    from graphics.GUI.randomGUIelements import *
except ImportError:
    try:
        from GUI.inputbox import *
        from GUI.pyguix import *
        from GUI.textboxify import *
        from GUI.randomGUIelements import *
    except ImportError:
        from inputbox import *
        from pyguix import *
        from textboxify import *
        from randomGUIelements import *