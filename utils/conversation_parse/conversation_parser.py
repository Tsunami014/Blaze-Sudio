try:
    from utils.conversation_parse.consts import *
except ImportError:
    try:
        from conversation_parse.consts import *
    except ImportError:
        from consts import *
import re
from math import inf

# FOR SAMPLES SEE THE BOTTOM OF THIS FILE

# TODO: replace code with regular expressions

def split(txt):
    tout = []
    spl = txt.split('\n')
    for line in spl:
        tmp = []
        out = re.split(r'([`|(\\)*~])', line) # ((?<!\\)[`|()*~]|\\(?=[^`|()~*]))
        for i in out:
            if i is None: continue
            if i == '': continue
            finds = re.findall(r'\\[^(|~)*]', i)
            if finds != []:
                raise SyntaxError(
                    f'Text "<txt>", line {spl.index(line)}, in <main>\n\
    {line}\n\
    {"".join([" " for _ in range(sum([len(__) for __ in out[:out.index(i)]])+i.index(finds[0]))])}^\n\
BackslashError: backslash escaping a character that is not in: [`, ), ~, |, (, \\, *]'
                )# TODO: in group (not main)
            #for j in re.findall(r'\\(\(|\)|~|\|`)', i): i = i.replace('\\'+j, j)
            tmp.append(i)
        tout.extend(tmp)
    return tout

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
    if lvl == None or lvl == inf:
        return f'*{txt}*'
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
        backslashed = False
        for i in split(description):
            if backslashed:
                if group == False:
                    l.append(i) if i != '``' else l.extend(['`', '`'])
                else:
                    temp += i
                backslashed = False
            elif i == '(':
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
            elif i == '\\':
                backslashed = True
            else:
                if group == False:
                    l.append(i) if i != '``' else l.extend(['`', '`'])
                else:
                    temp += i
        temp = [] # TODO: syntaxError if group hasn't closed off yet
        wrappedininf = False
        for wrd in l:
            if isinstance(wrd, list):
                if temp != []:
                    end.append({'txt': ''.join(temp), 'lvl': lvl})
                    temp = []
                end.append(wrd)
            elif wrd == '*':
                if wrappedininf:
                    end.append({'txt': ''.join(temp), 'lvl': inf})
                    temp = []
                    wrappedininf = False
                else:
                    wrappedininf = True
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
        if wrappedininf: # something went wrong with the infinity wrapping
            place = len(description) - description[::-1].index('*')
            raise SyntaxError(
                f'Text "<txt>", in <main>\n\
{description}\n\
{"".join([" " for _ in range(place)])}^\n\
InfinityError: unequal matchup of infinity creators') # TODO: in <group> and line # 
        return end
    
    def get(self, summary_lvl=0, was_bef=False):
        """
        gets the summary at the specified level of summarisation

        Parameters
        ----------
        summary_lvl : int
            the level of summarisation to get, 0 gets pretty much the whole text, 1 gets some and leaves out others, etc., defaults to 0
        was_bef : bool
            Whether or not there was text before. This means that the ~ parser will act as if there was text before.

        Returns
        -------
        str
            the summary of self.txt at the specified level
        """
        out = ''
        for i in self.txt:
            if isinstance(i, list):
                for j in i:
                    if j.get(summary_lvl) != '':
                        out += j.get(summary_lvl, out!='')
                        break
            elif i['lvl'] >= summary_lvl:
                out += i['txt']
        for i in re.findall('%s~.' % ('' if was_bef else '.'), out): out = out.replace(i, i[0]+' '+i[-1])
        return out.replace('~', '')

    def __add__(self, add2): # For combining Summaries, e.g. combine character details with knowledge.
        if isinstance(add2, str):
            add2 = Summary(add2)
        if isinstance(add2, Summary):
            self.txt.extend(add2.txt)
        else:
            raise TypeError(
                'Cannot add Summary to class ' + str(type(add2))
            )
    
    def __str__(self):
        return self.get(0)
    def __repr__(self): return str(self)

class Knowledge():
    def __init__(self, selfname, **kwargs):
        """
        This class stores knowledge (e.g. Grapefruit is nice and kind)

        Parameters
        ----------
        selfname : str
            The name of this character

        If you know your stuff about this class, you can add kwargs to be passed to self.add_clause for instant adding of the clauses.
        You can still use it, just you may need to see the documentation in that function itself.
        """
        self.clauses = {}
        self.selfname = selfname
        if kwargs != {}:
            self.add_clause(**kwargs)
    def add_clause(self, name=None, **kwargs):
        """
        Adds a clause to self. This is (for example) 'Grapefruit reads books' or 'Kinkajou is a kind dragon'
        This uses Summary syntax, see `docs/summary syntax.md`

        Parameters
        ----------
        name : str, optional
            The name of the classification that has this trait, by default self's name
        
        kwargs
        ------
        is_adjs : str/Summary/list[str/Summary]
            The list of adjectives ('kind', 'rough', 'mean', 'silly') to use.
        is_a : str/Summary
            The noun (or noun group) of a classification. (e.g. 'dog', 'dragon', 'RainWing dragon', etc.)
            Please note that there can only be one is_adj, so it will override the previous one.
            Also, lists aren't allowed for this param either.
        who : str/Summary/list[str/Summary]
            Things that don't fit into the above categories (e.g. 'reads lots', 'licks the floor each night')
        
        For the kwargs (adjs, thoughts or nouns), the following applies:
            If given a string will split the string by "/" to create a list of Summary classes.
            If given a Summary it will put it in a list by itself, e.g. [Summary]
            If given a list of strings it will turn each of the strings into Summary classes, though it will not split them up.
            If given a list of Summary classes it will just leave it as it is.
            If given a list of mixed strings and Summaries it will convert the strings to Summaries.
        
        For kwargs you MUST include:
         - is_adjs OR is_a OR who
        
        Examples for this function:
         - Grapefruit is kind and nice = (name='Grapefruit', adjs='kind ``nice``') (you can see the summary syntax is applied here too)
         - Hinix is a lovelly and kind brown dog who licks the floor clean = (name='Hinix', is_adjs='lovelly kind', is_a='brown dog', who='licks the floor clean')
        """
        parseKWs(kwargs, ['is_adjs', 'is_a', 'who'], [('is_adjs', 'is_a', 'who')])

        kwargs = {i: kwargs[i] for i in kwargs if kwargs[i] != [] and kwargs[i] != '' and kwargs[i] != None}
        
        for a in kwargs:
            if a in ['is_a']:
                if a in ['is_a']:
                    if isinstance(kwargs[a], str): kwargs[a] = Summary(kwargs[a])
                    elif isinstance(kwargs[a], Summary): pass
                    else:
                        raise TypeError(
                            f'Invalid type for kwarg "--{a}" (which should be str or Summary): '+str(type(kwargs[a]))
                        )
                else:
                    if isinstance(kwargs[a], str): pass
                    else:
                        raise TypeError(
                            f'Invalid type for kwarg "--{a}" (which should be str): '+str(type(kwargs[a]))
                        )
            elif isinstance(kwargs[a], str): kwargs[a] = [Summary(i) for i in kwargs[a].split('/')]
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
                    f'Invalid type for kwarg "--{a}" (which should be str, Summary, or list (of strs and/or Summaries)): {type(a)}'
                )
        if name == None: name = self.selfname
        if str(name) in self.clauses:
            self.clauses[str(name)]['is_adjs'].extend(kwargs.pop('is_adjs', []))
            self.clauses[str(name)]['is_a'] = kwargs.pop('is_a', self.clauses[str(name)]['is_a'])
            self.clauses[str(name)]['who'].extend(kwargs.pop('who', []))
        else:
            self.clauses[str(name)] = {'is_adjs': kwargs.pop('is_adjs', []), 'is_a': kwargs.pop('is_a', Summary()), 'who': kwargs.pop('who', [])}
    
    def _parse(self, is_adjs, is_a, who, name):
        is_adjs = [i for i in is_adjs if i != '']
        who = [i for i in who if i != '']
        notblank = [(i != [] and i != '') for i in [is_adjs, is_a, who]]
        #print(is_adjs, is_a, who, name, gender, notblank)
        if all([not i for i in notblank]): return ''
        out = name
        if notblank[0] or notblank[1]:
            out += ' is '
            if notblank[1]:
                out += 'a '
            if notblank[0]:
                if len(is_adjs) > 1:
                    out += ', '.join([i for i in is_adjs[:-1]])
                    if len(who) < 5: out += ' and '
                    else: out += ', '
                out += is_adjs[-1]
            if notblank[1]:
                if notblank[0]:
                    out += ' '
                out += is_a
        if notblank[2]:
            if notblank[0] and notblank[1]:
                out += ' who '
            else:
                out += ' '
            if len(who) > 1:
                out += ', '.join([i for i in who[:-1]])
                if len(who) < 5: out += ' and '
                else: out += ', '
            out += who[-1]
        return out + '.'
    
    def get(self, summary_lvl=0, topics=None):
        if topics == None: topics = [self.selfname]
        res = ''
        for i in topics:
            if i in self.clauses:
                res += self._parse([i.get(summary_lvl) for i in self.clauses[i]['is_adjs']], 
                                   self.clauses[i]['is_a'].get(summary_lvl), 
                                   [i.get(summary_lvl) for i in self.clauses[i]['who']], 
                                   i #.get(summary_lvl)
                )
        return res

# print(Summary().parse('`Hello!```Bye.``Hi again!'))
# print(Summary().parse('%s%s - noo! %s' % (SL('Hello!', 2), SL('Wait...'), SL('I forgot!!', 10))))

def PARSE(start, desc, prompt, bot_name):
    """
    Creates a string based off 'start' params.

    Parameters
    ----------
    start : iterable
        see `doc/character start.md`
    desc : str (should be parsed already from Summary or Knowledge classes)
        The descrition of anything the AI needs to know (e.g. You are a kind and loving person. etc.). If string will not process it. BEWARNED.
    prompt : dict
        [{'role': role, 'content': content}]
        (if given a string will imagine that 'system' said that)
    bot_name : str #TODO: REMOVE THIS PARAM
        the name of the bot. This is only used if the start param uses the bot's name, so at the end
        of the prompt it uses the name to prompt the AI, e.g. 'Grapefruit: '. Otherwise, the name of
        the bot is taken from the prompt.
    """
    if isinstance(prompt, str): prompt = [{'role': 'system', 'content': prompt}]
    prompt = parse_prompt(prompt, bot_name, 'User', start)
    end = ''
    add = STARTPARAM2[start[0][0]]
    if isinstance(add, dict) and 'NLs' in add.keys():
        end += add['NLs'].format(desc)
    else:
        if start[0][1] in [1, 3]:
            if isinstance(add, dict): end += add['A']
            else: end += add # assuming it's otherwise a string
            end += '\n'
        end += desc
        if start[0][1] in [2, 3]:
            end += '\n'
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

def PARSE2(systemmsg, prompt, end_with_assistant=False):
    if isinstance(prompt, str): prompt = [{'role': 'System', 'content': systemmsg}, {'role': 'User', 'content': prompt}]
    elif systemmsg != '': prompt = [{'role': 'System', 'content': systemmsg}] + list(prompt)
    prompt = parse_prompt(prompt, 'Assistant', 'User', [(3, 0), 2])
    end = ''
    for i in prompt:
        end += f'\n{i["role"]}: {i["content"]}'
    end += '\nAssistant:'
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
        if 'role' in rpl.keys():
            if i['role'].lower() == 'assistant': i['role'] = 'bot'
            try:
                i['content'] = i['content'].replace(rpl[i['role'].lower()], i['role'])
            except KeyError: pass
        else:
            try:
                i['role'] = i['sender']
                if i['role'].lower() == 'assistant': i['role'] = 'bot'
                try:
                    i['content'] = i['content'].replace(rpl[i['role'].lower()], i['role'])
                except KeyError: pass
            except: pass
    return prompt

def cycle(my_list, start_at=None):
    start_at = 0 if start_at is None else start_at
    while True:
        yield my_list[start_at]
        start_at = (start_at + 1) % len(my_list)

if __name__ == '__main__':
    from random import shuffle, choice, randint
    class Generator:
        def __init__(self):
            l = list(range(91, 96))
            shuffle(l)
            self.order = cycle(l)
            self.order2 = cycle(l, 2)
        def generate_desc(self):
            K = Knowledge('Grapefruit')
            self.args = {'is_adjs':choice([None, 'nice', 'nice/kind', 'nice/kind/happy/beautiful']), 
                'is_a':choice([None, 'dragon', 'human', 'elf', 'wizard', 'brown dog']), 
                'who':choice([None, 'loves life', 'reads lots/codes', 'gets bored easily/loves life/reads a lot/codes', 'always wears brown clothing'])
            }
            K.add_clause(**self.args)
            return K.get(0)
        def __call__(self, start=None):
            out = ''
            if start == None: start = [(randint(0, 3), randint(0, 4)), randint(0, len(STARTPARAM1)-1)]
            sample_prompt = choice([
                [{'role': 'user', 'content': 'Hello! How are you?'}, {'role': 'bot', 'content': 'I am good, how are you?'}, {'role': 'user', 'content': 'I am good too! What did you do today?'}],
                [{'role': 'user', 'content': 'Hello'}, {'role': 'bot', 'content': 'Hello! What can I help you with today?'}, {'role': 'user', 'content': 'I dunno...'}, {'role': 'bot', 'content': 'Well, I can help you with anything! Just pick a topic!'}, {'role': 'user', 'content': 'I like books'}, {'role': 'bot', 'content': 'I like books too! What is your favourite book?'}, {'role': 'user', 'content': 'I like Harry Potter'}],
                [{'role': 'user', 'content': 'Hello! How are you?'}, {'role': 'bot', 'content': 'What can I help you with?'}, {'role': 'user', 'content': 'I need help with a Python project.'}],
                [{'role': 'user', 'content': 'What is the best way to handle errors in Python?'}, {'role': 'bot', 'content': 'There are several ways to handle errors in Python, such as using try-except blocks or raising exceptions. What kind of errors are you trying to handle?'}, {'role': 'user', 'content': 'I\'m trying to handle file I/O errors.'}],
                [{'role': 'user', 'content': 'How do I install a Python package using pip?'}, {'role': 'bot', 'content': 'You can install a Python package using pip by running the command "pip install package_name" in your terminal. Have you used pip before?'}, {'role': 'user', 'content': 'No, I haven\'t. Can you walk me through it?'}]
            ])
            sample_desc = 'You are Grapefruit. '+self.generate_desc()
            self.args['start'] = start
            out += '\033[%sm| ' % str(next(self.order2))
            pretty = lambda x: '"' if isinstance(x, str) else ''
            for i in self.args: out += i+' : '+pretty(self.args[i])+str(self.args[i])+pretty(self.args[i])+' | '
            out += '\033[0m\n'
            out += PARSE(start, sample_desc, sample_prompt, 'Grapefruit')+'\n'
            out += '\033[%sm~~~~~~~~~~~~~~~~~~~~~~~~~\033[0m' % str(next(self.order))
            return out
    # If you run this file you can see these next statements at work
    # Each you can see is separated, by a like of ~~~~~~~~~~
    # You can see the different start params at work, with the same sample prompt
    def gen():
        g = Generator()
        yield g([(1, 2), 2])
        yield g([(0, 0), 3])
        yield g([(0, 3), 1])
        yield g([(3, 1), 2])
        yield g([(0, 2), 0])
        yield '\nAnd here are some randomly generated ones:\n' + g()
        while True:
            yield g()
    g = gen()
    print('Here are some I prepared earlier:\n')
    while True:
        print(next(g))
        if input() != '':
            break
