# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
# Edited by: Max Worrall
# Copyright 2022 J. Brandon George
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import io
import dataclasses as dc
import enum
import json as js
try:
    import pyguix.ui.themes as th
    import pyguix.ui.context as cx
    import pyguix.ui.settings as st
except ImportError:
    import graphics.GUI.pyguix.ui.themes as th
    import graphics.GUI.pyguix.ui.context as cx
    import graphics.GUI.pyguix.ui.settings as st 

# Constants:
DEFAULT_THEME='default.json'
DEFAULT_ENCODING='utf-8' 
ALIGNLEFT='Left'
ALIGNRIGHT='Right'
# DIMS:
DC_DIMS_WIDTH="width"
DC_DIMS_HEIGHT="height"
DC_RADIUS="radius"
#MessageBox:
MSGBOX='MessageBox'
MSGBOX_WIDTH=260
MSGBOX_HEIGHT=110
MSGBOX_TXT='OK'
MSGBOX_CANCELED_TXT='CANCELED'
MSGBOX_DEFAULT_JSONTHEME='MessageBox_default.json'
MSGBOX_DEFAULT_JSONSETTING='MessageBox.json'
MSGBOX_ISSUES_MSG='Issues loading supplied JSON MessageBox theme file. Loading default.'
MSGBOX_JUSTIFY_CENTER='center'
MSGBOX_JUSTIFY_LEFT='left'
#PopupMenu:
POPUP='PopupMenu'
POPUP_SEPCHAR="[&SEP]"
POPUP_SEPTEXT="-"
POPUP_DEFAULT_JSONCONTEXT='PopupMenu_default.json'
POPUP_DEFAULT_JSONSETTING='PopupMenu.json'
POPUP_ISSUES_MSG='Issues loading supplied JSON PopupMenu context file. Loading default.'
#SnapHUD:
SNAP='SnapHUD'
SNAP_DEFAULT_JSONSETTING='SnapHUD.json'
SNAP_DEFAULT_JSONCONTEXT='SnapHUD_default.json'
# Hamburger
HAM='Hamburger'
HAM_DEFAULT_JSONSETTING='Hamburger.json'
#global_cache:
POPUP_ACT="cat"
GLB_THEME="glbt"

# Enums:
PopupMenuItemType = enum.IntEnum('PopupMenuItemType','Action Separator')
SnapType = enum.IntEnum('SnapType', 'Closed Open Collasped Expanded')

# Dataclasses:
# Base dataclasses:
@dc.dataclass
class dimensions:
    width: int
    height: int
    radius: int

    def wh(self) -> tuple:
        """ returns tuple of (width,height) from loaded values """
        return (self.width,self.height)

    def new(v):
        ret = dimensions(
            width=int(v[DC_DIMS_WIDTH]),
            height=int(v[DC_DIMS_HEIGHT]),
            radius=int(v[DC_RADIUS])
        )
        return ret

@dc.dataclass
class color:
    RGB: tuple
    red: int
    green: int
    blue: int

    def new(v):
        r=v["RGB"]
        ret = color(
            RGB=r,
            red=int(r[0]),
            green=int(r[1]),
            blue=int(r[2])
        )
        return ret
    
    def astuple(v):
        nc = color.new(v["color"])
        ret = nc.RGB
        return ret

@dc.dataclass
class colors:
    default: tuple
    title: tuple
    text: tuple
    texttitle: tuple
    textsubtitle: tuple
    textdisabled: tuple
    button: tuple
    outline: tuple
    titleoutline: tuple
    buttonhover: tuple
    buttonhovertext: tuple

    def new(v):
        ret = colors(
            default=color.astuple(v["default"]),
            title=color.astuple(v["title"]),
            text=color.astuple(v["text"]),
            texttitle=color.astuple(v["text_title"]),
            textsubtitle=color.astuple(v["text_subtitle"]),
            textdisabled=color.astuple(v["text_disabled"]),
            button=color.astuple(v["button"]),
            outline=color.astuple(v["outline"]),
            titleoutline=color.astuple(v["title_outline"]),
            buttonhover=color.astuple(v["button_hover"]),
            buttonhovertext=color.astuple(v["button_hover_text"])
        )
        return ret

@dc.dataclass
class font:
    size: int
    type: str
    setbold: bool = False

    def new(v):
        return font(
            size=int(v["size"]),
            type=str(v["type"]),
            setbold=bool(v["set_bold"])
        )

@dc.dataclass
class text:
    size: int
    fonttype: str

    def new(v):
        ret = text(
            size=int(v["size"]),
            fonttype=v["fonttype"] if v["fonttype"] != "" else None
        )
        return ret

@dc.dataclass
class point:
    x: int
    y: int

    def new_astuple(v):
        ret = point(
            x=v[0],
            y=v[1]
        ).astuple()
        return ret
    
    def astuple(self):
        ret = (self.x,self.y)
        return ret

@dc.dataclass
class cords:
    tricords: tuple
    linecords: tuple

    def new(v):
        
        tcl = list()
        for p in v["tri_cords"]:
            np = point.new_astuple(p)
            tcl.append(np)

        lcl = list()
        for p in v["line_cords"]:
            np = point.new_astuple(p)
            lcl.append(np)

        ret = cords(
            tricords=tuple(tcl),
            linecords=tuple(lcl)
        )
        return ret

# SnapHUD dataclasses:
@dc.dataclass
class SnapButton:
    name: str
    cords: cords

    def new(v):
        ret = SnapButton(
            name=v["name"],
            cords=cords.new(v)
        )
        return ret

@dc.dataclass
class SnapHUDPart:
    id: str
    title: str
    function: str
    type: str

    def new(id,v):
        ret = SnapHUDPart(
            id=id,
            title=v["title"],
            function=v["function"],
            type=v["type"]
        )
        return ret

# MessageBox dataclasses:
@dc.dataclass
class MessageBoxVariables:
    titlemax: float
    messagemax: float
    fontsize: int
    outlinebuffer: int
    messagejustify: str
    messageheightbuffer: int

    def new(v):
        ret = MessageBoxVariables(
            titlemax=float(v["title_max"]),
            messagemax=float(v["message_max"]),
            fontsize=int(v["font_size"]),
            outlinebuffer=int(v["outline_buffer"]),
            messagejustify=MSGBOX_JUSTIFY_LEFT if v["message_justify"] == MSGBOX_JUSTIFY_LEFT else MSGBOX_JUSTIFY_CENTER,
            messageheightbuffer=int(v["message_height_buffer"]) 
        )
        return ret

@dc.dataclass
class MessageBoxTitle:
    dimensions: dimensions
    outlinebuffer: int
    fontsize: int
    textupcase: bool

    def new(v):
        ret = MessageBoxTitle(
            dimensions=dimensions.new(v["dimensions"]),
            outlinebuffer=int(v["outline_buffer"]),
            fontsize=int(v["font_size"]),
            textupcase=bool(v["text_upcase"])
        )
        return ret

@dc.dataclass
class MessageBoxCancelButton:
    surfacedimensions: dimensions
    circledimensions: dimensions
    circlebuffer: int
    circletext: str

    def new(v):
        ret = MessageBoxCancelButton(
            surfacedimensions=dimensions.new(v["surface"]["dimensions"]),
            circledimensions=dimensions.new(v["circle"]["dimensions"]),
            circlebuffer=int(v["circle"]["buffer"]),
            circletext=v["circle"]["default_text"]
        )
        return ret

@dc.dataclass
class MessageBoxButtons:
    dimensions: dimensions
    buffer: int
    returnbutton: int
    defaulttext: str
    outlinebuffer: int

    def new(v):
        ret = MessageBoxButtons(
            dimensions=dimensions.new(v["dimensions"]),
            buffer=int(v["buffer"]),
            returnbutton=int(v["return_button"]),
            defaulttext=v["default_text"],
            outlinebuffer=int(v["outline_buffer"])
        )
        return ret

# PopupMenu dataclasses:
@dc.dataclass
class PopupMenuItem:
    text: str
    type: PopupMenuItemType
    identity: str
    action: str
    enabled: bool
    clicked: bool = False

    def new(v,id):
        ret = PopupMenuItem(
            text=v["text"],
            type=PopupMenuItemType.Action if int(v["type"]) == 0 else PopupMenuItemType.Separator,
            identity=id,
            action=v["action"],
            enabled=bool(v["enabled"])
        )
        return ret

# Classes:
class jsonfile:
    
    def __init__(self,file_path,file):
        self.helper = helper()
        self.__file_path__ = file_path
        self.__file__ = file
        self.filebytes = self.__init__jsontheme_file__()
        self.__encode_type__ = js.detect_encoding(self.filebytes) # Enconding type match
        # TODO: (12/25/22) - Added logic to check against encoding constant and throw error if failed, and use default. 
        self.__jsdict__ = js.loads(self.filebytes) # json file load to dict class

    def __init__jsontheme_file__(self) -> bytes:
        """ internal function that read the path of the themes lib, and loads the passed in JSON theme file. (theme_name) """
        self.__path__ = self.helper.safe_path(self.__file_path__) 
        self.__file__ = ("%s/%s"  % (self.get_path(),self.__file__))
        try:
            f = io.FileIO(
                file=self.__file__,
                mode='r'
            )
        except:
            raise LookupError(("File missing %s [pyguix.__utils__.__help__.jsonfile]" % self.__file__))
        
        return f.readall() # read file to bytes object
    
    def __is_valid__(self) -> bool:
        """ internal function that must be implemented at named inherited theme class. base class returns false. """
        return False
    
    def __is_validitem__(self,dict,item) -> bool:
        ret = False
        
        if dict.__contains__(item):
            ret = True
        else:
            raise LookupError("Missing item: %s [pyguix.__utils__.__help__.jsonfile]" % (item))
        
        return ret
    
    def get_path(self) -> str:
        return self.__path__

    def get_dict(self) -> dict:
        return self.__jsdict__
    
class context(jsonfile):

    def __init__(self,context_name):
        super().__init__(cx.__path__.__str__(),context_name)

class settings(jsonfile):

    def __init__(self,setting_name):
        super().__init__(st.__path__.__str__(),setting_name)

class theme(jsonfile):

    def __init__(self,theme_name):
        super().__init__(th.__path__.__str__(),theme_name)

class PopupMenuContext(context):

    def __init__(self,context_name=POPUP_DEFAULT_JSONCONTEXT):
        super().__init__(context_name)

        if not self.__is_valid__():
            print(POPUP_ISSUES_MSG)
            super().__init__(POPUP_DEFAULT_JSONCONTEXT)
        
        self.__pmd__ = self.get_dict().get(POPUP)
        self.__dets__ = self.__pmd__.get("details")
        self.__act_cls__ = self.__dets__.get("actionclass")
        self.__tgtcls__ = self.__dets__.get("targetclasses")
        self.__mis__ = self.__pmd__.get("menuitems")
        self.__mia__ = []
        for m in self.__mis__.items():
            self.__mia__.append(PopupMenuItem.new(m[1].get("popupmenuitem"),m[0]))

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),POPUP)
        ret = ret and self.__is_validitem__(self.get_dict().get(POPUP),"details")
        ret = ret and self.__is_validitem__(self.get_dict().get(POPUP),"menuitems") 
        return ret
    
    def get_details(self):
        return self.__dets__
    def get_action_class(self):
        return self.__act_cls__
    def get_menuitems(self):
        return self.__mia__
    def find_menuitem_by_action(self,act) -> PopupMenuItem:
        ret = None
        for m in self.get_menuitems():
            if m.action == act:
                ret = m
                break
        return ret
    def get_target_classes(self):
        return self.__tgtcls__

class PopupMenuSettings(settings):

    def __init__(self, setting_name=POPUP_DEFAULT_JSONSETTING):
        super().__init__(setting_name)

        if not self.__is_valid__():
            print("Invalid PopupMenu JSON settings file. Will attempt to load default JSON setting file.")
            super().__init__(POPUP_DEFAULT_JSONSETTING)
        
        self.__pum__ = self.get_dict().get(POPUP)
        self.__vars__ = self.__pum__.get("variables")
        self.__outbuff__ = self.__vars__.get("outline_buffer")
        self.__dims__ = dimensions.new(self.__pum__.get("dimensions"))
        self.__mis__ = self.__pum__.get("menuitems")
        self.__misatbuff__ = self.__mis__.get("action_text_buffer")
        self.__mistxt__ = text.new(self.__mis__.get("text"))
        self.__mistxt_dims__ = dimensions.new(self.__mis__.get("dimensions"))

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),POPUP)
        ret = ret and self.__is_validitem__(self.get_dict().get(POPUP),"variables")
        ret = ret and self.__is_validitem__(self.get_dict().get(POPUP),"dimensions")
        ret = ret and self.__is_validitem__(self.get_dict().get(POPUP),"menuitems")
        return ret
    
    def get_outline_buffer(self):
        return self.__outbuff__
    def get_dimensions(self) -> dimensions:
        return self.__dims__
    def get_action_text_buffer(self):
        return self.__misatbuff__
    def get_menuitem_text(self) -> text:
        return self.__mistxt__
    def get_menuitem_dimensions(self) -> dimensions:
        return self.__mistxt_dims__

class MessageBoxSettings(settings):

    def __init__(self, setting_name=MSGBOX_DEFAULT_JSONSETTING):
        super().__init__(setting_name)

        if not self.__is_valid__():
            print("Invalid PopupMenu JSON settings file. Will attempt to load default JSON setting file.")
            super().__init__(MSGBOX_DEFAULT_JSONSETTING)
        
        self.__mbd__ = self.get_dict().get(MSGBOX)
        self.__vars__ = MessageBoxVariables.new(self.__mbd__.get("variables"))
        self.__title__ = MessageBoxTitle.new(self.__mbd__.get("title"))
        self.__cnlbtn__ = MessageBoxCancelButton.new(self.__mbd__.get("cancel_button"))
        self.__btns__ = MessageBoxButtons.new(self.__mbd__.get("buttons"))

    def __is_valid__(self) -> bool:
        """ Override version of is_valid for MessageBoxTheme(theme) class. """
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),MSGBOX)
        ret = ret and self.__is_validitem__(self.get_dict().get(MSGBOX),"variables")
        ret = ret and self.__is_validitem__(self.get_dict().get(MSGBOX),"title")
        ret = ret and self.__is_validitem__(self.get_dict().get(MSGBOX),"cancel_button")
        ret = ret and self.__is_validitem__(self.get_dict().get(MSGBOX),"buttons")
        return ret

    def get_variables(self) -> MessageBoxVariables:
        return self.__vars__
    def get_title(self) -> MessageBoxTitle:
        return self.__title__
    def get_cnlbtn(self) -> MessageBoxCancelButton:
        return self.__cnlbtn__
    def get_btns(self) -> MessageBoxButtons:
        return self.__btns__

class SnapHUDContext(context):
    
    def __init__(self,context_name=SNAP_DEFAULT_JSONCONTEXT):
        super().__init__(context_name)

        if not self.__is_valid__():
            print("Issues with SnapHUD context.json file loading. [pyguix.__utils__.__help__.py]")
            super().__init__(SNAP_DEFAULT_JSONCONTEXT)
        
        self.__pmd__ = self.get_dict().get(SNAP)
        self.__dets__ = self.__pmd__.get("details")
        self.__parts__ = self.__pmd__.get("parts")
        self.__paa__ = []
        for p in self.__parts__.items():
            self.__paa__.append(SnapHUDPart.new(p[0],p[1]))

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),SNAP)
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"details")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"parts") 
        return ret
    
    def get_details(self) -> dict:
        return self.__dets__
    def get_title(self):
        return self.get_details().get("title")
    def get_infoclass(self):
        return self.get_details().get("infoclass")
    def get_parts(self):
        return self.__paa__
    def get_part(self,p) -> SnapHUDPart:
        return p

class SnapHUDSettings(settings):
    
    def __init__(self, setting_name=SNAP_DEFAULT_JSONSETTING):
        super().__init__(setting_name)

        if not self.__is_valid__():
            print("Invalid SnapHUD JSON settings file. Will attempt to load default JSON setting file.")
            super().__init__(SNAP_DEFAULT_JSONSETTING)
        
        self.__shud__ = self.get_dict().get(SNAP)
        self.__vars__ = self.__shud__.get("variables")
        self.__dims__ = dimensions.new(self.__shud__.get("dimensions"))
        self.__btns__ = self.__shud__.get("buttons")
        self.__btns_closed__ = SnapButton.new(self.get_buttons().get("Closed"))
        self.__btns_open__ = SnapButton.new(self.get_buttons().get("Open"))
        self.__btns_dims__ = dimensions.new(self.__btns__.get("dimensions"))
        self.__btns_buff__ = self.__btns__.get("buffer")
        self.__btns_line_width__ = self.__btns__.get("line_width")
        self.__title__ = self.__shud__.get("title")
        self.__title_dims__ = dimensions.new(self.__title__.get("dimensions"))
        self.__title_font__ = font.new(self.__title__.get("font"))
        self.__part__ = self.__shud__.get("part")
        self.__part_title__ = self.__part__.get("title")
        self.__part_titledims__ = dimensions.new(self.__part_title__.get("dimensions"))
        self.__part_titlefont__ = font.new(self.__part_title__.get("font"))
        self.__part_body__ = self.__part__.get("body")
        self.__part_bodydims__ = dimensions.new(self.__part_body__.get("dimensions"))
        self.__part_bodyfont__ = font.new(self.__part_body__.get("font"))
        self.__align__ = self.__shud__.get("alignment")
        self.__buff__ = self.__align__.get("buffer")
        self.__buff_dims__ = dimensions.new(self.__buff__.get("dimensions"))
        self.__buff_buff__ = self.__buff__.get("buffer")
        
    def __is_valid__(self) -> bool:
        """ Override version of is_valid. """
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),SNAP)
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"variables")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"dimensions")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"buttons")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"title")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"part")
        ret = ret and self.__is_validitem__(self.get_dict().get(SNAP),"alignment")
        return ret
    
    def get_variables(self):
        return self.__vars__
    def get_dimensions(self) -> dimensions:
        return self.__dims__
    def get_buttons(self):
        return self.__btns__
    def get_button_closed(self) -> SnapButton:
        return self.__btns_closed__
    def get_button_open(self) -> SnapButton:
        return self.__btns_open__
    def get_button_dimensions(self) -> dimensions:
        return self.__btns_dims__
    def get_button_buffer(self):
        return self.__btns_buff__
    def get_button_line_width(self):
        return self.__btns_line_width__
    def get_title_dimensions(self) -> dimensions:
        return self.__title_dims__
    def get_title_font(self) -> font:
        return self.__title_font__
    def get_part(self):
        return self.__part__
    def get_part_title(self):
        return self.__part_title__
    def get_part_title_dimensions(self) -> dimensions:
        return self.__part_titledims__
    def get_part_title_font(self) -> font:
        return self.__part_titlefont__
    def get_part_body(self):
        return self.__part_body__
    def get_part_body_dimensions(self) -> dimensions:
        return self.__part_bodydims__
    def get_part_body_font(self) -> font:
        return self.__part_bodyfont__
    def get_aligment(self):
        return self.__align__
    def get_buffer_dimensions(self) -> dimensions:
        return self.__buff_dims__
    def get_buff_buffer(self):
        return self.__buff_buff__
    def get_start_direction(self) -> SnapType:
        try:
            ret = SnapType.__getitem__(self.get_variables().get("start_direction"))
            return ret
        except:
            raise LookupError("Invalid SnapHUD context.json supplied variable.start_direction conversion to SnapType enum value. Check context.json vsupplied varaible. [pyguix.__utils__.__help__.py]")

class HamburgerSettings(settings):

    def __init__(self, setting_name=HAM_DEFAULT_JSONSETTING):
        super().__init__(setting_name)
    
        if not self.__is_valid__():
            print("Invalid Hamburger JSON settings file. Will attempt to load default JSON setting file.")
            super().__init__(HAM_DEFAULT_JSONSETTING)

        self.__ham__ = self.get_dict().get(HAM)
        self.__vars__ = self.hamburger().get("variables")
        self.__dims__ = dimensions.new(self.variables().get("dimensions"))

    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),HAM)
        ret = ret and self.__is_validitem__(self.get_dict().get(HAM),"variables")
        ret = ret and self.__is_validitem__(self.get_dict().get(HAM)["variables"],"dimensions")
        return ret

    def hamburger(self) -> dict:
        return self.__ham__
    def variables(self) -> dict:
        return self.__vars__
    def dimensions(self) -> dimensions:
        return self.__dims__

class ElementTheme(theme):
    
    def __init__(self, theme_name=DEFAULT_THEME):
        super().__init__(theme_name)

        if not self.__is_valid__():
            print("Invlaid format for expected ElementTheme JSON file. Attempting to load default.")
            super().__init__(DEFAULT_THEME)
        
        self.__thm__ = self.get_dict().get("Theme")
        self.__clrs__ = colors.new(self.__thm__.get("colors"))
    
    def __is_valid__(self) -> bool:
        ret = super().__is_valid__()
        ret = self.__is_validitem__(self.get_dict(),"Theme")
        ret = ret and self.__is_validitem__(self.get_dict().get("Theme"),"colors")
        return ret
    
    def get_colors(self) -> colors:
        return self.__clrs__

class helper:

    def get_sepchar2text(self,s) -> str:
        ret = s
        if ret == POPUP_SEPCHAR:
            ret = POPUP_SEPTEXT
        return ret

    def str_rtrim(self,s,i) -> str:
        """ uses passed in string(s=) and trims len of string by provided int(i=) """
        ret = io.StringIO(s)
        ret = ret.read(s.__len__()-i)
        return ret
    
    def safe_path(self,s) -> str:
        """ uses passed in string(s=) and returns a usable path location by .lstrip() & .rstrip() str operations. """
        ret = s.rstrip("']")
        ret = ret.lstrip("['")
        return ret
    
    # TODO: Clean up following seciton: ***********************
    def init_reg_json2pmas(self) -> dict:
        ret = dict()
        jsonfiles = cx.get_json_files()
        for f in jsonfiles:
            c = context(f)
            if c.__jsdict__.__contains__("PopupMenu"):
                pmc = PopupMenuContext(f)
                if not ret.__contains__(pmc.get_action_class()):
                    ret[pmc.get_action_class()] = f
        
        return ret

    
    def init_reg_pmas(self) -> dict:

        ret = dict()
        # Load files in context:
        jsonfiles = cx.get_json_files()
        for f in jsonfiles:
            c = context(f)
            if c.__jsdict__.__contains__("PopupMenu"):
                pmc = PopupMenuContext(f)
                if not ret.__contains__(pmc.get_action_class()):
                    ret[pmc.get_action_class()] = None
        
        return ret
    # NOTE: END TODO Clean up section *************************************