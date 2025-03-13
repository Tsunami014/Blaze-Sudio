# The graphics module
## Making a Graphic Screen
Ensure `from BlazeSudio.graphics import Screen` is present. To make a graphic screen you make a class:
```py
class Main(Screen):
    pass

Main()
```
This class shouldn't remain empty (or it would be a very boring screen), so let's add some functions to it!
### Functions
#### `_LoadUI(self)`
This is ran at the start of execution and whenever `self.Reload()` is ran. The code always clears the screen before running, so you don't need to include that here.

This function is where you typically create most of the GUI elements that will be present in the screen.

// TODO: Finish other functions

### Layers and stuff
To add elements to the screen, you need to add to the layers and stuff of the Screen. `self.layers` is the list of layers present in the screen. You start off with one layer `self.layers[0]`, but you can specify other layers (e.g. `self.layers[1]` or `self.layers[2]`) and it will automatically add them for you. Each element of `self.layers` is a `Stuff` element. How this works is you add categories to the `Stuff` and sort your elements into these categories. Then, all you need to do is to call `self['layername']` and it will automatically find the correct category for you!

Here is a clearer example:
```py
def _LoadUI(self):
    self.layers[0].add('Main') # Add category 'Main' to the Stuff on layer 0
    self.layers[1].add('MoreMain') # Create layer 1 and add category 'MoreMain' to it
    self['Main'].append(GUI.Text(GO.PCTOP, 'HI!')) # Add text saying 'HI!' to the top centre of the screen, putting it in the category 'Main' (which is on layer 0)
    self['MoreMain'].append(GUI.Text(GO.PCCENTER, 'Bye :(')) # Add text saying 'Bye :(' to the centre of the screen, putting it in the category 'MoreMain' (which is on layer 1)
```
Here is a JSON dictionary demonstrating the output of this:
```json
{
    "Layers": [
        { // This is Layers[0] (a stuff object)
            "Main": [ // This is a category in the layer 0 Stuff
                "GUI.Text(GO.PCTOP, 'HI!')" // This item is in category 'Main' of layer 0
            ]
        },
        { // This is Layers[1] (a stuff object)
            "MoreMain": [ // This is a category in the layer 1 Stuff
                "GUI.Text(GO.PCCENTER, 'Bye :(')" // This item is in category 'MoreMain' of layer 1
            ]
        }
    ]
}
```

#### THINGS TO NOTE ABOUT ORDER OF LAYERS
1. **The lower down (i.e. index closer to 0) the layer is, the *later* it will be rendered** (the layer with index 1 will be rendered before the layer of index 0)
2. If you have multiple categories with the same name;
    - If they are in the same layer making a new layer will override the existing layer
    - If they are in different layers specifying `self['layername']` will only find the category that is *lower down in the list* (e.g. if there was a 'Main' on layer 0 and 1 running `self['Main']` will return the list of the category from layer 0)
