try:
    from graphics.GUI.inputbox import RESIZE_W, RESIZE_H, RESIZE_NONE, InputBox, renderTextCenteredAt
    from graphics.GUI.pyguix import *
    from graphics.GUI.textboxify import *
except ImportError:
    from inputbox import RESIZE_W, RESIZE_H, RESIZE_NONE, InputBox, renderTextCenteredAt
    from pyguix import *
    from textboxify import *