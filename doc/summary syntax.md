# Summary syntax
------------------------------------

## The backticks (\`)
------
Encasing anything in backticks (\`) makes it more important.

e.g.
\`\`hi\`\` makes the statement `hi` have an importance of 2, so when you ask for a summary of it to a summary level of 2 or less, it will include that wheras if you have \`bye\` that shows the word `bye` has an importance of 1, so when you ask for a summary of it to a summary level of 1 or lower it will include that, but a summary level of 2 will exclude it but include \`\`hi\`\` and anything above 2 will not include either of them.

## Groups ('or' syntax)
------
To make a group you need to encase the words in brackets, and to separate each element in a group you use the pipe (`|`).

The group works so that it goes through each element of the group until it finds one that isn't blank and uses that.

E.g. (\`hi\`|\`\`bye\`\`)

So in that example above you can see that the word `hi` has an importance of 1, and `bye` has an importance of 2. So if you asked for a summary level of 1 or less the first element on the list that is not blank is `hi`, but a summary level of 2 would mean that `hi` (with it's importance of 1 being lower than the asked for 2) is blank as it does not contain anything that fits the asked for level of 2. So, it would go to the next element and use it as it works (`bye`). And anything higher than that, neither element of the list works so it will be blank.

## Combining
------

If you had something like \`hi\`\`\`bye\`\` I think you would be confused. No? Well, if you look carefully you can separate it.

How you should look at this to make it make more sense (and also how the compiler looks at it) is shown below:

1. Look at the first word. It is encased with one back tick. Yes, it has multiple on the right side, but look:

    If you had something like \`hi\`\` that would not be correct, as what importance level would that be? (My compiler would say that is one, but that's not the point. If you had anything after that it would stuff that next text up.)

    So to find out what importance level something has, start from the start and count the back ticks.

2. Now we know that `hi` has an importance level of 1, we can now see that if we remove it entirely from the text we get \`\`bye\`\` which has an importance level of 2!!

So now we can see in that example shown above, `hi` has an importance level of 1 and `bye` has an importance level of 2.

### Now what if you asked for the importance level of the whole thing?

Well, in the example above, if you asked for an importance level of 0, it would give you `hi bye`. Why? We didn't tell it to give any spaces! The answer is that it separates each word to compile the text, so to put it back together again it uses a retokenizer. Don't stress about it too hard, it just means that in some cases, the spacing will stuff up. See `Warnings and FAQ` below.

Anyways, so a summary level of 0 would produce `hi bye`.

A summary level of 1 would produce `hi bye` as both `hi` and `bye` have importance levels equal to or greater than 1.

But, when you input a summary level of 2, the output would be `bye` as the word `hi` has a summary level of less than 2.

And anything higher than 2 will make nothing.

## Examples
------
 - \`hi\`\`\`bye\`\`hi again

    This would have: `hi` with an importance level of 1, `bye` with an importance level of 2, and `hi again` with an importance level of 0.

    So if you asked for a summary level of 0, it would look like `hi bye hi again` and an importance level of 1 would look like `hi bye` and an importance level of 2 would look like `bye` and anything greater would be blank.

TODO: more examples.

## Warnings and FAQ
------
### About the stuff-ups about the spacings

The retokenizer means that the spacing will be stuffed up. This does not matter for a lot of things, TODO: make it not matter for more/all things, but if you find your text looks wonky, try something else.

So, no `:)`s. If you tried to input `hi :)` It will output `hi: )` instead. YOU HAVE BEEN WARNED!

### Why is my syntax not working?
TODO: make syntaxErrors to give them errors.
also TODO: finish this

### How high can the importance level be?
As high as the integer bit limit :D

But it is good practice to have the importance levels low. Like, 0-10 range.

Oh, and the lowest is 0. Ask for anything lower and it will look like it's 0.

### Why do you use `hi` and `bye` in your examples?
Because I can XD

You can use anything you want.
