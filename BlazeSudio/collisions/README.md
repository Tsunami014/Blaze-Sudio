# How to use
Regular: `from BlazeSudio import collisions`

To debug (will be very very much slower): `from BlazeSudio.debug import collisions`. **BUT** this means you need to have the debug version of the library installed. You can get this through 2 ways; don't pip install it and just run code in the root directory (so the module is there) with the code freshly off of github, or you can download the repo, `cd` into it's directory and then `pip install .[debug]`.

Also with the debug statement it *will* get **very** annoyed at you if you have half your code using the regular and the other half with the debug. It *can* tell the difference between the two and will not rest until they are the same, causing an infinite loop. And, once you run the debug it will keep using the debug. So, please have the debug at the top of your main file, no matter even if you don't want to use it.
# TO BUILD THIS FOR YOUR DEVICE:
1. `pip install cython setuptools`
2. Make sure you can run the `stubgen` command. On Linux, you need to `sudo apt install mypy`. On any other OS, I have no clue what you need to do, you're on your own. Check if it's installed first before complaining tho.
3. `cd BlazeSudio/collisions/`
4. `python3 setup.py build_ext --inplace`
5. Wait for it to finish :)

```bash
cd BlazeSudio/collisions/
python3 setup.py build_ext --inplace
```

## The auto builds
The code will manually be built into linux and windows for python versions 3.10 to 3.12 each time I feel like it, but always before new releases if anything changes. Please do not build it yourself and make a PR, as when I change something it won't be built. Instead please contact me on discord and I may/may not add your version/distro/something to the auto build script :)

Or if you edited something then you can ask me and I'll re-run it for you.

PLEASE NOTE: If you are using precompiled versions then I may have not compiled them and they may be behind. This is *only* if you build from source, and not from a release. Just sayin', thass all...

BUT if you are using the main release I *should* have compiled everything for you.
