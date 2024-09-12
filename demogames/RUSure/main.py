from BlazeSudio.Game import Game
import BlazeSudio.Game.statics as Ss
from BlazeSudio.graphics import options as GO
G = Game()

@G.DefaultSceneLoader
class MainGameScene(Ss.BaseScene):
    useRenderer = False
    def __init__(self, Game, **settings):
        self.rendered = False
        self.title = settings.get('title', ' ')
        self.txt = settings.get('txt', ' ')
        self.buttons = settings.get('buttons', {})
    
    def render(self):
        if not self.rendered:
            G.G.stacks.clear()
            G.G.WIN.fill((175, 175, 175))
            G.G.add_empty_space(GO.PCTOP, 0, 30)
            G.G.add_text(self.title, GO.CACTIVE, GO.PCTOP, GO.FTITLE)
            G.G.add_text(self.txt, GO.CINACTIVE, GO.PCTOP)
            centre = GO.PNEW([1, 0], GO.PCCENTER.func, 1, 1)
            G.G.add_empty_space(centre, -50, 0)
            for n, inf in self.buttons.items():
                if isinstance(inf[1], str):
                    G.G.add_button(n, inf[0], centre, callback=lambda x, inf=inf: G.load_scene(txt=inf[1], buttons=inf[2]))
                else:
                    G.G.add_button(n, inf[0], centre, callback=inf[1])
            self.rendered = True
    
    def tick(self, keys):
        pass

def load_title(*args):
    orng = GO.CNEW('orange')
    G.load_scene(title='Do you want to play the game?', buttons={
        "Yes": [GO.CGREEN, 'But are you *really* sure?', {
            "Yes": [GO.CGREEN, 'OK then.', {
                "Back to title!": [orng, load_title]
            }],
            "No": [GO.CRED, 'AHA! I thought so much. You DISCUST ME.', {
                "OK.": [orng, load_title]
            }]
        }],
        "No": [GO.CRED, 'Ha. YOU LOOSE THEN.', {
            "OK.": [orng, load_title]
        }]
    })

load_title()

G.play(debug=True)