import languagemodels as lm
try:
    from utils.bot.install_tinyllm import installed
except:
    try:
        from bot.install_tinyllm import installed
    except:
        from install_tinyllm import installed

def classify(doc: str, *labels: list[str]):

    results = lm.rank_instruct(
        f"Classify as {'or'.join(labels)}: {doc}\n\nClassification:", labels
    )

    return results[0]

class TinyLLM:
    def __init__(self):
        self.rams = installed()
        self.resp = ''
    
    async def __call__(self, cnvrs, ram=None):
        if ram == None: ram = 4 # for this we need 4 because anything lower SUCKS LIKE HELL
        # I TRIED WITH LOWER THAN 4. WAS TRASH. DON'T USE. TRUST ME.
        lm.set_max_ram(ram)
        return lm.chat(cnvrs)
    
    async def interrupt(self, txt, ram=None):
        if ram == None: ram = self.rams[0]
        lm.set_max_ram(ram)
        if lm.classify(txt,"simple reply","complex reply") == 'complex reply': return 'l'
        return 's'

if __name__ == '__main__':
    import asyncio
    tllm = TinyLLM()
    prompt = f"System: Reply as a helpful assistant. Currently {lm.get_date()}."
    while True:
        inp = input('> ')
        if inp == '': break
        prompt += f"\n\nUser: {inp}"
        i = asyncio.run(tllm.interrupt(inp))
        prompt += "\n\nAssistant:"
        end = asyncio.run(tllm(prompt))
        print(i)
        print(end)
        prompt += f" {end}"
