# Use a pipeline as a high-level helper
print('(1/3) Importing... May take a while...') # Takes a long time
from transformers import pipeline, AutoTokenizer
print('\033[A(1/3) Importing others...                 ')
from transformers.generation.streamers import BaseStreamer
from re import findall, escape

print('\033[A(2/3) Loading model... May take a while...') # Takes a long time
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v0.4")
print('\033[A(2/3) Loading tokenizer...                            ')
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.4")

print('\033[A(3/3) Loading other things and finishing up...              ')
pifg = pipe.model.prepare_inputs_for_generation # A random function with the inputs that are needed for this
class Streamer(BaseStreamer):
    def __init__(self, default):
        self.default = default.replace('<|im_start|>', '').replace('<|im_end|>', '').strip(' ')
        self.sofar = ''
        pipe.model.prepare_inputs_for_generation = self.pifg
    def pifg(self, input_ids, *args, **kwargs):
        val = tokenizer.batch_decode(input_ids, skip_special_tokens=True)[0]
        value = val
        defs = self.default.split('\n')
        for i in findall('[ \n]*?'.join([escape(i) for i in defs])+'\n', value):
            value = value.replace(i, '')
        if value == '':
            self.sofar = ''
            self.start()
        else:
            self.output(value[len(self.sofar):], value)
            self.sofar = value
        return pifg(input_ids, *args, **kwargs)
    
    def put(self, v):
        pass
    def start(self): # Change this if u want :)
        print('Thinking...\nGrapefruit: ', end='')
    def output(self, nexttok, whole): # Change this 2 if u want :D
        print(nexttok, end='')
    def end(self): # ANd once again, change this if u want :)
        print('\nFinished!')

CHAT_EOS_TOKEN_ID = 32002
system_prompt = "Grapefruit is happy, kind and helpful friend. GRAPEFRUIT ALWAYS ANSWERS WITH JUST ONE WORD."
name = "Grapefruit"
history = []

print('\033[ADone! Start chatting now:                                 ')
while True:
    try: inp = input('> ')
    except:
        print('Exiting...')
        break
    history.append(f'<|im_start|>user\n{inp}<|im_end|>')
    history = history[-4:]
    hist = '\n'.join(history)
    if hist != '': hist += '\n'
    prompt = (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n{hist}<|im_start|>{name}\n"
    )
    try:
        res = pipe(prompt, streamer=Streamer(prompt),
            top_k=50,
            # top_p = 0.9, do_sample=True # I don't think this is a good idea
            num_return_sequences=1,
            repetition_penalty=1.1,
            max_new_tokens=1024,
            pad_token_id=CHAT_EOS_TOKEN_ID,
            eos_token_id=CHAT_EOS_TOKEN_ID
        )
        print(res[0]['generated_text'][len(prompt):])
        history.append(f'<|im_start|>{name}\n{res[0]["generated_text"][len(prompt):]}<|im_end|>')
    except: print('\nCancelled!')
