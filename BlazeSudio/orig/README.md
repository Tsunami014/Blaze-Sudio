# How to use
- Compiled: `from BlazeSudio import something`
- Regular: `from BlazeSudio.orig import something`

To use the regular version (will be very very much slower), you need to have the debug version of the library installed. You can get this through 2 ways;
- Don't pip install it and just run code in the root directory (so the module is there) with the code freshly off of github
- Download the repo, `cd` into it's directory and then `pip install -e .`

Also try to replace every import with either one or the other. It'll probably crash out if you tried to combine stuff.
# TO BUILD THIS FOR YOUR DEVICE:
1. `pip install cython setuptools mypy`
2. `python3 BlazeSudio/orig/setup.py <folder you want to build>`
3. Wait for it to finish :)

## The auto builds
The code will manually be built into linux and windows for python versions 3.11+ each time I feel like it, but always before new releases if anything changed. Please do not build it yourself and make a PR, instead please contact me and I may/may not build it for you or add your version/distro/something to the auto build script :)

