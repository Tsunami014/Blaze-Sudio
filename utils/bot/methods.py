#If it returns True it will continue generating. If it returns False, it will stop.
#If it returns a string, that will override the bot's response and get it to stop generating.
#It takes 2 parameters - the token it produced and the whole text it has generated so far.
#It also takes customisations too!

def infinite(token, whole, printfunc=lambda tok: print(tok, end='')): #make the bot generate infinitely
    """
    Generates until it reaches max limit

    Customisations
    ----------
    printfunc : function(token), optional
        The function if you want to print something, e.g. lambda tok: print(tok, end=''), by default prints the result token by token.
    """    
    printfunc(token)
    return True

def untilNext(token, whole, printfunc=lambda tok: print(tok, end='')):
    """
    Generates until it hits "User: " or "### Prompt" in the output

    Customisations
    ----------
    printfunc : function(token), optional
        The function if you want to print something, e.g. lambda tok: print(tok, end=''), by default prints the result token by token.
    """    
    printfunc(token)
    if 'User: ' in whole:
        return whole[:whole.index('User: '):] # override the end result to remove the 'User: ' part, and stop generating
    if '### Prompt' in whole:
        return whole[:whole.index('### Prompt'):]
    #We do not need return True here as it does this for us!
