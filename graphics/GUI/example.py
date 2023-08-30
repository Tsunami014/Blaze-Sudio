import pygame
from pygame import locals
try:
    from __init__ import InputBox, RESIZE_H, TextBoxFrame
    from __init__ import gui as ui
    from textboxify.borders import LIGHT, BARBER_POLE
except ImportError:
    from graphics.GUI import InputBox, RESIZE_H, TextBoxFrame
    from graphics.GUI.pyguix import gui as ui
    from graphics.GUI.textboxify.borders import LIGHT, BARBER_POLE

class SnapHUDPartInfoExample(ui.SnapHUDPartInfo):

    # NOTE: Example bound function called by reflection OR by in game logic to update 'listening' SnapHUDPart:
    # This example simply allows for setting of value or getting current value when calling .part_one()
    # You can easily add other logic in part_one() that then updates the value when called. 
    # Yet still important is to return the part value.
    def part_one(self,v=None):
        return self.partinfo("part_one",v)

    def __init__(self) -> None:
        super().__init__()

def textboxify_test(screen):
    # Customize and initialize a new dialog box.
    dialog_box = TextBoxFrame(
        text="Hello! This is a simple example of how TextBoxify can be implemented in Pygame games.",
        text_width=320,
        lines=2,
        pos=(80, 180),
        padding=(150, 100),
        font_color=(92, 53, 102),
        font_size=26,
        bg_color=(173, 127, 168),
        border=LIGHT,
    )

    # Optionally: add an animated or static image to indicate that the box is
    # waiting for user input before it continue to do anything else.
    # This uses the default indicator, but custom sprites can be used too.
    dialog_box.set_indicator()

    # Optionally: add a animated portrait or a static image to represent who is
    # talking. The portrait is adjusted to be the same height as the total line
    # height in the box.
    # This uses the default portrait, but custom sprites can be used too.
    dialog_box.set_portrait()

    # Create sprite group for the dialog boxes.
    dialog_group = pygame.sprite.LayeredDirty()
    #dialog_group.clear(screen, background)
    dialog_group.add(dialog_box)

    run = True
    next_quit = False
    while run:
        pygame.time.Clock().tick(60)
        screen.fill((92, 53, 102))
        all.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    shud.clicked()
            if event.type == locals.QUIT:
                run = False
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_ESCAPE:
                    run = False

                # Event that let the user tell the box to print next lines of
                # text or close when finished printing the whole message.
                if event.key == locals.K_RETURN:
                    if not dialog_box.alive():
                        dialog_group.add(dialog_box)
                    else:
                        # Cleans the text box to be able to go on printing text
                        # that didn't fit, as long as there are text to print out.
                        if dialog_box.words:
                            dialog_box.reset()

                        # Whole message has been printed and the box can now reset
                        # to default values, set a new text to print out and close
                        # down itself.
                        else:
                            dialog_box.reset(hard=True)
                            dialog_box.set_text("Happy coding!")
                            dialog_box.__border = BARBER_POLE
                            dialog_box.kill()
                            if next_quit:
                                del dialog_box
                                return
                            else:
                                next_quit = True

        # Update the changes so the user sees the text.
        dialog_group.update()
        shud.update() # NOTE: update() called to check for 'hover'
        rects = dialog_group.draw(screen)
        pygame.display.update(rects)
        pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((640, 360))

all = pygame.sprite.RenderUpdates()

shudpie = SnapHUDPartInfoExample()
# NOTE: SnapHUD instance created AFTER the Info class instance.  
shud = ui.SnapHUD(window=screen, rg=all, set_num_of_groups=1)

run = True
shudpie.part_one("None")
while run:
    screen.fill((92, 53, 102))
    all.draw(screen)
    shud.update()
    pygame.display.update()
    mb = ui.MessageBox(
    window=screen,
    event_list=pygame.event.get(),
    buttons=['textboxify', 'input box'],
    )

    # NOTE: Act upoon if the MessageBox was canceled, if not can act upon the .clicked() value.:
    if not mb.canceled():
        if mb.clicked() == 'textboxify':
            textboxify_test(screen)
        else:
            input_box = InputBox(100, 100, 140, 32, 'Type here!', resize=RESIZE_H)
            def _(screen):
                all.draw(screen)
                shud.update()
            def __(event):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        shud.clicked()
            out = input_box.interrupt(screen, run_too=_, event_callback=__)
            shudpie.part_one(out)
    else:
        print("You canceled the MessageBox instance.")
        run = False
