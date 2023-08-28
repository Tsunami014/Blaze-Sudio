# The start param for the Character class is defined like so

Let's say we have a character called Grapefruit.

## Params for character creation:

```python
GF = Character(
               AI, 
               'Grapefruit', 
               'You are a kind human girl called Grapefruit. You are not afraid to speak your mind.'
               start=
              )
```
## But what number goes in the `start` param?

Let's say in this conversation you've already said `How are you Grapefruit?` and she has already replied `I'm good thanks.`

If the `start` param were to be 0 your input into the AI would look like this:
```
You are a human girl called Grapefruit. You are not afraid to speak your mind.
Q: How are you Grapefruit?
A: I'm good thanks.
Q: [Your input]
A: 
```
| pros: | cons: |
|:------|------:|
|It is small and 'lightweight'|It works in questions and answers, not in anything else|
|       |doesn't work for multiple characters

If the start param were to be 1 it would look like this:
```
You are a human girl called Grapefruit. You are not afraid to speak your mind.
Finish this conversation:
User: How are you Grapefruit?
You: I'm good thanks.
User: [Your input]
You: 
```
| pros: | cons: |
|:------|------:|
|Tells you who says what, good for multi-characters|very large|
|       |Uses You pronouns, may not work for some versions of the parameters|

And for 2:
```
In this conversation, a human girl called Grapefruit is chatting with someone. Grapefruit has a strong personality, and is not afraid to speak her mind.
Finish this conversation:
User: How are you Grapefruit?
Grapefruit: I'm good thanks.
User: [Your input]
Grapefruit: 
```
| pros: | cons: |
|:------|------:|
|Tells you who says what, good for multi-characters|very large|
|       |The more messages, the more characters needed (10 for 'grapefruit' instead of 3 for 'you'), but I guess this isn't that bad, but I guess what's more bad is the large amount of description needed at the start, though maybe this can be avoided with a little prompt engineering.|
|       |
