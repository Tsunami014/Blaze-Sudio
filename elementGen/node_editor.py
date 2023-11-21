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
            G.Container.saved = False
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
                    RTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PRTOP][1], 1)
                    LTOP = GO.PNEW([0, 1], GO.PSTACKS[GO.PLTOP][1], 2)
                    G.Clear()
                    G.add_text('SETTINGS FOR NODE "%s":'%G.Container.name, GO.CGREEN, LTOP, GO.FFONT)
                    G.Container.inpname = G.add_input(LTOP, width=G.size[0]/3, resize=GO.RNONE, placeholder=G.Container.name)
                    G.add_text('SETTINGS FOR NODE EDITOR:', GO.CBLUE, RTOP, GO.FFONT)
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
                    res = G.uids[G.Container.inpname].text
                    if res != '':
                        G.Container.name = res
                        G.Container.contents['name'] = res
                    pass # Whatever you return here will be returned by the function
            settings()
        elif event == GO.ETICK:
            return True
        elif event == GO.EEVENT: # When something like a button is pressed. Is passed 'element' too, but this time it is an event
            if element.type == pygame.KEYDOWN:
                if element.key == pygame.K_s and element.mod & pygame.KMOD_CTRL:
                    if path.endswith('.elm'):
                        path = path[:-4]
                    G.Container.saved = True
                    json.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'w+')) # Save
        elif event == GO.ELAST:
            if G.Container.saved:
                if path.endswith('.elm'):
                    path = path[:-4]
                if G.Container.name != path.split('/')[1]:
                    os.remove('data/elements/'+path+'.elm')
                    path = path.split('/')[0] + '/' + G.Container.name
                    open('data/elements/'+path+'.elm', 'w+')
                    json.dump(G.Container.contents, open('data/elements/'+path+'.elm', 'w+'))
    return editor(path)
