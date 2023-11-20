def NodeEditor(G):
    """Makes a Node Editor screen! Still in progress. Come back later!

    Parameters
    ----------
    G : graphics.Graphic
        The Graphic screen
    
    USE:
```py
from graphics import Graphic
G = Graphic()
NodeEditor(G)
```
    """
    @G.Graphic
    def editor(event, path, element=None, aborted=False):
        if event == GO.EFIRST:
            if path.endswith('.elm'):
                path = path[:-4]
            if not os.path.exists('data/elements/'+path+'.elm'):
                open('data/elements/'+path+'.elm', 'w+').write('{"idea": "BLANK", "name": "New File"}')
            G.Container.contents = json.load(open('data/elements/'+path+'.elm'))
            G.Container.name = G.Container.contents['name']
        if event == GO.ELOADUI:
            G.Clear()
            G.add_text('EDITING ELEMENT "%s"'%G.Container.name, GO.CGREEN, GO.PCTOP, GO.FTITLE)
            G.add_button('Settings', GO.CGREEN, GO.PRTOP)
        elif event == GO.EELEMENTCLICK: # This is going to be the only button that was created
            @G.Graphic
            def settings(event, element=None, aborted=False):
                if event == GO.ELOADUI:
                    CBOT = GO.PNEW([1, 0], GO.PSTACKS[GO.PCBOTTOM][1], 0)
                    G.Clear()
                    G.add_empty_space(CBOT, -20, 0)
                    G.Container.go = G.add_button('Apply!', GO.CGREEN, CBOT)
                    G.Container.exit = G.add_button('Cancel', GO.CGREY, CBOT)
                elif event == GO.ETICK: return True
                elif event == GO.EELEMENTCLICK:
                    if element == G.Container.go:
                        print('GO!')
                        G.Abort()
                    elif element == G.Container.exit:
                        print('Cancel. :(')
                        G.Abort()
                elif event == GO.ELAST:
                    pass # Whatever you return here will be returned by the function
            settings()
        elif event == GO.ETICK:
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and event.mod & pygame.KMOD_SHIFT:
                    json.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'w+')) # Save
    return editor(path)
