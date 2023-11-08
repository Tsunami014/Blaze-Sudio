try:
    from graphics.GUI.inputbox import RESIZE_W, RESIZE_H, RESIZE_NONE, InputBox, renderTextCenteredAt
    from graphics.GUI.pyguix import *
    from graphics.GUI.textboxify import *
    from graphics.GUI.randomGUIelements import *
except ImportError:
    try:
        from GUI.inputbox import RESIZE_W, RESIZE_H, RESIZE_NONE, InputBox, renderTextCenteredAt
        from GUI.pyguix import *
        from GUI.textboxify import *
        from GUI.randomGUIelements import *
    except ImportError:
        from inputbox import RESIZE_W, RESIZE_H, RESIZE_NONE, InputBox, renderTextCenteredAt
        from pyguix import *
        from textboxify import *
        from randomGUIelements import *