Welcome to AIHub! This is where you can use any AIs you want!

Things to note:
1. still in progress
2. someone please find a good name (e.g. android made 'nougat' and 'eclare' and whatnot, and Adobe made Firefly, so please someone find a good name for this)
3. This is probably my best formed git repo I've ever made :)
4. *Some* of the code was AI generated. Please do not kill me for that.
5. This project comes with 2 python libraries built into it, [pyguix](https://github.com/DarthData410/PyGames-pyguix) and [textboxify](https://github.com/hnrkcode/TextBoxify/tree/master). This is for a couple of reasons:
    1. (the main big one) It can't be installed with pip (maybe it got taken down? I don't know)
    2. I don't have to wory about dependancy issues with those two packages (lame, but still, you must admit it's a good reason)
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
