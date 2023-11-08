# PyGames-pyguix
# made with: pygame 2.1.2 (SDL 2.0.16, Python 3.10.6)
# using: vscode ide
# By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay
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

import pygame
try:
    import graphics.GUI.pyguix.utils as utils
except ImportError:
    try:
        import GUI.pyguix.utils as utils
    except ImportError:
        import pyguix.utils as utils

uth = utils.helper()
# NOTE: When an action class is created, the base scope class adds its targetclasses as keys
# to the following dict(), with a value of the action class instance to use 
reg_json2pmas = uth.init_reg_json2pmas()
reg_pmas = uth.init_reg_pmas()
reg_tc2pma = dict()

# NOTE: START global_cache section **********************
__global_cache__ = dict()

# spritecache for global_cache
def clear_spritecache():
    """ Resets global_cache for Sprite active target executing PopupMenuActions. """
    __global_cache__[utils.POPUP_ACT]=None
def spritecache(v=None):
    """ When v=Sprite, then passed in Sprite is acted upon for executing PopupMenuActions class. Call clear_spritecache() to clear cache. """
    if v != None:
        __global_cache__[utils.POPUP_ACT]=v
    elif not __global_cache__.keys().__contains__(utils.POPUP_ACT):
        # Initialize global_cache[utils.POPUP_ACT]
        clear_spritecache()
    return __global_cache__[utils.POPUP_ACT] 

# themecache for global_cache
def clear_globaltheme():
    __global_cache__[utils.GLB_THEME]=None
def globaltheme(v=None):
    """ Set/Get theme for ui elements. """
    if v != None:
        __global_cache__[utils.GLB_THEME]=v
    elif not __global_cache__.keys().__contains__(utils.GLB_THEME):
        # Initialize global_cache[utils.GLB_THEME]
        clear_globaltheme()
    return __global_cache__[utils.GLB_THEME]

# context for global_cache
def clear_globalcontext(k):
    __global_cache__[k]=None
def globalcontext(k,v=None):
    if v != None:
        __global_cache__[k]=v
    elif not __global_cache__.keys().__contains__(k):
        clear_globalcontext(k)
    return __global_cache__[k]
# END global_cache section ******************************

# Classes:
class MessageBox(pygame.sprite.Sprite):
    """ pyguix.ui.elements.MessageBox ui class. Instance crated and called to with flexible options for displaying supplied data and information. Ability to supply MessageBox.buttons, and react upon button value clicked post rendering of MessageBox and user intercation. """

    def __init__(
            self,
            window,
            message_text=utils.MSGBOX_TXT,
            title=utils.MSGBOX_TXT,
            buttons=(utils.MSGBOX_TXT,),
            width=utils.MSGBOX_WIDTH,
            height=utils.MSGBOX_HEIGHT,
            event_list=None,
            theme=utils.DEFAULT_THEME,
            settings=utils.MSGBOX_DEFAULT_JSONSETTING,
            rg=None
        ):
        
        super().__init__()

        # Init MessageBox JSON Settings file:
        self.settings = self.__init_settings(settings)

        # Init MessageBox JSON theme file:
        self.theme = self.__init_theme__(theme)

        # Init MessageBox dimensions and variables:
        self.__init_messagebox_dimesions__(window,width,height,buttons,message_text,title,event_list)
        
        # MessageBox outline surface:
        self.box_outline_surf = self.__get_box_outline_surf__()
        
        # MessageBox (inner) surface:
        self.box_surf = self.__get_box_surf__()
        
        # Init title details:
        self.__init_title_details__()

        # Init button details. (includes cancel button.):
        self.__init_button_details__()

        # Blit message text surface:
        self.msgtext_surf = self.__get_message_text__()
        self.__blit_msgtext_surf__()
        
        # Blit title outline surface:
        self.__blit_title_outline_surf__()

        # Add MessageBox to sprite.RenderUpdates() group.:
        self.image = self.box_outline_surf
        self.rect = pygame.Rect((self.box_outline_pos+(self.box_outline_width,self.box_outline_height)))
        
        if type(rg) == type(pygame.sprite.RenderUpdates()):
            self.rg = rg
        else:
            self.rg = pygame.sprite.RenderUpdates()

        self.rg.add(self)

        # Check if event_list is sent in, if so 'self-contained' MessageBox mode executing.:
        if self.event_list != None:
            while self.wait(self.event_list):
                self.event_list = pygame.event.get()

    def __init_settings(self,settings) -> utils.MessageBoxSettings:
        return utils.MessageBoxSettings(settings)
    
    def __init_theme__(self,theme) -> utils.ElementTheme:
        """ internal function that loads passed in (or default) MessageBox JSON theme. """
        if globaltheme() != None:
            theme = globaltheme()
        return utils.ElementTheme(theme)

    def __init_messagebox_dimesions__(self,window,width,height,buttons,message_text,title,event_list):
        """ internal function that initializes the MessageBox dimensions, and passed in variables. """
        self.__wait__ = True
        self.__canceled__ = False
        self.window = window
        self.box_width = width 
        self.box_outline_width = self.box_width+self.settings.get_variables().outlinebuffer
        self.box_height= height
        self.box_outline_height = self.box_height+self.settings.get_variables().outlinebuffer
        self.buttons = buttons
        self.message_text = self.__message_text_max__(message_text)
        self.title = self.__title_text_max__(title)
        self.w_width,self.w_height = window.get_size()
        self.event_list = event_list
    
    def __init_title_details__(self):
        """ internal function that initializes the title, title surface and title outline surface details. """
        self.title_width = self.box_width
        self.title_outline_width = self.title_width
        self.title_height = self.settings.get_title().dimensions.height
        self.title_outline_height = self.title_height + self.settings.get_title().outlinebuffer
        self.title_outline_surf = pygame.Surface((self.title_outline_width,self.title_outline_height))
        self.title_outline_surf.fill(self.theme.get_colors().titleoutline)
        self.title_surf = pygame.Surface((self.title_width,self.title_height))
        self.title_surf.fill(self.theme.get_colors().title)
        # TODO: (12/26/22) Finaize custom font
        title_font = pygame.font.Font(None,self.settings.get_title().fontsize)
        title_font.set_bold(True)
        # TODO: (12/26/22) Finalize custom font
        self.title_text_surf = title_font.render(self.title, True, self.theme.get_colors().text)
        self.title_surf.blit(self.title_text_surf, self.title_text_surf.get_rect(
            center=(
                    (
                        (self.title_width // 2),
                        (self.title_height // 2)
                    ) 
                )
            )
        )
    
    def __init_button_details__(self):
        """ internal function that initializes the button details based on passed in button string names. Includes cancel button. """
        # Cancel button (X):
        self.cancel_button_surf = self.__get_cancel_button__()
        self.__blit_cancel_button__()
        self.__clicked__= utils.MSGBOX_CANCELED_TXT

        # Button dimensions:
        self.btn_dims = self.settings.get_btns().dimensions.wh() 
        self.btn_buffer = self.settings.get_btns().buffer 

        # Build buttons:
        self.btn_array = []
        btn_order = 0
        for b in self.buttons:
            self.btn_array.append(
                (
                    b,
                    self.__get_button__(b,btn_order)
                )
            )
            btn_order += 1
        
        # Blit buttons:
        self.__blit_buttons__()

    def __get_box_outline_surf__(self) -> pygame.Surface:
        """ internal function that returns MessageBox outline surface for element creation. """
        self.box_outline_pos = (
            ((self.w_width // 2)-(self.box_outline_width // 2)),
            ((self.w_height // 2)-(self.box_outline_height // 2))
        )
        ret = pygame.Surface((self.box_outline_width,self.box_outline_height))
        ret.fill(self.theme.get_colors().outline)
        return ret
    
    def __get_box_surf__(self) -> pygame.Surface:
        """ internal function that returns MessageBox surface for element creation. """
        self.box_pos = (
            ((self.box_outline_width // 2)-(self.box_width // 2)),
            ((self.box_outline_height // 2)-(self.box_height // 2))
        )
        ret = pygame.Surface((self.box_width,self.box_height))
        ret.fill(self.theme.get_colors().default)
        return ret
    
    def __blit_box_outline__(self):
        """ internal function that will blit changes made, so they appear on MessageBox. """
        self.box_outline_surf.blit(
            self.box_surf, 
            self.box_surf.get_rect(
                center=(
                    (self.box_outline_width//2),
                    (self.box_outline_height//2)
                )
            )
        )
    
    def __blit_title_outline_surf__(self):
        """ internal function that will blit changes made to title, so they appear on MessageBox. """
        self.title_outline_surf.blit(
            self.title_surf, 
            self.title_surf.get_rect()
        )
        self.box_surf.blit(self.title_outline_surf, self.title_outline_surf.get_rect())
        self.__blit_box_outline__()
    
    def __blit_msgtext_surf__(self):
        """ internal function that will blit MessageBox text to box_surf """
        if self.settings.get_variables().messagejustify == utils.MSGBOX_JUSTIFY_LEFT:
            # Left:
            left_pos = (
                self.box_pos[0],(self.box_height // 2)-self.settings.get_variables().messageheightbuffer
            )
            self.box_surf.blit(
                self.msgtext_surf, 
                self.msgtext_surf.get_rect(topleft=left_pos)
            )
        else:
            # Center:
            center_pos = (
                self.box_width // 2,
                (self.box_height // 2)-self.settings.get_variables().messageheightbuffer
            )
            self.box_surf.blit(
                self.msgtext_surf, 
                self.msgtext_surf.get_rect(center=center_pos)
            )
        
    def __blit_cancel_button__(self):
        """ internal function that will blit the cancel button to the current title surface. """
        but_center = (
            self.title_width-self.settings.get_cnlbtn().circlebuffer, 
            self.title_height-self.settings.get_cnlbtn().circlebuffer 
        )
        self.title_surf.blit(self.cancel_button_surf,self.cancel_button_surf.get_rect(center=but_center))
    
    def __blit_buttons__(self):
        """ internal function that will blit buttons based on buttons sent as part of instance init() """
        for btn in self.btn_array:
            btup = btn[1] # btup tuple (ie: (surface,(center dimensions)))
            bt_surf = btup[0] # button_surface (bt_surf.get_rect(center=bt_center))
            bt_center = btup[1] # button_center 
            self.box_surf.blit(bt_surf, bt_surf.get_rect(center=bt_center))
    
    def __get_cancel_button_pos__(self) -> tuple:
        """ returns cancel button (X) (x,y) cords for usage of collidepoint() dectection with mouse. """
        ret = ( 
                # X= related to position of MessageBox and width(s):
                self.box_outline_pos[0]+self.box_pos[0]+(
                        self.title_width-self.settings.get_cnlbtn().circlebuffer 
                    )+(
                        self.settings.get_cnlbtn().surfacedimensions.width-( 
                                self.settings.get_cnlbtn().circledimensions.width 
                            )
                        )-(
                            self.settings.get_cnlbtn().circledimensions.radius // 2 
                ),
                # Y= related to position of MessagBox and height(s): 
                self.box_outline_pos[1]+self.box_pos[1]+(
                    self.title_height-self.settings.get_cnlbtn().circlebuffer 
                    )+(
                         self.settings.get_cnlbtn().surfacedimensions.height -( 
                                self.settings.get_cnlbtn().circledimensions.height 
                            )
                        )-(
                            self.settings.get_cnlbtn().circledimensions.radius // 2 
                ) 
            )
        return ret

    def __get_cancel_button__(self,hover=False) -> pygame.Surface:
        """ returns MessageBox cancel button. When hover will highlight in UI. """
        # TODO: (12/26/22) Finalize custom font.
        font = pygame.font.Font(None,self.settings.get_variables().fontsize) 
        butsurf_dims = self.settings.get_cnlbtn().surfacedimensions.wh() 
        button_surf = pygame.Surface(butsurf_dims)
        button_surf.fill(self.theme.get_colors().title)
        
        button_clr = self.theme.get_colors().default
        text_clr = self.theme.get_colors().text
        if hover:
            # DRAW Circle Hover color:
            button_clr = self.theme.get_colors().button
            text_clr = self.theme.get_colors().buttonhovertext

        butcircle_dims = self.settings.get_cnlbtn().circledimensions.wh() 
        text_surface = font.render(self.settings.get_cnlbtn().circletext, True, text_clr)
        # DRAW Circle:
        cbr = self.settings.get_cnlbtn().circledimensions.radius
        pygame.draw.circle(button_surf,button_clr,butcircle_dims,cbr,cbr) 
        # BLIT to button_surface that will be returned:
        button_surf.blit(text_surface, text_surface.get_rect(center = butcircle_dims))
        return button_surf        
    
    def __get_button__(self,b,border=0,hover=False) -> tuple:
        """ returns a new messagebox button for use with messagebox. """
        # TODO: (12/26/22) Finalize custom font
        font = pygame.font.Font(None, self.settings.get_variables().fontsize)
        dims_center = (
            (self.btn_dims[0] // 2)+(self.settings.get_btns().outlinebuffer // 2),
            (self.btn_dims[1] // 2)+(self.settings.get_btns().outlinebuffer // 2)
        ) 
        button_surf = pygame.Surface(self.btn_dims)
        
        # Hover Outline setup:
        bod = (
            self.btn_dims[0]+self.settings.get_btns().outlinebuffer,
            self.btn_dims[1]+self.settings.get_btns().outlinebuffer
        )
        button_outline = pygame.Surface(bod)
        
        button_outline_clr = self.theme.get_colors().titleoutline 
        button_text_clr = self.theme.get_colors().text 

        if hover:
            button_outline_clr = self.theme.get_colors().buttonhover 
            button_text_clr = self.theme.get_colors().buttonhovertext 

        button_outline.fill(button_outline_clr)
        # TODO: (12/26/22) Finalize custom font
        text_surface = font.render(b, True, button_text_clr) 

        button_surf.fill(self.theme.get_colors().button)
        button_surf.blit(text_surface, text_surface.get_rect(center = (dims_center[0],(dims_center[1]))))
        button_outline.blit(button_surf, button_surf.get_rect(center = (dims_center[0],dims_center[1])))

        tar_width = (self.box_width // self.buttons.__len__())
        tar_width = (tar_width // 2) + (tar_width * border)
        
        button_center = (
            (tar_width), 
            ((self.box_height-self.btn_dims[1])+self.btn_buffer)
        )

        ret = (button_outline,button_center)
        return ret
    
    def __get_button_pos__(self,bc) -> tuple:
        """ internal function that will use the passed in bc (button cetner) current value and calculate (x,y) cords/POSition for given button. """
        return (
            self.box_outline_pos[0]+self.box_pos[0]+bc[0],
            self.box_outline_pos[1]+self.box_pos[1]+bc[1]
        )
    
    def __get_message_text__(self) -> pygame.Surface:
        """ returns a surface that is ready for blit() call upon message box surface to display messagebox message. """
        # TODO: (12/26/22) Finalize custom font.
        font = pygame.font.Font(None, self.settings.get_variables().fontsize)
        text_surface = font.render(self.message_text, True, self.theme.get_colors().text)
        return text_surface    
    
    def __message_text_max__(self,msg) -> str:
        """ returns safe text for message, based on max constant percentage of message box width. """
        return self.__base_text_max__(msg, self.settings.get_variables().messagemax)

    def __title_text_max__(self,msg) -> str:
        """ returns safe text for title, based on max constant percentage of message box width. """
        return self.__base_text_max__(msg,self.settings.get_variables().titlemax,self.settings.get_title().textupcase)

    def __base_text_max__(self,s,max,up=False) -> str:
        """ base internal function called for safe title and message text. """
        if s.__len__() > (self.box_width * max):
            m = int(self.box_width*max)
            r = (s.__len__()-m)+3 # TODO: Finalize base_text_max count buffer
            s = uth.str_rtrim(s,r)
            s = ("%s..." % s)
        if up:    
            s = s.upper()    
        return s

    def __event_list_check_keys__(self,event_list):
        """ internal function that will process passed in event_list for key pressed while MessageBox is active and take directed action. """
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__wait__ = False
                    self.__clicked__ = utils.MSGBOX_CANCELED_TXT
                    self.__canceled__ = True
                elif event.key == pygame.K_RETURN:
                    self.__wait__ = False
                    self.__clicked__ = self.buttons[self.settings.get_btns().returnbutton]

    def __event_list_check_button__(self,event_list,b=utils.MSGBOX_CANCELED_TXT):
        """ internal function that will process passed in event_list and update MessageBox properties. """
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.__wait__ = False # set wait() to False
                    if b != utils.MSGBOX_CANCELED_TXT:
                        self.__clicked__ = b # set clicked() to selected button text.
                    else:
                        self.__clicked__ = utils.MSGBOX_CANCELED_TXT # set clicked() to CANCELED_TXT
                        self.__canceled__ = True
  
    def __update_cancel_button__(self,event_list):
        """ internal function that uses passed in event_list and operates off of it to track user intreaction with MessageBox cancel button. """
        # CANCEL BUTTON (X):
        cancelbtn_pos = self.__get_cancel_button_pos__()
            
        # NOTE: (12/24/22) Check for mouse collide with rect of cancel button.
        # if so mark as hover and change UI to show hover button.:
        cbhover = self.cancel_button_surf.get_rect(center=cancelbtn_pos).collidepoint(pygame.mouse.get_pos())
        if cbhover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.cancel_button_surf = self.__get_cancel_button__(True)
            self.__event_list_check_button__(event_list)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.cancel_button_surf = self.__get_cancel_button__()
        self.__blit_cancel_button__()
        # NOTE: Blit title outline surface so changes to cancel button appear.:
        self.__blit_title_outline_surf__()
    
    def __update_buttons__(self,event_list):
        """ internal function that uses passed in event_list and operates off of it to track user interaction with MessageBox buttons for selection choice / .clicked() value. """
        count=0
        for btn in self.btn_array:
            bt = btn[0] # bt string (ie: 'Yes','No')
            btup = btn[1] # btup tuple (ie: (surface,(center dimensions)))
            bt_surf = btup[0] # button_surface (bt_surf.get_rect(center=bt_center))
            bt_center = btup[1] # button_center 
            
            # NOTE: (12/23/22) Check for mouse collide with rect of button from array.
            # if so mark as hover and change UI to show hover of button vs. not.
            btn_pos = self.__get_button_pos__(bt_center)
            hover = bt_surf.get_rect(center=btn_pos).collidepoint(pygame.mouse.get_pos())
            self.btn_array.pop(count) # Remove button from array
            if hover:
                nb = self.__get_button__(bt,count,True) # Get hover button
                self.__event_list_check_button__(event_list,bt)
            else:
                nb = self.__get_button__(bt,count) # Get standard button

            nb_surf = nb[0]
            nb_center = nb[1]
            self.box_surf.blit(nb_surf, nb_surf.get_rect(center=nb_center))
            self.__blit_box_outline__()
            self.btn_array.insert(count,(bt,nb))
            count += 1
    
    def update(self, event_list):
        """ called from the wait() method to process the buttons and to check collide against each MessageBox button. """
        # Cancel Button:
        self.__update_cancel_button__(event_list)

        # Selection Buttons:
        self.__update_buttons__(event_list)

        # Check for keys pressed by user (ie: return or esacpe keys):
        self.__event_list_check_keys__(event_list)

        # DRAW MessageBox and update display:
        self.rg.draw(self.window)
        pygame.display.flip()

    def wait(self,event_list) -> bool:
        """ returns True if waiting for user input, False if user has made a choice. """
        self.update(event_list)
        if not self.__wait__:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        return self.__wait__
    
    def clicked(self) -> str:
        """ returns the string value of the button text pressed. """
        return self.__clicked__
    
    def canceled(self) -> bool:
        """ returns True if MessageBox instance was canceled, False otherwise. """
        return self.__canceled__

class PopupMenuActions(object):
    """ pyguix.ui.elements.PopupMenuActions class. Meant to be subed and paired with context (*.json) file for menu item actions. Contains function / logic for PopupMenuItem actions that are to-be executed upon contextof mapped Sprite class."""

    def __init__(self):
        
        # TODO: Finalize a 'safe' method for checking full type as str vs. loaded json2pmans mapping dict().
        self.__context_name__ = reg_json2pmas[str("%s" % type(self))] #context
        self.__context__ = self.__init_context__()
        self.__target__ = ""
        self.__target_classes__ = self.__init_target_classes__()
        self.__funcmap__ = self.__init_funcmap__()

        if not self.__is_valid__():
            errmsg = ("Invalid JSON context (%s) supplied mapping with PopupMenuActions (%s) class. [pyguix]" % (self.get_context_name(),self.get_context().get_action_class()))
            raise LookupError(errmsg)    
     
        # TODO: Need to finalize context and contextof vars and how these are used through instance.
        if reg_pmas[self.get_context().get_action_class()] == None:
            reg_pmas[self.get_context().get_action_class()] = self
            for t in self.get_target_classes():
                if not reg_tc2pma.__contains__(t):
                    reg_tc2pma[t] = self.get_context().get_action_class()
                else:
                    raise LookupError(("Targetclass (%s) listed multiple times. Look at JSON Context files. Current file %s [pyguix]" % (t,self.get_context_name())))

        self.__act_pmi__ = None

    def __is_valid__(self) -> bool:
        """ base is_valid checks """
        ret = self.__check_valid_class__()
        ret = ret and self.__check_valid_functions__()
        return ret
    
    # TODO: Finalize object cache, intilization, etc.
    def __init_context__(self) -> utils.PopupMenuContext:
        ret = None
        if globalcontext(self.get_context_name()) == None:
            ngc = utils.PopupMenuContext(self.get_context_name())
            globalcontext(self.get_context_name(),ngc)
        ret = globalcontext(self.get_context_name())
        return ret
        #return utils.PopupMenuContext(self.get_context_name())
    
    def __init_target_classes__(self) -> tuple:
        return self.get_context().get_target_classes()
    
    def __init_funcmap__(self) -> dict:
        ret = dict()
        for mi in self.get_context().get_menuitems():
            if mi.type == utils.PopupMenuItemType.Action:
                ret[mi.identity] = mi.action
        return ret
    
    def set_enabled(self,act,b=True):
        """ Called from derived classes to allow for dynamically enable or disable PopupMenuItems. """
        mi = self.get_context().find_menuitem_by_action(act)
        if mi == None:
            raise LookupError(("Can't find PopupMenuContext (%s) menuitem action (%s) [pyguix.ui.elements.PopupMenuAction]" % (self.get_context_name(),act)))
        ngc = self.get_context()
        iof = ngc.get_menuitems().index(mi)
        nmi = mi
        nmi.enabled = b
        ngc.get_menuitems().pop(iof)
        ngc.get_menuitems().insert(iof,nmi)
        globalcontext(self.get_context_name(),ngc)

    def __check_valid_functions__(self) -> bool:
        ret = True
        for mi in self.get_funcmap():
            func = self.get_funcmap().get(mi)
            found = False
            for s in self.__dir__():
                if func == s:
                    found = True
            ret = ret and found
            if not found:
                raise LookupError(
                    ("Bad match between JSON context file (%s) mapping and action class (%s) [pyguix] \n Issue with function (%s) missing from action class. [pyguix]" % (
                        self.get_context_name(),
                        self.get_context().get_action_class(),
                        func)
                )
            )
        return ret
    
    def __check_valid_class__(self) -> bool:
        ret = False    
        if ("%s" % type(self)) == self.get_context().get_action_class():
            ret = True
        if not ret:
            raise LookupError("JSON context file (%s) with name %s & %s class don't match. Check the JSON file. [pyguix]" % (self.get_context_name(),self.get_context().get_action_class(),self.__class__.__name__))
        return ret

    def get_context_name(self) -> str:
        return self.__context_name__
    
    def get_context(self) -> utils.PopupMenuContext:
        return self.__context__

    def set_target(self,target):
        self.__target__ = target
    
    def get_target(self):
        return self.__target__
    
    def get_target_classes(self):
        return self.__target_classes__
    
    def get_funcmap(self):
        return self.__funcmap__
    
    def get_active_menuitem(self):
        return self.__act_pmi__

    def execute(self):
        # NOTE: Use of reflection to find active function related to clicked/active menuitem. 
        funcstr = self.get_funcmap().get(self.get_active_menuitem().get_identity())
        # Then call with getattr() to get callable function (func) for active instance of 'self'
        func = getattr(self,funcstr)
        # Finally call the desired target self.function() mapped via context.JSON file.
        func()

class PopupMenuItem(pygame.Surface):
    """ pyguix.ui.elements.PopupMenuItem class used in generation of PopupMenu. Generated by mapped JSON context files, listing details for 'menuitems'. Actions are mappings to PopupMenuActions.(function) name to-be executed, in contextof mapped Sprite class. """

    def __init__(self,window,dataclass,theme,settings,ishover=False,pos=(0,0),dims=(0,0)):

        super().__init__(size=dims)

        self.__ishover__ = ishover
        self.__dataclass__ = dataclass
        self.__enabled__ = self.__get_pmi__().enabled # Set True or False
        self.__theme__ = theme
        self.__settings__ = settings
        
        self.__init_dimensions(window,pos,dims)
        self.rect = pygame.Rect((pos,dims))
        self.image = self.__init_item__()
        self.mouse_pos = (0,0)
        self.contextof = None
        
    def __init_dimensions(self,window,pos,dims):
        self.window = window
        self.width = dims[0]
        self.height = dims[1]
        self.w_width,self.w_height = window.get_size()
        if self.__get_pmi__().type == utils.PopupMenuItemType.Separator and self.__get_pmi__().text == utils.POPUP_SEPCHAR:
            
            i=0
            ntext = uth.get_sepchar2text(self.__get_pmi__().text)
            
            while i <= (self.width):
                i+=1
                ntext = ntext + uth.get_sepchar2text(self.__get_pmi__().text)

            self.__get_pmi__().text = ntext

        self.pos = pos
        self.dims = dims
    
    def __get_pmi__(self) -> utils.PopupMenuItem:
        return self.__dataclass__
    
    def __get_theme__(self) -> utils.ElementTheme:
        return self.__theme__
    
    def __get_settings__(self) -> utils.PopupMenuSettings:
        return self.__settings__

    def __init_item__(self) -> pygame.Surface:
        f = pygame.font.Font(
            self.__get_settings__().get_menuitem_text().fonttype,
            self.__get_settings__().get_menuitem_text().size
        ) 
        mibclr = (0,0,0)
        if self.get_enabled():
            if self.__ishover__:
                mibclr = self.__get_theme__().get_colors().buttonhovertext
            else:
                mibclr = self.__get_theme__().get_colors().text 
        elif self.get_type() == utils.PopupMenuItemType.Separator:
            mibclr = self.__get_theme__().get_colors().outline
        else:
            mibclr = self.__get_theme__().get_colors().textdisabled
        text_surface = f.render(self.get_text(), True, mibclr)
        return text_surface
    
    def get_text(self) -> str:
        return self.__get_pmi__().text
    def get_type(self) -> utils.PopupMenuItemType:
        return self.__get_pmi__().type
    def get_identity(self) -> str:
        return self.__get_pmi__().identity
    def get_action(self) -> str:
        return self.__get_pmi__().action
    def get_enabled(self) -> bool:
        return self.__enabled__
    def get_clicked(self) -> bool:
        return self.__get_pmi__().clicked

class PopupMenu(pygame.sprite.Sprite):
    """ pyguix.ui.elements.PopupMenu Main class for generating contexual PopupMenu(s). Based on JSON context/theme files, as well as PopupMenuAction inherited classes. Related to mapping 'actions' (PopupMenuItem) and sprite classes (contextof)."""

    def __init__(self,window,rg=None,target_mouse_pos=(0,0),settings=utils.POPUP_DEFAULT_JSONSETTING,theme=utils.DEFAULT_THEME):

        super().__init__()

        self.tpma = None
        self.__theme__ = theme
        self.pum_pos = (0,0)
        self.isvalid = True

        if rg == None:
            self.isvalid = False
            return
        else:
            self.rg = rg

        # determine if ANY object class was clicked on.:
        # NOTE: Get class for popup mouse pos collide context of:
        if spritecache() != None:
            self.__contextof__ = spritecache()  
        else:
            self.__contextof__ = self.__get_contextof__()

        self.__contextof_pum__ = self.__init_context_of__(self.__contextof__)
        # Init PopupMenu context JSON file:
        self.__context__ = self.__init_popup_context__(self.__contextof_pum__)
        if self.__context__.get_action_class() == "" or self.__context__.get_action_class() == None:
            # DO NOT RENDER PopupMenu
            self.isvalid = False
            return

        self.__settings__ = self.__init_popup_settings__(settings)

        # Init PopupMenu dimensions:
        self.__init_dimensions__(window)
        
        self.rg.add(self)
        self.update(isinit=True)
        self.target_mouse_pos=target_mouse_pos
    
    # TODO Finalize init - * KEY TO MEMORY ISSUE BECAUSE OF DEFAULT.JSON *
    def __init_popup_context__(self,context) -> utils.PopupMenuContext:
        # NOTE: KEY issue for 'default.json' memory leak problem.
        if globalcontext(context) == None:
            ngc = utils.PopupMenuContext(context)
            globalcontext(context,ngc)
        ret = globalcontext(context)
        return ret

    def __init_popup_settings__(self,settings) -> utils.PopupMenuSettings:
        return utils.PopupMenuSettings(settings)
    
    def __init_context_of__(self,cat):
        tos = ("%s" % type(cat))
        ret = None

        if cat != None:
            # NOTE: Following tos must be a perfect match <class '(module).(class)'> 
            # (ie: <class '__main__.SomeSpriteClass'>)
            if reg_tc2pma.__contains__(tos): 
                    tos_pma = reg_pmas[reg_tc2pma[tos]] 
                    self.tpma = tos_pma
                    ret = tos_pma.get_context_name()

        if ret == None:
            ret = utils.POPUP_DEFAULT_JSONCONTEXT
        
        return ret
    
    def __get_contextof__(self): 
        # NOTE: Based on passed in group, grab Sprite (if any) that collide with pygame.mouse.get_pos()
        ret = None
        for s in self.rg:
            if s.rect.collidepoint(pygame.mouse.get_pos()):
                ret = s
                break
        return ret

    def __init_dimensions__(self,window):
        self.window = window
        self.dims =  self.__get_settings__().get_dimensions()
        self.width = self.dims.width
        self.box_outline_width = self.width + self.__get_settings__().get_outline_buffer() 
        self.height = self.dims.height
        self.box_outline_height = self.height + self.__get_settings__().get_outline_buffer()
        self.w_width,self.w_height = window.get_size()
        self.pmis=[]
        self.__clicked__ = None
    
    def __get_box_outline_surf__(self,pos=(0,0)) -> pygame.Surface:
        """  """
        if pos == (0,0):
            pos = ((self.w_width // 2),(self.w_height // 2))

        self.box_outline_pos = (
            (pos[0]+self.__get_settings__().get_outline_buffer()),
            (pos[1]+self.__get_settings__().get_outline_buffer()) 
        )

        # Check to make sure that pos will not allow popup to draw beyond window bounds:
        bop = self.box_outline_pos
        wd = (self.w_width,self.w_height)
        bod = (self.box_outline_width,self.box_outline_height)
        # TODO: (12/26/22) - Need to revisit this when target is passed in vs. just cords. 
        # mostly works except for bottom right hand corner of screen. 
        if bop[0]+bod[0] > wd[0]:
            bop = (
                bop[0]-(
                    (bop[0]+bod[0])-wd[0]
                ),
                bop[1]
            )
        
        if bop[1]+bod[1] > wd[1]:
            bop = (
                bop[0],
                bop[1] - (
                    (bop[1]+bod[1])-wd[1]
                )
            )
        
        self.box_outline_pos = bop
        # NOTE: End check for screen/display placemenet of popup
        ret = pygame.Surface((self.box_outline_width,self.box_outline_height))
        ret.fill(self.__get_theme__().get_colors().outline)  
        return ret

    def __get_button__(self,pos,dc,ishover=False) -> PopupMenuItem:

        pmi = PopupMenuItem(
            window=self.window,
            dataclass=dc,
            theme=self.__get_theme__(),
            settings=self.__get_settings__(),
            ishover=ishover,
            pos=pos,
            dims=(
                self.__get_settings__().get_menuitem_dimensions().wh()
            )
        )
        return pmi
    
    def __get_context__(self) -> utils.PopupMenuContext:
        return self.__context__

    def __get_settings__(self) -> utils.PopupMenuSettings:
        return self.__settings__
    
    def __get_theme__(self) -> utils.ElementTheme:
        if globaltheme() != None:
            self.__theme__ = globaltheme()
        return utils.ElementTheme(self.__theme__)

    def __get_displaybox__(self) -> pygame.Surface:
        ret = pygame.Surface((self.width,self.height))
        ret.fill(self.__get_theme__().get_colors().default)
        return ret

    def update(self,isinit=False):

        if not self.isvalid:
            return 

        # MessageBox outline surface:
        if isinit:
            self.pum_pos = pygame.mouse.get_pos()    
        pos = self.pum_pos
        
        self.box_outline_surf = self.__get_box_outline_surf__(pos=pos)
        self.displaybox = self.__get_displaybox__()
        
        # TODO: Move the following section for an __init__* to build out menu items, seprators, etc.
        miorder=0
        self.pmis.clear()
        for mi in self.__get_context__().get_menuitems():
    
            pos2=(
                self.box_outline_pos[0],
                (self.box_outline_pos[1]+(
                        self.__get_settings__().get_menuitem_dimensions().height*miorder
                    )
                )
            )

            ishover = False
            if mi.type == utils.PopupMenuItemType.Action:
                pos2=(
                    pos2[0]+self.__get_settings__().get_action_text_buffer(),
                    pos2[1]+self.__get_settings__().get_action_text_buffer()
                )
                # NOTE: Collide rect check for menu item button:
                pr = pygame.Rect(
                        pos2[0],
                        pos2[1],
                        self.__get_settings__().get_menuitem_dimensions().width,
                        self.__get_settings__().get_menuitem_dimensions().height
                    )
                prc = pr.collidepoint(pygame.mouse.get_pos())
                if prc:
                    ishover=True
                del pr

            p = self.__get_button__(pos2,mi,ishover)
            pis = pygame.Surface(size=(self.dims.width,(self.__get_settings__().get_menuitem_dimensions().height))) 
            pis.fill(self.__get_theme__().get_colors().default) 
            
            if p.__get_pmi__().type == utils.PopupMenuItemType.Action:
                tl = (
                        p.get_rect().x+self.__get_settings__().get_action_text_buffer(),
                        p.get_rect().y+self.__get_settings__().get_action_text_buffer()
                ) 
            else:
                tl = p.get_rect().topleft

            pis.blit(p.image,p.image.get_rect(topleft=(tl)))
            
            self.displaybox.blit(pis,pis.get_rect(topleft=(
                        pis.get_rect().x,
                        (pis.get_rect().y+((self.__get_settings__().get_menuitem_dimensions().height)*miorder))
                    )
                )
            )
            self.pmis.append(p)
            miorder+=1
        # END MOVE TO SELF CONTAINED INIT **************************************

        self.box_outline_surf.blit(self.displaybox,self.displaybox.get_rect(
                center=(
                    self.box_outline_width // 2,
                    self.box_outline_height // 2
                )
            )
        )

        # Add popup to sprite.RenderUpdates() group.:
        self.image = self.box_outline_surf
        self.rect = pygame.Rect((self.box_outline_pos+(self.box_outline_width,self.box_outline_height)))

        self.rg.draw(self.window)
        pygame.display.flip()

    def clicked(self,event_list=None) -> PopupMenuItem:

        if not self.isvalid:
            return None
        
        ret = self.__clicked__
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    for p in self.pmis:
                        # NOTE: Make sure the PopupMenuItem clicked by user is of type Action and is currently Enabled:
                        if p.get_type() == utils.PopupMenuItemType.Action and p.get_enabled():
                            if p.rect.collidepoint(pygame.mouse.get_pos()):
                                p.mouse_pos = self.target_mouse_pos
                                p.contextof = self.__contextof__
                                self.__clicked__ = p
                                ret = p
                                
                                # NOTE: Must remove self from passed in render group.
                                self.remove(self.rg)
                                # NOTE: This will use the target PopupMenuAction instance and call to 
                                # execute() the active PopupMenuItem related action:
                                if self.tpma != None:
                                    self.tpma.__act_pmi__ = p
                                    self.tpma.execute()
                                break # NOTE: Stop after finding PopupMenuItem button.
                                    

        return ret
    
    def clearall(instance):
        """ static method that checks instance passed in, and clear any membership of active sprite groups. """
        if isinstance(instance,PopupMenu):
            for g in instance.groups():
                instance.remove(g)

class SnapHUDPartInfo(object):
    """ Base SnapHUDPartInfo class meant to be inherited from. Mapped 1:1 with SnapHUD(context).json file. Contains part.function() to be executed and relay information to SnapHUDPart objects.. """
    
    def __init__(self) -> None:
        
        # NOTE: Self global context of SnapHUDPartInfo dervied class for usage through instance of game 
        # Allowing a single instance of each type to exist, via globalcontext().:
        if globalcontext(self.__get_typestr__(self)) != None:
            return globalcontext(self.__get_typestr__(self))
        
        self.__infodict__ = dict()
        globalcontext(self.__get_typestr__(self),self) 
    
    def partinfo(self,k,v=None):
        if v != None:
            self.__set_info__(k,v)
        return self.__get_info__(k)

    def __get_typestr__(self,o):
        return ("%s" % type(o))
    def __get_info__(self,k):
        return self.__value__(k)
    def __set_info__(self,k,v=None):
        self.__value__(k,v)

    def __value__(self,k,v=None):
        if not self.__infodict__.__contains__(k):
            self.__infodict__[k]=v
        if v != None:
            self.__infodict__[k]=v
        return self.__infodict__[k]

class SnapHUDPart(pygame.sprite.Sprite):
    """ Base level class in which all SnapHUDParts inherit from.  """

    def __init__(self):

        super().__init__()

        self.__settings__ = None
        self.__theme__ = None
        self.__context__ = None
        self.__dataclass__ = None
        self.__part__ = None

    def init(self,settings,theme,context,dataclass):
        """ base method call for setting values before reflection func() call of info for SnapHUDPart derived class. """
        self.settings(settings)
        self.theme(theme)
        self.context(context)
        self.__get_part_data__(dataclass)
        self.get_part(self.__init__part__())
    
    def __init__part__(self) -> pygame.Surface:
        """ function that should be overriden at derived class instance.  """
        return None

    def settings(self,s=None) -> utils.SnapHUDSettings:
        if s != None:
            self.__settings__ = s
        return self.__settings__
    def theme(self,t=None) -> utils.ElementTheme:
        if t != None:
            self.__theme__ = t
        return self.__theme__
    def context(self,c=None) -> utils.SnapHUDContext:
        if c != None:
            self.__context__ = c
        return self.__context__
    def __get_part_data__(self,dc=None) -> utils.SnapHUDPart:
        if dc != None:
            self.__dataclass__ = dc
        return self.__dataclass__
    def get_id(self):
        return self.__get_part_data__().id
    def get_title(self):
        return self.__get_part_data__().title
    def get_function(self):
        return self.__get_part_data__().function
    def get_type(self):
        return self.__get_part_data__().type
    def get_part(self,gp=None) -> pygame.Surface:
        if gp != None:
            self.__part__ = gp
        return self.__part__
    def get_value(self):
        # NOTE: uses reflection:
        func = getattr(globalcontext(self.context().get_infoclass()),self.get_function())
        return func()

class SnapHUDPartText(SnapHUDPart):
    """ Simple text SnapHUDpart class that extends from base of SnapHUDPart """

    def __init__part__(self) -> pygame.Surface:
        """ build out simple text SnapHUDPart. """
        wh = (
            self.settings().get_part_title_dimensions().width,
            self.settings().get_part_title_dimensions().height+self.settings().get_part_body_dimensions().height
        )
        ret = pygame.Surface(wh)
        
        ret.fill(self.theme().get_colors().default)
        
        title_surf = pygame.Surface(
            (self.settings().get_part_title_dimensions().width,
            self.settings().get_part_title_dimensions().height)
        )
        
        title_surf.fill(self.theme().get_colors().title)
        
        ret.blit(title_surf,title_surf.get_rect())
        
        fonttitle = pygame.font.Font(None,self.settings().get_part_title_font().size)
        fonttitle.set_bold(self.settings().get_part_title_font().setbold)
        snap_title = fonttitle.render(self.get_title(),True,self.theme().get_colors().textsubtitle)
        ret.blit(snap_title,snap_title.get_rect(
                center=(
                    ret.get_width() // 2,
                    (ret.get_height()-(ret.get_height()-self.settings().get_part_title_dimensions().height)) // 2
                )
            )
        )

        font = pygame.font.Font(None,self.settings().get_part_body_font().size)
        font.set_bold(self.settings().get_part_body_font().setbold)
        snap_text = font.render(self.get_value(),True,self.theme().get_colors().text)
        ret.blit(snap_text,snap_text.get_rect(
            center=(
                ret.get_width() // 2,
                (ret.get_height()-self.settings().get_part_body_dimensions().height // 2)
            )
        ))

        return ret

    def __init__(self):

        super().__init__()

class SnapHUD(pygame.sprite.Sprite):
    """ snap right/left heads up display ui element. """

    def __init__(self,window,settings=utils.SNAP_DEFAULT_JSONSETTING,theme=utils.DEFAULT_THEME,context=utils.SNAP_DEFAULT_JSONCONTEXT,rg=pygame.sprite.RenderUpdates(),*groups, set_num_of_groups=0):
        
        super().__init__(*groups)

        self.__settings__ = self.__init_snap_settings__(settings)
        self.__context__ = self.__init_snap_context__(context)
        self.__context__.__paa__ = self.__context__.__paa__[:set_num_of_groups]
        self.__theme__ = self.__init_theme__(theme)
        self.__win__ = window
        self.__win_w__,self.__win_h__ = window.get_size()
        self.__width__ = self.settings().get_dimensions().width
        self.__height__ = self.settings().get_dimensions().height
        self.__rg__ = rg
        self.__olpos__ = (0,0) # Outline position (x,y)
        self.__direct__ = self.settings().get_start_direction()
        self.__hudparts__ = dict()
        self.__hudpartsprites__ = dict()

        self.update() # NOTE: Initial call to update() to draw ui element
        self.__rg__.add(self)

    def __init_outline__(self,*pos) -> pygame.Surface:
        ret = pygame.Surface((0,0))
        if self.__olpos__ == (0,0):
            self.__olpos__ = (
                self.__win_w__-self.settings().get_buffer_dimensions().width,
                self.__win_h__-(self.__win_h__-self.settings().get_buffer_dimensions().height)
            )

        if self.__direct__ == utils.SnapType.Closed:
            self.__height__ = self.settings().get_dimensions().height
            self.__set_olpos__(((self.__win_w__-self.settings().get_buffer_dimensions().width),self.__olpos__[1]))
        else:
            self.__height__ = self.settings().get_dimensions().height
            self.__set_olpos__(((self.__win_w__-self.__width__),self.__olpos__[1]))
            

        ret = pygame.Surface((self.__width__,self.__height__))
        ret.fill(self.theme().get_colors().outline)
        return ret
    
    def __init_snap_button__(self,*pos) -> pygame.Surface:

        self.__snapbutton_pos__ = (
            self.__olpos__[0],
            self.__olpos__[1]
        )

        wh = (
            self.settings().get_button_dimensions().width-self.settings().get_button_buffer(),
            self.settings().get_button_dimensions().height-self.settings().get_button_buffer()
        )
        ret = pygame.Surface(wh)
        ret.fill(self.theme().get_colors().default)
        return ret

    def __init_snap_title__(self) -> pygame.Surface:

        wh = (
            self.settings().get_title_dimensions().width,
            self.settings().get_title_dimensions().height
        )
        ret = pygame.Surface(wh)
        ret.fill(self.theme().get_colors().default)
        
        font = pygame.font.Font(None,self.settings().get_title_font().size)
        font.set_bold(self.settings().get_title_font().setbold)
        title_txt = font.render(self.context().get_title(),True,self.theme().get_colors().texttitle)
        ret.blit(title_txt,title_txt.get_rect(
            center=(
                ret.get_width() // 2,
                ret.get_height() // 2
            )
        ))

        return ret

    def __init_arrow__(self,hover) -> pygame.Rect:
        """ SnapHUD main button arrow for 'Closed/Open' state of SnapType """
        
        if self.__direct__ == utils.SnapType.Closed:
            cords = self.settings().get_button_closed().cords.tricords
            line_cords = self.settings().get_button_closed().cords.linecords
        else:
            cords = self.settings().get_button_open().cords.tricords
            line_cords = self.settings().get_button_open().cords.linecords

        if hover:
            clr = self.theme().get_colors().buttonhovertext
        else:
            clr = self.theme().get_colors().texttitle

        pygame.draw.polygon(
            self.__snapbutton__,
            clr,
            cords,
            self.settings().get_button_line_width()
        )

        pygame.draw.polygon(
            self.__snapbutton__,
            clr,
            line_cords,
            self.settings().get_button_line_width()
        )
    
    def __init_snap_settings__(self,settings) -> utils.SnapHUDSettings:
        return utils.SnapHUDSettings(settings)
    def settings(self) -> utils.SnapHUDSettings:
        return self.__settings__
    def __init_snap_context__(self,context) -> utils.SnapHUDContext:
        return utils.SnapHUDContext(context)
    def context(self) -> utils.SnapHUDContext:
        return self.__context__

    def __init_theme__(self,theme) -> utils.ElementTheme:
        if globaltheme() != None:
            theme = globaltheme()
        return utils.ElementTheme(theme)
    
    def theme(self) -> utils.ElementTheme:
        return self.__theme__

    def __set_direct__(self):
        if self.__direct__ == utils.SnapType.Closed:
            self.__direct__ = utils.SnapType.Open
        else:
            self.__direct__ = utils.SnapType.Closed

    def __set_olpos__(self,pos):
        self.__olpos__ = pos

    def __get_parts__(self) -> list:
        """ get parts and render as part of SnapHUD.: """
        spa = list()
        
        for p in self.context().get_parts():
            part = self.context().get_part(p)
            if self.__hudparts__.__contains__(part.id):
                obj = self.__hudparts__[part.id]
                obj.init(self.settings(),self.theme(),self.context(),p)
            else:
                obj = eval("%s()" % part.type)
                obj.init(self.settings(),self.theme(),self.context(),p)
                self.__hudparts__[part.id] = obj
            spa.append(obj)
        return spa
            
            
    def update(self):
        """ function that draws SnapHUD element, including called for check of hover collide. """
        self.__olsurf__ = self.__init_outline__() # Outline pygame.Surface
        
        self.image = self.__olsurf__
        self.__snapbutton__ = self.__init_snap_button__()
        self.rect = pygame.Rect((self.__olpos__+(self.__width__,self.__height__)))
        hover = self.rect.collidepoint(pygame.mouse.get_pos())
        self.__init_arrow__(hover)
        
        self.image.blit(self.__snapbutton__,self.__snapbutton__.get_rect(
            topleft=(
                self.__snapbutton__.get_width()-(self.__snapbutton__.get_width()-(self.settings().get_button_buffer()//2)),
                self.__snapbutton__.get_height()-(self.__snapbutton__.get_height()-(self.settings().get_button_buffer()//2))
            )
        ))

        self.__snaptitle__ = self.__init_snap_title__()
        self.image.blit(self.__snaptitle__,self.__snaptitle__.get_rect(
            topleft=(
                (self.__snaptitle__.get_width()-(self.__snaptitle__.get_width()-1)+self.settings().get_button_dimensions().width),
                self.__snaptitle__.get_height()-(self.__snaptitle__.get_height()) 
            )
        ))

        # NOTE|TODO: Finalize and move to own bound function. For now reside in main update() for now.
        parts = self.__get_parts__()
        buff = 0
        npos = (
                    self.__olpos__[0]+self.settings().get_buffer_dimensions().width,
                    self.__olpos__[1]+self.settings().get_dimensions().height+self.settings().get_buff_buffer()+buff
                )
        ix=2
        i=1
        for sp in parts:

            if self.__hudpartsprites__.__contains__(sp):
                s = self.__hudpartsprites__[sp]
            else:
                s = pygame.sprite.Sprite(self.__rg__)
            
            s.image = sp.get_part()
            s.rect = pygame.Rect(npos+(self.__width__,self.__height__))

            self.__hudpartsprites__[sp] = s

            buff += self.settings().get_dimensions().height
            npos = (
                    self.__olpos__[0]+self.settings().get_buffer_dimensions().width,
                    (self.__olpos__[1]+self.settings().get_dimensions().height+(self.settings().get_buff_buffer()*ix)+buff+(self.settings().get_part_title_dimensions().height*i))
                )
            ix += 1
            i+=1

        self.__rg__.draw(self.__win__)
        pygame.display.flip()

    def clicked(self) -> bool:
        """ clicked function used to check to see if user has 'clicked' to expand SnapHUD. Returns True if so, False if not. """        
        ret = False
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            ret = True
            if self.__direct__ == utils.SnapType.Closed:
                self.__set_olpos__(((self.__win_w__-self.__width__),self.__olpos__[1]))
            else:
                self.__set_olpos__(((self.__win_w__-self.settings().get_buffer_dimensions().width),self.__olpos__[1]))
            self.__set_direct__()
            self.update()
        return ret

# NOTE:
# ALL CLASSES BELOW HERE ARE IN BETA DEVELOPMENT

class __Hamburger__(pygame.sprite.Sprite):

    def __init__(self,window,settings=utils.HAM_DEFAULT_JSONSETTING,theme=utils.DEFAULT_THEME,rg=pygame.sprite.Group()):
        
        super().__init__(rg)

        self.__win__ = window
        self.__settings__ = settings
        self.__theme__ = theme

    def window(self):
        return self.__win__
    def settings(self) -> utils.HamburgerSettings:
        return self.__settings__
    def theme(self) -> utils.ElementTheme:
        return self.__theme__

