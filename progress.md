# Roadmap

TOFILLIN

# What I'm working on:

Stages of production (SOP):
 1. just an idea at the moment
 2. early stages
 3. in progress, you can test it out
 4. finished, but more features/stuff coming soon
 5. finished, probably only going to get an update once every blue moon

| What is it | Stage of production (SOP) | Testable? | My rating on how well I did at it /5 |
|:----------:|:-------------------------:|:---------:|:---------:|
| Node stuff | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟🌟🌟 |
| Graphics | ![Finished, more features soon](https://badgen.net/badge/Production/4?color=green) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟🌟🌟 |
| World/terrain generation | ![Finished, more features soon](https://badgen.net/badge/Production/4?color=green) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟⭐ |
| AIs | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟⭐ |
| Conversation Parse | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟🌟🌟 |
| Main code | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ![__main\_\_.py:Testable!](https://badgen.net/badge/__main__.py/Testable!?color=green) | 🌟🌟🌟⭐ |
| API Keys interface (I don't think I need it, so I'll probably delete it at some point) | ![Finished](https://badgen.net/badge/Production/5?color=blue) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) (files are in `keys` directory, I moved it in there so it doesn't work yet) | ⭐ |
| Speech-To-Text | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |
| Image generator | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |
| Music generator | ![Idea](https://badgen.net/badge/Production/1?color=pink) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |
| GUI | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |
| Overlay windows | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ![demos.py:Testable!](https://badgen.net/badge/demos.py/Testable!?color=green) | 🌟🌟🌟⭐ |
| LDtk integration | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |
| A nice clean Github repo | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | N/A | 🌟🌟🌟⭐ |
| Hyperanalysis Drive (also known as Qibli Simulator) | ![Idea](https://badgen.net/badge/Production/1?color=pink) | ![Not testable](https://badgen.net/badge/%20/Not%20testable?color=red) | TBD |

# IMPORTANT TODOS
We use a todo in front of everything so my parser can pick it up and yell at me about them
## STUFF THAT VERY MUCH NEEDS DOING
TODO: Make this readme nicer (i.e. table of contents, nice headers, etc.)
TODO: Move entire thing into one folder (so you pip install Blaze-sudio and then import blaze-sudios)
TODO: After that add optional requirements ([example](https://github.com/xtekky/gpt4free/blob/main/setup.py))
TODO: Add type annotations
TODO: possibly remove some of the libraries that come built in (like the one that's broken and I replaced it's main purpose) (see `demos.py`'s `GOtherGraphicsDemo`)
TODO: Make the Graphics decorator able to be called to do things (see graphics.options)
TODO: Make graphics run WAY faster (currently EXTREMLY SLOW)
## STUFF I'M DOING AT SOME POINT THAT ISN'T AS URGENT AS ABOVE
TODO: Make the buttons in the LDTK window do something
TODO: Make `loading.py` MUCH better (can rewrite it if you want, just need to also update `graphics.py`)
TODO: remove UIPack and wait for me to finish my one
Make GO.PNEW easier (e.g. have GO.P___ all have their functions in them and stuff so you don't need GO.PSTACKS)
