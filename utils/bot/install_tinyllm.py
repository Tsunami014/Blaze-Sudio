import languagemodels as lm
def install_all_fast():
    # basically, this just runs everything that is in the library so it installs all the models it needs for all the tasks
    lm.set_max_ram('base')
    lm.do("What color is the sky?")
    lm.complete("She hid in her room until")
    lm.code("""
    a = 2
    b = 5
    # Swap a and b
    """)
    lm.chat('''
    System: Respond as a helpful assistant.
    User: What time is it?
    Assistant:''')
    lm.get_wiki('Chemistry')
    lm.get_weather(41.8, -87.6)
    lm.get_date()
    lm.chat(f'''
    System: Respond as a helpful assistant. It is {lm.get_date()}
    User: What time is it?
    Assistant:''')
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

def install_all_slow():
    # basically, this just runs everything that is in the library so it installs all the models it needs for all the tasks
    lm.set_max_ram('4gb')
    lm.do("What color is the sky?")
    lm.complete("She hid in her room until")
    lm.code("""
    a = 2
    b = 5
    # Swap a and b
    """)
    lm.chat('''
    System: Respond as a helpful assistant.
    User: What time is it?
    Assistant:''')
    lm.get_wiki('Chemistry')
    lm.get_weather(41.8, -87.6)
    lm.get_date()
    lm.chat(f'''
    System: Respond as a helpful assistant. It is {lm.get_date()}
    User: What time is it?
    Assistant:''')
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
