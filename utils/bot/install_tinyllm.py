import languagemodels as lm

import os, re, json
bef = re.findall(r'((utils\/?)?(bot)?\n)', os.getcwd().replace('\\','/')+'\n')[0][0][:-1] # inp ends in newline
bef = '/'.join([i for i in ['utils', 'bot'] if i not in bef.split('/')])
if bef != '': bef += '/'

# NOTE: The chat models for anything lower than 4 GB SUCK LIKE HELL
# I TRIED TO MAKE THEM WORK AND THEY WON'T
# KEEP THE CHAT AT 4GB

def installed(new=None): # if new == None, don't change anything
    with open(f'{bef}preferences.json', 'r+') as f:
        d = json.load(f)
        if new != None:
            d['downloaded tinyllms'] = new
            json.dump(d, f, indent=4)
    return d['downloaded tinyllms']

def install_tinyllm(ram):
    # basically, this just runs everything that is in the library so it installs all the models it needs for all the tasks
    ram = lm.set_max_ram(ram)
    lm.do("What color is the sky?")
    lm.complete("She hid in her room until")
    lm.code("""
a = 2
b = 5
# Swap a and b
""")
    lm.get_wiki('Chemistry')
    lm.get_weather(41.8, -87.6)
    lm.get_date()
    context = "There is a green ball and a red box"
    lm.extract_answer("What color is the ball?", context).lower()
    lm.classify("That movie was terrible.","positive","negative")
    lm.store_doc("Paris is in France.")
    lm.store_doc("Paris is nice.")
    lm.store_doc("The sky is blue.")
    lm.get_doc_context("Where is Paris?")
    lm.docs.clear()
    lm.store_doc(lm.get_wiki("Python"), "Python")
    lm.store_doc(lm.get_wiki("C language"), "C")
    lm.store_doc(lm.get_wiki("Javascript"), "Javascript")
    lm.get_doc_context("What does it mean for batteries to be included in a language?")
    ram = lm.set_max_ram(4)
    lm.chat(f'''
    System: Respond as a helpful assistant. It is {lm.get_date()}
    User: What time is it?
    Assistant:''')
    installed(installed() + [ram])

def install_all_fast():
    install_tinyllm('base')

def install_all_slow():
    install_tinyllm('4gb')

def test_tinyllm():
    lm.set_max_ram('base')
    # default RAM: 0.48gb ("base")
    print(lm.do("What color is the sky?"))
    print(lm.do("What is the capital of France?"))
    print(lm.do("If I have 7 apples then eat 5, how many apples do I have?"))
    #lm.set_max_ram('4gb') # increase this so that the models it selects are more powerful
    # but the thing is, I have better models that are faster than the ones that are with 4gb anyways
    #print(lm.do("If I have 7 apples then eat 5, how many apples do I have?"))
    #lm.set_max_ram('base')
    print(lm.complete("She hid in her room until"))
    print(lm.code("""
a = 2
b = 5
# Swap a and b
"""))
    lm.set_max_ram('4gb')
    print(lm.chat('''
    System: Respond as a helpful assistant.
    User: What time is it?
    Assistant:'''))
    lm.set_max_ram('base')
    print(lm.get_wiki('Chemistry'))
    print(lm.get_weather(41.8, -87.6))
    print(lm.get_date())
    lm.set_max_ram('4gb')
    print(lm.chat(f'''
System: Respond as a helpful assistant. It is {lm.get_date()}
User: What time is it?
Assistant:'''))
    lm.set_max_ram('base')
    context = "There is a green ball and a red box"
    print(lm.extract_answer("What color is the ball?", context).lower())
    print(lm.classify("That movie was terrible.","positive","negative"))
    lm.store_doc("Paris is in France.")
    lm.store_doc("Paris is nice.")
    lm.store_doc("The sky is blue.")
    print(lm.get_doc_context("Where is Paris?"))
    lm.docs.clear()
    lm.store_doc(lm.get_wiki("Python"), "Python")
    lm.store_doc(lm.get_wiki("C language"), "C")
    lm.store_doc(lm.get_wiki("Javascript"), "Javascript")
    print(lm.get_doc_context("What does it mean for batteries to be included in a language?"))

if __name__ == '__main__':
    test_tinyllm()