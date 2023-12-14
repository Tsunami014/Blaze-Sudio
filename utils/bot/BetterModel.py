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
system_prompt = "Grapefruit is a happy, kind and helpful human assistant who ALWAYS GIVES 2-WORD ANSWERS TO QUESTIONS."
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

"""
# Use a pipeline as a high-level helper
print('importing...')
from transformers import pipeline

print('Loading model...')
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v0.4")

res = pipe('How are you?\n')

quit()

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.4")
model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.4")

model_inputs = tokenizer(["A list of colors: red, blue"], return_tensors="pt")
streamer = TextStreamer(tokenizer)
quit()

from transformers import AutoTokenizer
import transformers
import torch
# pip install torch transformers>=4.31 accelerate
model = "TinyLlama/TinyLlama-1.1B-Chat-v0.4"
tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float32,
    device_map="auto",
)

CHAT_EOS_TOKEN_ID = 32002

while True:
    prompt = input('> ')
    formatted_prompt = (
        f"<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"
    )


    sequences = pipeline(
        formatted_prompt,
        do_sample=True,
        top_k=50,
        top_p = 0.9,
        num_return_sequences=1,
        repetition_penalty=1.1,
        max_new_tokens=1024,
        eos_token_id=CHAT_EOS_TOKEN_ID,
        stream=True
    )

    for seq in sequences:
        print(f"Result: {seq['generated_text'][len(formatted_prompt):]}")
"""