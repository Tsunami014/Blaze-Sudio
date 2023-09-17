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
## But what list goes in the `start` param?

The `start` param is a list: 
```py
 [
    separator
    below
 ]
```

# The separator
This is what goes in between the description and the `below` section.

e.g.
```
You are a human girl called Grapefruit. You are not afraid to speak your mind.
### conversation ###
Q: How are you Grapefruit?
A: I'm good thanks.
Q: [Your input]
A: 
```
where in that one the separator is `### conversation ###`

## Separator values:
The separator is a tuple. These are the possible first values:
| Value | What it does | Pros | Cons |
|:------|:------------:|-----:|-----:|
| 0 | `## Conversation:` | It tells exactly what's coming next (a conversation in this case) | It's long |
| 1 | `##` | It's short | It doesn't tell what's coming next |
| 2 | `######` | It's short-ish | It doesn't tell what's coming next and its quite long... |
| 3 | nothing | It doesn't take up any space | It doesn't say that the conversation starts here, you may get whacky results, but in most cases it'll *probably* be fine... |

And these are the possible second values:
Example:
```
A
You are a human girl called Grapefruit. You are not afraid to speak your mind.
B
Q: How are you Grapefruit?
A: I'm good thanks.
Q: [Your input]
A: 
```
Values list:
| Value | Where it places the ones from the first value in the list | Pros | Cons |
|:------|:------------:|-----:|-----:|
| 0 | nowhere |  | It effectively doesn't do anything. Do not use this option |
| 1 | A |  | It doesn't do what the first value was trying to achieve. Do not use this option |
| 2 | B | It does what the first value was trying to achieve | It is only one separator, which may/may not be bad... |
| 3 | A & B | It clearly describes what each section of the input is trying to achieve | It is quite long... |

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
Grapefruit has a strong personality, and is not afraid to speak her mind.
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
|       | Doesn't say WHO to complete, just says to complete. |

3:
```
Grapefruit has a strong personality, and is not afraid to speak her mind.
Finish this conversation:
Person: How are you Grapefruit?
Grapefruit: I'm good thanks.
Person: [Your input]
Grapefruit: 
```
| pros: | cons: |
|:------|------:|
|Tells you who says what, good for multi-characters|very large|
| Allows adding for a name for the user |The more messages, the more characters needed (10 for 'grapefruit' instead of 3 for 'you'), but I guess this isn't that bad, but I guess what's more bad is the large amount of description needed at the start, though maybe this can be avoided with a little prompt engineering.|
|       | Doesn't say WHO to complete, just says to complete. |
