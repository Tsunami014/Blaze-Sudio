from nltk import word_tokenize as wt
from nltk.tokenize.treebank import TreebankWordDetokenizer as TWD

def SL(txt, lvl=1): # Set Level
    amnt = ''.join(['`' for _ in range(lvl)])
    return amnt + txt + amnt

class Summary:
    def __init__(self, description=''):
        """
        A class for summarising text, useful for descriptions of things that need to be shortened.

        Parameters
        ----------
        description : str
            the text to summarise, defaults to nothing
        """
        if description != '': self.txt = self.parse(description)
        else: self.txt = []
    
    def parse_into_txt(self, description):
        """
        Parses the description into self.txt, to be gotten by self.get(num)

        Parameters
        ----------
        description : str
            the text to summarise
        """
        self.txt = self.parse(description)
    
    def parse(self, description):
        """
        parses the description into a list of dicts, each dict has a 'txt' and 'lvl' key, 'txt' is the text, 'lvl' is the level of the summary, 0 is the highest level, 1 is the next highest, etc.

        Parameters
        ----------
        description : str
            the text to summarise

        Returns
        -------
        list[dict[]]
            the parsed text
        """
        end = []
        temp = []
        lvl = 0
        prev = 0 # 0 = nothing was before, 1 = going up, 2 = going down
        l = []
        for i in wt(description): l.append(i) if i != '``' else l.extend(['`', '`'])
        for wrd in l:
            if wrd == '`':
                if prev == 0:
                    if temp != []:
                        end.append({'txt': TWD().detokenize(temp), 'lvl': lvl})
                        temp = []
                    if lvl != 0:
                        lvl -= 1
                        if lvl != 0:
                            prev = 2
                    else:
                        lvl += 1
                        prev = 1
                elif prev == 1:
                    lvl += 1
                else: # prev == 2
                    lvl -= 1
                    if lvl == 0:
                        prev = 0
            else:
                temp.append(wrd)
                prev = 0
        if temp != []:
            end.append({'txt': TWD().detokenize(temp), 'lvl': lvl})
        return end
    
    def get(self, summary_lvl):
        """
        gets the summary at the specified level of summarisation

        Parameters
        ----------
        summary_lvl : int
            the level of summarisation to get, 0 is the highest level, 1 is the next highest, etc.

        Returns
        -------
        str
            the summary of self.txt at the specified level
        """
        res = []
        for i in self.txt:
            if i['lvl'] <= summary_lvl:
                res.append(i['txt'])
        return TWD().detokenize(res)

# print(Summary().parse('`Hello!```Bye.``Hi again!'))
# print(Summary().parse('%s%s - noo! %s' % (SL('Hello!', 2), SL('Wait...'), SL('I forgot!!', 10))))

def PARSE(cnvrs, summary_level, prompt_type):
    """
    _summary_

    Parameters
    ----------
    cnvrs : list[dict[]]
        The conversation input. Just make a conversation with the 'discussion.py' file and use the get_messages func
    summary_level : int
        0-10, 0 = not summarised at all, 10=basically 3 words long
    prompt_type : int
        see `doc/character start.md`, this value is that.

    Returns
    -------
    str
        The conversation, but parsed
    """
    full_prompt = ''
    for message in cnvrs:
        if message["role"] == "user":
            full_prompt += 'user: ' + message["content"] + '\n'
        if message["role"] == "assistant":
            full_prompt += 'assistant: ' + message["content"] + '\n'
    return full_prompt
