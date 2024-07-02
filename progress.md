# Roadmap
## Current version (2.2.0-beta)
 - [ ] Structure code to be how I want it so you can make a game! Somewhat! [See this](#new-idea)
## 2.3.0-beta
 - [ ] Fix documentation
 - [ ] Make all the demos work (add some, remove others)
 - [ ] Figure out whether we even *need* `__main__.py` or the node editor
 - [ ] Make `__main__.py` work again!
 - [x] Make cross-platform
## 2.4.0-beta
 - [ ] Make graphics run WAY faster and **efficient** (currently EXTREMLY SLOW)
 - [ ] Overhaul of `terrainGen.py` to remove most of the dependancies, making there less things to install and also load WAYYY faster.
 - [ ] Make `loading.py` MUCH faster (can rewrite it if you want, just need to also update `graphics.py`)
 - [ ] Make the graphics faster to make elements
 - [ ] Fix import system to make things load faster
 - [ ] Make progressbars load stuff in the background for faster launching of the app
## 2.5.0-beta
 - [ ] Add more elements
 - [ ] Add some pretty <u>G</u>UI made by my lovelly pixelarting
## 2.6.0-beta
 - [ ] Make multiple different terrain gens for some fast and some slow generation!
## When I get to next major version after that: 3.0.0
 - When I can make a game that I feel like I can submit to a game jam or something
 - May take way longer than it should to make the game, that's for versions following to fix
 - May also not be the next Mario either

# Important todos to do at some point
 - [ ] Add optional requirements ([example](https://github.com/xtekky/gpt4free/blob/main/setup.py))
 - [ ] Remove all the AI stuff and instead use my AIHub I also made to make it easier and in a different package
 - [ ] Add type annotations

# What I'm working on:

Stages of production (SOP):
 1. just an idea at the moment
 2. early stages
 3. in progress, you can test it out
 4. finished, but more features/stuff coming soon
 5. finished, probably only going to get an update once every blue moon

Testable things can be tested from the demos in `__main__.py` or from `demos.py`

| What is it | Stage of production (SOP) | Testable? | My rating on how well I did at it /5 |
|:----------:|:-------------------------:|:---------:|:---------:|
| Node stuff | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ✔️ | 🌟🌟🌟🌟🌟 |
| Graphics | ![Finished, more features soon](https://badgen.net/badge/Production/4?color=green) | ✔️ | 🌟🌟🌟🌟🌟 |
| World/terrain generation | ![Finished, more features soon](https://badgen.net/badge/Production/4?color=green) | ✔️ | 🌟🌟🌟⭐ |
| AIs | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ✔️ | 🌟🌟🌟⭐ |
| Conversation Parse | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ✔️ | 🌟🌟🌟🌟🌟 |
| Main code | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ✔️ | 🌟🌟🌟⭐ |
| Speech-To-Text | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ❌ | TBD |
| Image generator | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ❌ | TBD |
| Music generator | ![Idea](https://badgen.net/badge/Production/1?color=pink) | ❌ | TBD |
| GUI | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ❌ | TBD |
| Overlay windows | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ✔️ | 🌟🌟🌟⭐ |
| LDtk integration | ![Early Stages](https://badgen.net/badge/Production/2?color=orange) | ❌ | TBD |
| A nice clean Github repo | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | N/A | 🌟🌟🌟⭐ |

# ![Ideas](https://badgen.net/badge/%20/Ideas?color=pink&label=)
 - Hyperanalysis Drive (also known as Qibli Simulator); Track player's every move to feed into an algorithm for personalised gameplay
 - OFTEN (Old Fashioned Times Engineering Nuiances) (Acronym subject to change); Try to make a game with old fashioned hardware! Makes making a game much harder, the result much worse, but it just shows you how hard it was back then, and it'll be such a cool feat too!

# new-idea
Instead of a `__main__.py` and the node editor (maybe keep the node editor), have it so this acts fully and soley as a library

Example idea:
```py
import BlazeSudio as BS
Game = BS.Game()
Game.load_map("./game.ldtk")

NPCS = BS.Character("Generic NPC", specific=False) # Every NPC in the game not specified otherwise

@NPCS.chat
def chat(npc):
    return "Hello! I am " + npc.name

Wizard = BS.Character("Wizard", id="ID of this guy in LDTK") # This specific NPC
@Wizard.chat
def chat():
    Game.run_action("unlock", "cave")
    return "I'm a wizard. Have a nice day!"

@Game.event("unlock")
def unlocks(thing):
    Game.dialog("You have unlocked " + thing)


if __name__ == '__main__':
    # Game.?????() # Launches Blaze Sudios and analyses the game and stuff and the LDTK file and shows you all the
                # Objects, events, etc. in the game so you can easily define them and it will suggest you code or something (?)
    # Game.debug() # Debugs the game
    Game.play()
```