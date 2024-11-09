# How to install

1. Run `pip install Blaze-Sudio[all]`. Done. Wasn't that hard, was it? Or was it? If there was an error please tell me about it by [making a new issue](https://github.com/Tsunami014/Blaze-Sudio/issues) or [joining Discord](https://discord.gg/xr3phyEZtv) and hopefully I'll be onto it soon enough.

## Optional requirements
You don't need to install *everything*, so here is a list of all the optional requirements and what they do:
- `Blaze-Sudio[all]` - Installs all of the below.
- `Blaze-Sudio[game]` - Installs the required dependencies for the **game, graphics & collisions** module (everything you need to make a game with).
- `Blaze-Sudio[collisions]` - Installs the required dependencies for the **collisions** module.
- `Blaze-Sudio[image]` - Installs the required dependencies for the **element Gen** module.
- `Blaze-Sudio[graphics]` - Installs the required dependencies for the **graphics** module.

You can also install multiple of these at a time like so: `pip install Blaze-Sudio[game,collisions]`.

# How to install the long hard way
This is not recommended. It gets the latest release, which if you get it at the wrong time may be the time where I committed 'was half way through majorly rewriting the code and it's all broken'. So be careful.
1. Download via git using one of the below methods:
    - Run in the terminal:
    ```bash
    git clone https://github.com/Tsunami014/Blaze-Sudio.git
    ```
    - Go to [the website](https://github.com/Tsunami014/Blaze-Sudio/) and download the repo as a zip file then unzip it.
2.  Grab your favourite terminal and navigate into the folder (if you used the first option of git cloning, you can just `cd Blaze-Sudio`), then run;
    ```bash
    pip install .
    ```
You may have to modify some of them to be suited for *your* specific python (i.e. some may need to use `pip3` instead of `pip`, or `python3 -m pip`, or whatever).

Here is the commands alltogether (copy paste them into the terminal):
```bash
git clone https://github.com/Tsunami014/Blaze-Sudio.git
cd Blaze-Sudio
pip install .
```
