"""Image wrapping [image]"""
def main():
    from BlazeSudio.graphics import Screen, Progressbar, options as GO, GUI
    from BlazeSudio.utils.wrap import wrapSurface, Segment
    import pygame
    
    class Main(Screen):
        def __init__(self):
            super().__init__(GO.CGREY)
        
        def makeSur(self):
            topF = self.topF
            news = pygame.Surface((1, 2))
            news.set_at((0, 0), topF['Main'][1].get())
            news.set_at((0, 1), topF['Main'][3].get())
            news2 = pygame.transform.smoothscale(news, (topF['Main'][5].get(), topF['Main'][7].get()))
            self.inputSur = news2
            topF['Main'][-1].set(news2)
            self.segs = []
            self.cursegidx = None
        
        def _LoadUI(self):
            self.layers[0].add('Main')
            self.layers[1].add('Top')
            self.segs = []
            self.cursegidx = None
            topF = GUI.BaseFrame(GO.PCTOP, (self.size[0], self.size[1]//2), 2)
            topF.layers[0].add('Main')
            self.topF = topF
            botF = GUI.BaseFrame(GO.PCTOP, (self.size[0], self.size[1]//2), 2)
            botF.layers[0].add('Main')
            self.botF = botF

            self['Main'].extend([topF, botF])

            self.GObtn = GUI.Button(GO.PCCENTER, GO.CORANGE, 'Wrap!')
            self['Top'].append(self.GObtn)

            LTOP = GO.PNEW((0, 0), (0, 1))
            topF['Main'].extend([
                GUI.Text(LTOP, 'Colour 1'),
                GUI.ColourPickerBTN(LTOP),
                GUI.Text(LTOP, 'Colour 2'),
                GUI.ColourPickerBTN(LTOP, default=(10,255,50)),
                GUI.Text(LTOP, 'Width'),
                GUI.NumInputBox(LTOP, 100, GO.RHEIGHT, start=500, minim=1, maxim=1500, placeholdOnNum=None),
                GUI.Text(LTOP, 'Height'),
                GUI.NumInputBox(LTOP, 100, GO.RHEIGHT, start=100, minim=1, maxim=500, placeholdOnNum=None),
            ])

            RTOP = GO.PNEW((1, 0), (0, 1))
            self.offset = len(topF['Main'])
            topF['Main'].extend([
                GUI.Text(RTOP, 'Top'),
                GUI.NumInputBox(RTOP, 100, GO.RHEIGHT, empty=0.5, start=None, minim=0, maxim=2, placeholdOnNum=None, decimals=8),
                GUI.Text(RTOP, 'Bottom'),
                GUI.NumInputBox(RTOP, 100, GO.RHEIGHT, empty=-0.5, start=None, minim=-1, maxim=0, placeholdOnNum=None, decimals=8),
                GUI.Text(RTOP, 'Limit'),
                GUI.Switch(RTOP, default=True),
            ])

            topF['Main'].append(GUI.Text(GO.PCTOP, '# INPUT IMAGE'))

            def customImg(img):
                topF['Main'][-1].set(pygame.image.load(img))
                self.segs = []
                self.cursegidx = None

            rainbow = GO.CRAINBOW()
            topF['Main'].extend([
                GUI.Button(GO.PLBOTTOM, next(rainbow), 'Iris',   func=lambda: customImg('wrap1.png')),
                GUI.Button(GO.PLBOTTOM, next(rainbow), 'Text',   func=lambda: customImg('wrap2.png')),
                GUI.Button(GO.PLBOTTOM, next(rainbow), 'Planet', func=lambda: customImg('wrap3.png')),
            ])

            topF['Main'].append(GUI.Static(GO.PCCENTER, pygame.Surface((0, 0))))

            def resetBotSur():
                botF['Main'][-1].set(pygame.Surface((0, 0)))
                self.segs = []
                self.cursegidx = None

            botF['Main'].extend([
                GUI.Empty(GO.PCTOP, (0, 30)),
                GUI.Text(GO.PCTOP, '# OUTPUT IMAGE'),

                GUI.Button(GO.PRTOP, GO.CORANGE, 'Reset', func=resetBotSur)
            ])

            CCENTER = GO.PNEW((0.5, 0.5), (1, 0), (True, True))
            botF['Main'].append(GUI.ImageViewer(CCENTER, pygame.Surface((0, 0)), (800, 400)))

            self.makeSur()
        
        def _Event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.cursegidx = None
                    self.segs = []
                elif event.key == pygame.K_RETURN:
                    self.wrap()
        
        def _Tick(self):
            if self.topF['Main'][1].active or self.topF['Main'][3].active or \
               self.topF['Main'][5].active or self.topF['Main'][7].active:
                self.makeSur()
            
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                w = self.topF['Main'][-1].get().get_width()
                pos = pygame.mouse.get_pos()[0]-(self.size[0]-w)/2
                pos = max(min(pos, w), 0)
                if self.cursegidx is None:
                    self.cursegidx = len(self.segs)
                    self.segs.append([pos, pos])
                else:
                    curSeg = self.segs[self.cursegidx]
                    if pos < curSeg[0]:
                        curSeg[0] = pos
                    if pos > curSeg[1]:
                        curSeg[1] = pos
            else:
                self.cursegidx = None
        
        def _DrawAft(self):
            w = self.topF['Main'][-1].get().get_width()
            off = (self.size[0]-w)/2
            for seg in self.segs:
                pygame.draw.line(self.WIN, (125, 125, 125), (seg[0]+off, 90), (seg[1]+off, 90), 5)
        
        def _ElementClick(self, obj):
            if obj == self.GObtn:
                self.wrap()
        
        def wrap(self):
            @Progressbar.decor(4)
            def load(slf):
                import time
                time.sleep(0.5)
                pygame.event.pump()
                yield 'Setting up'
                off = self.offset
                topF = self.topF['Main']

                conns = []
                for seg in self.segs:
                    conns.append(Segment(seg[0], seg[1]))

                slf['surf'] = yield from wrapSurface(
                    topF[-1].get(), 
                    topF[off+1].get(), 
                    topF[off+3].get(), 
                    topF[off+5].get(), 
                    pg2=False, 
                    constraints=conns, 
                    isIter=True
                )

                yield 'Finishing up'
            fin, outs = load()
            if fin:
                self.botF['Main'][-1].set(outs['surf'])
    
    Main()()
