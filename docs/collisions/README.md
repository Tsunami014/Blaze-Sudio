# The Collisions module
My pride and joy is this collisions module. It isn't finished yet, but next release it should be.

It contains many different classes and methods
## Classes
### `Shape`
The base class which all other shapes are derived from. Please do not use this in your actual code, it is quite useless. I mean, you *could* use it for making an infinite plane which always collides, but why?!?
### `NoShape`
The exact opposite of a Shape; this **never** collides with anything. This is useful if you performed an operation on something and it expects a Shape response, but the operation ended out giving nothing. Still, you should be mostly fine just using a `Shapes` object with no shapes in it.
### `Shapes`
// TODO: Finish