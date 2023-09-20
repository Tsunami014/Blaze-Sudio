try:
    from utils.conversion_parse.consts import *
except ImportError:
    try:
        from conversion_parse.consts import *
    except ImportError:
        from consts import *

# FOR SAMPLES SEE THE BOTTOM OF THIS FILE

def wt(txt): # word tokenize
    l = list(txt)
    out = []
    tmp = ''
    for i in l:
        if i in ['`', ')', '(', '|']:
            if tmp != '': out.append(tmp)
            tmp = ''
            out.append(i)
        else:
            tmp += i
    if tmp != '': out.append(tmp)
    return out

def parseKWs(kwargs, possible, requireds=[]):
    allrequ = {}
    for i in range(len(requireds)):
        if isinstance(requireds[i], str): allrequ[requireds[i]] = i
        else:
            for _ in list(requireds[i]): allrequ[_] = i
    rs = [True for _ in range(len(requireds))]
    for a in kwargs:
        if a not in possible:
            raise ValueError(
                f'Unknown kwarg "--{a}"\nAvaliable args: "{" ".join("--"+_ for _ in possible)}"'
            )
        if a in allrequ.keys(): rs[allrequ[a]] = False
    if any(rs):
        find = []
        for i in range(len(requireds)):
            if rs[i]:
                if isinstance(requireds[i], str): find.append('--'+requireds[i])
                else: find.append('('+' or '.join(['--'+_ for _ in list(requireds[i])])+')')
        raise ValueError(
            f'Missing required kwargs: "{" ".join(find)}"'
        )

def SL(txt, lvl=1): # Set Level
    amnt = ''.join(['`' for _ in range(lvl)])
    return amnt + txt + amnt

class Summary:
    def __init__(self, description=''):
        """
        A class for summarising text, useful for descriptions of things that need to be shortened.
        If you need it... `docs/summary syntax.md`

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
        If you need it... `docs/summary syntax.md`

        Parameters
        ----------
        description : str
            the text to summarise
        """
        self.txt = self.parse(description)
    
    def parse(self, description):
        """
        parses the description into a list of dicts, each dict has a 'txt' and 'lvl' key, 'txt' is the text, 'lvl' is the level of the summary, 0 is the highest level, 1 is the next highest, etc.
        If you need it... `docs/summary syntax.md`

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
        lvl = 0
        prev = 0 # 0 = nothing was before, 1 = going up, 2 = going down
        l = []
        group = False #TODO: groups IN groups
        temp = ''
        for i in wt(description):
            if i == '(':
                group = []
                temp = ''
            elif i == ')':
                if temp != '': group.append(Summary(temp))
                temp = ''
                l.append(group)
                group = False
            elif i == '|':
                if group != False:
                    if temp != '': group.append(Summary(temp))
                    temp = ''
            else:
                if group is False:
                    l.append(i) if i != '``' else l.extend(['`', '`'])
                else:
                    temp += i
        temp = []
        for wrd in l:
            if isinstance(wrd, list):
                end.append(wrd)
            elif wrd == '`':
                if prev == 0:
                    if temp != []:
                        end.append({'txt': ''.join(temp), 'lvl': lvl})
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
            end.append({'txt': ''.join(temp), 'lvl': lvl})
        return end
    
    def get(self, summary_lvl):
        """
        gets the summary at the specified level of summarisation

        Parameters
        ----------
        summary_lvl : int
            the level of summarisation to get, 0 gets pretty much the whole text, 1 gets some and leaves out others, etc.

        Returns
        -------
        str
            the summary of self.txt at the specified level
        """
        res = []
        for i in self.txt:
            if isinstance(i, list):
                for j in i:
                    if j.get(summary_lvl) != '':
                        res.append(j.get(summary_lvl))
                        break
            elif i['lvl'] >= summary_lvl:
                res.append(i['txt'])
        return ''.join(res)

    def __add__(self, add2): # For combining Summaries, e.g. combine character details with knowledge.
        if isinstance(add2, str):
            add2 = Summary(add2)
        if isinstance(add2, Summary):
            self.txt.extend(add2.txt)
        else:
            raise TypeError(
                'Cannot add Summary to class ' + str(type(add2))
            )

class DescSummary():
    # TODO: generate a summary of description that can change - e.g.
    # Have it so that you can return a summarised version of 'Grapefruit is a kind human girl' OR a summarised version of 'You are Grapefruit, a kind human girl.'
    def __init__(self, selfname):
        self.clauses = {}
        self.selfname = selfname
    def add_clause(self, who=None, **kwargs):
        """
        Adds a clause to self. This is (for example) 'You are Grapefruit' or 'Kinkajou is kind'
        This uses Summary syntax, see `docs/summary syntax.md`

        Parameters
        ----------
        who : str, optional
            The name of the classification that has this trait, by default self
        
        kwargs
        ------
        adjs : str/Summary/list[str/Summary]
            The list of adjectives ('kind', 'rough') to use.
        thoughts : str/Summary/list[str/Summary]
            The thoughts of a classification. (e.g. loves, how they feel about things, etc.)
        nouns : str/Summary/list[str/Summary]
            The nouns of a classification. (e.g. for a character a noun could be 'human' saying they are a human)
        part : str
            The part of the who that is described. This by default is just the whole who.
        
        For the kwargs (adjs, thoughts or nouns), the following applies:
            If given a string will split the string by " " to create a list of Summary classes.
            If given a Summary it will put it in a list by itself, e.g. [Summary]
            If given a list of strings it will turn each of the strings into Summary classes, though it will not split them up.
            If given a list of Summary classes it will just leave it as it is.
            If given a list of mixed strings and Summaries it will convert the strings to Summaries.
        
        For kwargs you MUST include:
         - adjs OR thoughts OR nouns
        
        Examples for this function:
         - Grapefruit is kind and nice = (who='Grapefruit', adjs=')
        """
        parseKWs(kwargs, ['adjs', 'thoughts', 'nouns', 'part'], [('adjs', 'thoughts', 'nouns')])
        
        for a in kwargs:
            if a in ['part']:
                if isinstance(kwargs[a], str): pass
                else:
                    raise TypeError(
                        'Invalid type for kwarg "--part" (which should be str): '+str(type(kwargs[a]))
                    )
            if isinstance(kwargs[a], str): kwargs[a] = [Summary(i) for i in a.split(' ')]
            elif isinstance(kwargs[a], Summary): kwargs[a] = [kwargs[a]]
            elif isinstance(kwargs[a], list):
                if all([isinstance(i, str) for i in kwargs[a]]):
                    kwargs[a] = [Summary(i) for i in kwargs[a]]
                elif all([isinstance(i, Summary) for i in kwargs[a]]): pass
                else:
                    for i in kwargs[a]:
                        if isinstance(i, Summary): pass
                        elif isinstance(i, str): i = Summary(i)
                        else:
                            raise TypeError(
                                f'Invalid type for value {i} from list kwarg "--{a}" (which should be str or a Summary): {type(i)}'
                            )
            else:
                raise TypeError(
                    f'Invalid type for kwarg "--{a}" (which should be str or a Summary): {type(a)}'
                )
        if who == None: who = self.selfname
        if str(who) in self.clauses:
            for i in self.clauses[str(who)]:
                i['adjs'].extend(kwargs.pop('adjs', []))
                i['thoughts'].extend(kwargs.pop('thoughts', []))
                i['nouns'].extend(kwargs.pop('nouns', []))
        else:
            self.clauses[str(who)] = {'adjs': kwargs.pop('adjs', []), 'thoughts': kwargs.pop('thoughts', []), 'nouns': kwargs.pop('nouns', [])}
    def get(self, summary_lvl, tense):
        if tense not in ALLTENSES:
            raise ValueError(
                f'Tense "{tense}" is not a valid tense! Valid tenses are: {ALLTENSES}'
            )
        res = []
        for i in self.clauses:
            res.append('%s %s' % (i['who'], i['verbs'].get(summary_lvl)))
        return ''.join(res)

#DS = DescSummary('Grapefruit')
#DS.add_clause('kind human girl')
#pass

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
