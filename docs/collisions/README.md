# The Collisions module
The collisions module is one of the major parts of this library. It may never get fully finished, as there are **SO MANY** features I would like to add that I may never get to, but the basics are pretty well completed.

It has support for Shapely for more advanced mathy logic I lacked the pacience to add, *but anything that uses an external library will say so, and all the Shape classes do not use any external libraries for any of their functions, I hand made them all.*

Also, **one of the most common mistakes I make is forgetting whether functions input/output in radians or degrees, make sure to double check you are inputting to/using the output of the functions correctly!!!**

# Classes
## `Shape`
The base class which all other shapes are derived from. Please do not use this in your actual code, it is quite useless. I mean, you *could* use it for making an infinite plane which always collides, but why?!?
### `NoShape`
The exact opposite of a Shape; this **never** collides with anything. This is useful if you performed an operation on something and it expects a Shape response, but the operation ended out giving nothing. Still, you should be mostly fine just using a `Shapes` object with no shapes in it.
## `Shapes`
// TODO: Finish