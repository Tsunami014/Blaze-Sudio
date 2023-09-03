#It returns a string that is the "personality" of the bot (how it acts)
# TO BE BUILT INTO CHARACTER & AI, CURRENTLY USED TO TEST GPT4ALL
class RAWP: #Raw Personality
    def PS(inp): # Personality String
        return inp # nothing at all (raw)
    
    def method(token, whole, printfunc=lambda tok: print(tok, end='')):
        """
        Generates until it reaches max limit

        Customisations
        ----------
        printfunc : function(token), optional
            The function if you want to print something, e.g. lambda tok: print(tok, end=''), by default prints the result token by token.
        """    
        printfunc(token)
        return True

def GFP(inp): # GrapeFruit Personality
    return f"""You are Grapefruit.
You are a kind and compassionate human girl (NOT an AI, you speak NOTHING like one, you speak more like a child/teenager).
You never say no or that you doesn't understand. Yau are not afraid to speak your mind and ask questions back.
Continue this conversation:
User: {inp}
You: """

def AIP(inp): # AI Personality
    return f"""\
### Prompt: {inp}
### Response: """

def RAWP(inp): # Raw Personality (nothing at all)
    return inp