Welcome to AIHub! This is where you can use any AIs you want!
1. still in progress
2. someone please find a good name (e.g. android made 'nougat' and 'eclare' and whatnot, and Adobe made Firefly, so please someone find a good name for this)

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
