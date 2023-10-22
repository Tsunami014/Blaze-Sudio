import languagemodels as lm
import re
try:
    from utils.bot.install_tinyllm import installed
except:
    try:
        from bot.install_tinyllm import installed
    except:
        from install_tinyllm import installed

from googlesearch import search # pip install beautifulsoup4 google
import bs4, requests

def classify(doc: str, *labels: list[str]):

    results = lm.rank_instruct(
        f"Classify as {'or'.join(labels)}: {doc}\n\nClassification:", labels
    )

    return results[0]

def generatelist(query):
    steps = lm.do(query)
    r = lm.config["max_ram"]
    lm.set_max_ram('base')
    code = lm.code(f"""
# a python list that has the following dot points: "{steps}"
l = [""")
    lm.set_max_ram(r)
    try:
        l = eval('['+re.findall('((.|\n)+?])', code)[0][0])
    except Exception as e:
        raise e
    # What this next line does is it replaces the "1. " at the start of each string (but with a different num o course)
    # And also replaces the " 8" at the end of each string (again, with a different num o course)
    return [re.sub(r'( +?\d*?$)', '', re.sub(r'(^\d*?\.? *?(?=[^ ]))', '', i)) for i in l]

def googleit(AIquery, searchquery):
    out = {}
    # to search
    query = searchquery
    
    for j in search(query, tld="co.in", num=10, stop=10, pause=2):
        response = requests.get(j,headers={'User-Agent': 'Mozilla/5.0'})
        soup = bs4.BeautifulSoup(response.text,'lxml')
        txt = soup.body.get_text('\n', strip=True).split('\n')

        out[j] = txt
    lm.docs.clear()
    for i in out:
        for j in out[i]: lm.store_doc(j)
    return lm.get_doc_context(AIquery), out

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
