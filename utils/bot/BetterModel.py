# Use a pipeline as a high-level helper
print('(1/3) Importing... (1/3)')
from transformers import pipeline, AutoTokenizer
print('\033[A(1/3) Importing... (2/3)')
from transformers.generation.streamers import BaseStreamer
print('\033[A(1/3) Importing... (3/3)')
from re import findall

print('\033[A(2/3) Loading model & tokenizer... (1/2)')
pipe = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v0.4")
print('\033[A(2/3) Loading model & tokenizer... (2/2)')
tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v0.4")

print('\033[A(3/3) Loading other things and finishing up...              ')
class Streamer(BaseStreamer):
    def __init__(self, default):
        self.default = default.replace('<|im_start|>', '').replace('<|im_end|>', '').strip(' ')
        for i in findall('[ \t]+?\n[ \t]+?', self.default):
            self.default = self.default.replace(i, '\n')
        self.whole = ''
    def put(self, value):
        val = tokenizer.batch_decode(value)[0].replace('<|im_start|>', '').replace('<|im_end|>', '')
        value = val.strip(' ')
        for i in findall('[ \t]+?\n[ \t]+?', value):
            value = self.default.replace(i, '\n')
        if value == self.default:
            self.whole = ''
            self.start()
        else:
            self.whole += val
            self.output(val, self.whole)
    def start(self):
        pass
    def output(self, val, whole):
        if whole == val: # It has nothing else in it but the value, so it just started generating
            print('Generating...')
            print('Grapefruit: ', end='')
        print(val, end='')
    def end(self):
        print('\nFinished!')

CHAT_EOS_TOKEN_ID = 32002
system_prompt = "Grapefruit is a happy, kind and helpful human assistant who rarely speaks more than a word."
name = "Grapefruit"

print('\033[ADone! Start chatting now:                                 ')
while True:
    inp = input('> ')
    print('Thinking...')
    prompt = (
        f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{inp}<|im_end|>\n<|im_start|>{name}\n"
    )
    res = pipe(prompt, streamer=Streamer(prompt),
        top_k=50,
        # top_p = 0.9, do_sample=True # I don't think this is a good idea
        num_return_sequences=1,
        repetition_penalty=1.1,
        max_new_tokens=1024,
        pad_token_id=CHAT_EOS_TOKEN_ID,
        eos_token_id=CHAT_EOS_TOKEN_ID
    )

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