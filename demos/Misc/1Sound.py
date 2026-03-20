"""Sound"""
def main():
    from BlazeSudio.graphics import Screen, GUI
    import BlazeSudio.graphics.options as GO
    from BlazeSudio.Game.sound import Beep
    from pygame.locals import KEYDOWN, K_RETURN
    class Main(Screen):
        def _LoadUI(self):
            self.layers[0].add_many(['Main', 'go'])
            fs = {
                'Sin': Beep.sin,
                'Square': Beep.square,
                'Triangle': Beep.triangle,
                'Noise': Beep.noise
            }
            self['Main'].extend([
                GUI.Text(GO.PCTOP, '# Sounds demo'),
                GUI.Text(GO.PLCENTER, '## OPTIONS'),
                GUI.Text(GO.PLCENTER, 'Type of wave'),
                (typ := GUI.DropdownButton(GO.PLCENTER, list(fs.keys()))),
                GUI.Text(GO.PLCENTER, 'Frequency left'),
                (Lfreq := GUI.NumInputBox(GO.PLCENTER, 100, GO.RNONE, minim=1, empty=500, placeholdOnNum=None)),
                GUI.Text(GO.PLCENTER, 'Frequency right'),
                (Rfreq := GUI.NumInputBox(GO.PLCENTER, 100, GO.RNONE, minim=0, empty=0, placeholdOnNum=0, placeholder='Left')),
            ])
            self['go'].append(GUI.Button(GO.PCCENTER, GO.CORANGE, 'Beep', func=lambda: fs[typ.get()](Lfreq.get(), Rfreq.get() or None)))
        
        def _Event(self, event):
            if event.type == KEYDOWN and event.key == K_RETURN:
                self['go'][0].func()
    
    Main()()
