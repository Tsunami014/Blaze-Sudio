from BlazeSudio.Game import Game
import BlazeSudio.Game.statics as Ss
from BlazeSudio.graphics import options as GO
G = Game()

@G.DefaultSceneLoader
class MainGameScene(Ss.SkeletonScene):
    useRenderer = False
    def __init__(self, Game, **settings):
        super().__init__(Game, **settings)
        self.rendered = False
        self.title = settings.get('title', ' ')
        self.txt = settings.get('txt', ' ')
        self.buttons = settings.get('buttons', {})
    
    def render(self):
        if not self.rendered:
            graphic = self.Game.G
            graphic.stacks.clear()
            graphic.WIN.fill((175, 175, 175))
            graphic.add_empty_space(GO.PCTOP, 0, 30)
            graphic.add_text(self.title, GO.CACTIVE, GO.PCTOP, GO.FTITLE)
            graphic.add_text(self.txt, GO.CINACTIVE, GO.PCTOP)
            centre = GO.PNEW([1, 0], GO.PCCENTER.func, 1, 1)
            graphic.add_empty_space(centre, -50, 0)
            for n, inf in self.buttons.items():
                if isinstance(inf[1], str):
                    graphic.add_button(n, inf[0], centre, callback=lambda x, inf=inf: self.Game.load_scene(txt=inf[1], buttons=inf[2]))
                else:
                    graphic.add_button(n, inf[0], centre, callback=inf[1])
            self.rendered = True

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