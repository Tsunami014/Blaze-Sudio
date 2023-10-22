import languagemodels as lm
import re
from difflib import get_close_matches as GCM
try:
    from utils.bot.tinyllm import *
except:
    try:
        from bot.tinyllm import *
    except:
        from tinyllm import *
# This will only work with GPT4all.

class Copilot:
    def __init__(self, name):
        self.name = name
    
    def runtask(self, task):
        strat = lm.do('How would you do this task: "%s"' % task)
        lm.do('What do you need to perform this: "%s"' % task)

    def __call__(self, aim):
        lm.do('What do you need to perform this: "%s"' % aim)
        tasks = generatelist('List the steps to "%s"' % aim)
        #tasks = generatelist('Please output a list of prerequirements you would need for this task: "%s"' % aim)
        #tasks = generatelist('Please output a list of tasks you would need to do for this task: "%s"' % aim)
        #tasks = generatelist('Output a list of all the things you would need to do to accomplish this task: "%s"' % aim)
        print(tasks)

c = Copilot('TranslateGPT')
c('Find out how to translate zonai text')
c()
pass