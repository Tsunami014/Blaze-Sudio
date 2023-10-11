import AIs, asyncio

class Copilot:
    def __init__(self):
        print('setup...')
        self.ai = AIs.AI()
        print('evaluating...')
        asyncio.run(self.ai.find_current())
        print('Done :)')
    
    def __call__(self, txt):
        print('running...')
        asyncio.run(self.ai(txt))
        seen = ''
        while self.ai.still_generating():
            if self.ai.resp != seen:
                print(self.ai.resp[len(seen):], end='')
                seen = self.ai.resp
        print()

c = Copilot()
c('Hello! how are you?')
pass