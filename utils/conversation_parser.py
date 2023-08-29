from nltk import word_tokenize as wt
from nltk.tokenize.treebank import TreebankWordDetokenizer as TWD

def SL(txt, lvl=1): # Set Level
    amnt = ''.join(['`' for _ in range(lvl)])
    return amnt + txt + amnt

class Summary:
    def __init__(self, description):
        self.txt = self.parse(description)
    
    def parse(self, description):
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

# print(Summary('`Hello!```Bye.``Hi again!').txt)
# print(Summary('%s%s - noo! %s' % (SL('Hello!', 2), SL('Wait...'), SL('I forgot!!', 987))).txt)

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
        see `doc/character start int.md`, this value is that.

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
