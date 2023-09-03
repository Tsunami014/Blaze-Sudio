# Welcome to 🎇 Spark Sudios!
(purposeful typo, if you wanted to know - for all of those whos `t` key is broken :D)

Things to note:
1. still in progress
3. This is probably my best formed git repo I've ever made :)
4. *Some* of the code was AI generated. Please do not kill me for that.
5. This project comes with 2 python libraries built into it, [pyguix](https://github.com/DarthData410/PyGames-pyguix) and [textboxify](https://github.com/hnrkcode/TextBoxify/tree/master). This is for a couple of reasons:
    1. (the main big one) It can't be installed with pip (maybe it got taken down? I don't know)
    2. I don't have to wory about dependancy issues with those two packages
    3. I can modify it myself
    4. You guys don't have to install another package

# How to install
```bash
pip install -r requirements.txt
```

If you're getting an error that says 'nltk package punkt not found', try this:
```bash
python -c "import nltk;nltk.download('punkt')"
```
And if it says python is not a valid command, check if python is installed, and if it is, check if typing `python3` or `py` instead of `python` works. If not search it up.

And if nltk is giving you odd errors that are not what is listed above, run this:
```bash
pip install -U nltk
```
and if pip gives you errors try this:
```bash
python -m pip install nltk
```
and if it says python is not a valid command, try the steps listed above.

## Next versions coming soon:
 - v1.0.0 - 🟠`Ember Sudio` - all main AI functionality complete!
 - v2.0.0 - 🧨`Flare Sudio` - got a world and storyline!
 - v3.0.0 - 🧯`Fire Sudio` - cos by then it'll be on fire :grin: - all functionality complete!
 - v4.0.0 - 🔥`Blaze Sudio` - Unity integration!
