# How to use
This contains the source code for the compiled modules.
To actually see this, you need to download the code off github and use that (or you can `pip install -e .` to use it with other code)

To use the regular version (will be very very much slower), run
```py
from BlazeSudio.orig import Debug
Debug(pkgname)
```
e.g. to debug the `graphicsCore` module you'd run `Debug('graphicsCore')`.

This MUST be run before any imports to that module.

# TO BUILD THIS FOR YOUR DEVICE
1. `pip install cython setuptools mypy`
2. `python3 BlazeSudio/orig/setup.py <folder you want to build>`
3. Wait for it to finish :)

## The auto builds
The code will manually be built into linux and windows for python versions 3.11+ each time I feel like it, but always before new releases if anything changed. Please do not build it yourself and make a PR, instead please contact me and I may/may not build it for you or add your version/distro/something to the auto build script :)

