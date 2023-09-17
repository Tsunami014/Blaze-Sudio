from nltk import word_tokenize as wt
from nltk.tokenize.treebank import TreebankWordDetokenizer as TWD

# FOR SAMPLES SEE THE BOTTOM OF THIS FILE

# 0 = no names, 1 = bot name, 2 = user name, 3 = both names
STARTNAMES = [
    0, 0, 1, 2
]

STARTPARAM1 = [
    {
        'user': '\nQ: ',
        'bot': '\nA: '},
    {
        'user': '\nUser: ',
        'bot': '\nYou: ',
        'other': '\n{0}: '
    },
    {
        'user': '\nUser: ',
        'other': '\n{0}: '
    },
    {
        'other': '\n{0}: '
    }
]
STARTPARAM2 = [
    {
        'A': '## Description:\n',
        'B': '\n## Conversation:'
    },
    '\n##',
    '\n######',
    ''
]

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

    def __add__(self, add2): # For combining Summaries, e.g. combine character details with knowledge.
        # Please note this takes 2 options for inputs - strings or Summary.
        pass

# print(Summary().parse('`Hello!```Bye.``Hi again!'))
# print(Summary().parse('%s%s - noo! %s' % (SL('Hello!', 2), SL('Wait...'), SL('I forgot!!', 10))))

def PARSE(start, description, prompt, bot_name, summary_level=0):
    """
    Creates a string based off 'start' params.

    Parameters
    ----------
    start : iterable
        see `doc/character start.md`
    description : Summary or str
        The descrition of anything the AI needs to know (e.g. You are a kind and loving person. etc.). If string will not process it. BEWARNED.
    prompt : dict
        [{'role': role, 'content': content}]
    bot_name : str #TODO: REMOVE THIS PARAM
        the name of the bot. This is only used if the start param uses the bot's name, so at the end
        of the prompt it uses the name to prompt the AI, e.g. 'Grapefruit: '. Otherwise, the name of
        the bot is taken from the prompt.
    summary_level : int
        0-10, 0 = not summarised at all, 10=basically 3 words long. THIS IS ONLY FOR SUMMARISING THE DESCRIPTION, see `description` param.
    """
    if isinstance(description, str):
        desc = description
    elif isinstance(description, Summary):
        desc = description.get(summary_level)
    else:
        desc = ''
    end = ''
    add = STARTPARAM2[start[0][0]]
    if start[0][1] in [1, 3]:
        if isinstance(add, dict): end += add['A']
        else: end += add # assuming it's otherwise a string
    end += desc
    if start[0][1] in [2, 3]:
        if isinstance(add, dict): end += add['B']
        else: end += add
    add = STARTPARAM1[start[1]]
    ks = list(add.keys())
    if 'other' in ks: ks.remove('other')
    for i in prompt:
        if i['role'] == 'assistant': i['role'] = 'bot'

        if i['role'] in ks:
            end += add[i['role']]
        else:
            if 'other' in add.keys():
                end += add['other'].format(i['role'])
            else:
                raise ValueError(
                    f'Invalid role "{i["role"]}" for start param "{start[1]}" which cannot take multi inputs.'
                )
        end += i['content']
    if 'bot' in add.keys(): end += add['bot']
    else:
        if 'other' in add.keys():
            end += add['other'].format(bot_name)
        else:
            raise ValueError(
                f'Invalid role "bot" for start param {start[1]} which cannot take multi inputs. And this error is very rare and should not happen.'
            )
    return end

def parse_prompt(prompt, botNAME, userNAME, start):
    rpl = {}
    rpls = STARTNAMES[start[1]]
    if rpls == 1: rpl['bot'] = botNAME
    elif rpls == 2: rpl['user'] = userNAME
    elif rpls == 3:
        rpl['bot'] = botNAME
        rpl['user'] = userNAME
    
    for i in prompt:
        if i['role'] in rpl.keys():
            if i['role'] == 'assistant': i['role'] = 'bot'
            i['content'] = i['content'].replace(rpl[i['role']], i['role'])
    return prompt

if __name__ == '__main__':
    from random import randint
    def sample(start):
        sample_prompt = [{'role': 'user', 'content': 'Hello! How are you?'}, {'role': 'bot', 'content': 'I am good, how are you?'}, {'role': 'user', 'content': 'I am good too! What did you do today?'}]
        sample_desc = 'Grapefruit has a strong personality, and is not afraid to speak her mind.'
        print(PARSE(start, sample_desc, parse_prompt(sample_prompt, 'Grapefruit', 'User', start), 'Grapefruit'))
        print('\033[%sm~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m' % str(randint(91, 96)))
    # If you run this file you can see these next statements at work
    # Each you can see is separated, by a like of ~~~~~~~~~~
    # You can see the different start params at work, with the same sample prompt
    sample([(1, 2), 2])
    sample([(0, 0), 3])
    sample([(0, 3), 1])
    sample([(3, 1), 2])
    sample([(0, 2), 0])
    pass
