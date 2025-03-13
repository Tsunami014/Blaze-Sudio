# Roadmap
 - [ ] Use `multiprocessing` instead of `threading`
 - [ ] Finish theme editor
 - [ ] Finish texture editor
 - [ ] Procedural generation testing area?
 - [ ] Finish Music/SFX editor/generator
 - [ ] Fix pyldtk (add type hints & make it work more)
 - Keep adding more features to the main editor, allthewhile doing the below:
 - [ ] Fix documentation
 - [ ] Overhaul of `terrainGen.py` to remove most of the dependencies, making there less things to install and also load WAYYY faster.
 - [ ] Add more elements
 - [ ] Add type annotations to EVERYTHING

# What I'm (not really) working on:

Stages of production (SOP):
 1. ![Just an idea](https://badgen.net/badge/Just%20an/IDEA?color=pink)
 2. ![Early stage of development](https://badgen.net/badge/-/Early%20stage%20of%20dev?color=orange&label=)
 3. ![In progress](https://badgen.net/badge/In/PROGRESS?color=yellow)
 4. ![Finished but still being developed/improved](https://badgen.net/badge/FINISHED%20but%20still/being%20developed?color=green)
 5. ![Finished, probably won't touch it again](https://badgen.net/badge/FINISHED,/probably%20won't%20recieve%20updates?color=blue)

Testable things can be tested from the demos in `__main__.py` or from `demos.py`

| What is it | Stage of production (SOP) | Testable? | My rating on how well I did at it /5 |
|:----------:|:-------------------------:|:---------:|:---------:|
| Node stuff | ![In Progress](https://badgen.net/badge/Production/3?color=yellow) | ✔️ | 🌟🌟🌟⭐ |
| Graphics | ![Finished, more features soon](https://badgen.net/badge/Production/4?color=green) | ✔️ | 🌟🌟🌟🌟🌟🌟 |
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

# ![Ideas](https://badgen.net/badge/-/Ideas?color=pink&label=&scale=3)
 - Hyperanalysis Drive (also known as Qibli Simulator); Track player's every move to feed into an algorithm for personalised gameplay
 - OFTEN (Old Fashioned Times Engineering Nuiances) (Acronym subject to change); Try to make a game with old fashioned hardware! Makes making a game much harder, the result much worse, but it just shows you how hard it was back then, and it'll be such a cool feat too!

# idea-for-main
You can make a game using the python library, OR alternatively have a main file which opens an LDtk file and it does the same thing EXCEPT it *generates* the python file for you based off of some things you set

Like, it's another way to open an LDtk file; you can either open it to edit or open it to make a game with.

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