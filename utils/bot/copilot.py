import AIs, asyncio

print('setup...')
ai = AIs.AI()
def print_generation(txt):
    print('running...')
    asyncio.run(ai(txt))
    seen = ''
    while ai.still_generating():
        if ai.resp != seen:
            print(ai.resp[len(seen):], end='')
            seen = ai.resp

print('evaluating...')
asyncio.run(ai.reevaluate())
print_generation('Hello! how are you?')
pass