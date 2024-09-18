# TO BUILD THIS FOR YOUR DEVICE:
1. `pip install cython setuptools`
2. Make sure you can run the `stubgen` command. On Linux, you need to `sudo apt install mypy`. On any other OS, I have no clue what you need to do, you're on your own.
3. `cd BlazeSudio/collisions/`
4. `python3 setup.py build_ext --inplace`
5. Wait for it to finish :)

```bash
cd BlazeSudio/collisions/
python3 setup.py build_ext --inplace
```

## The auto builds
The code will manually be built into linux and windows for python versions 3.10 to 3.12 each release (if anything changes). Please do not build it yourself and make a PR, as when I change something it won't be built. Instead please contact me on discord and I may/may not add your version/distro/something to the auto build script :)

PLEASE NOTE: If you are using precompiled ones I may have forgotten to compile them and they may be behind. Just sayin', thass all...

BUT if you are using the main release I *should* have compiled everything for you.

# How to use
Regular: `from BlazeSudio import collisions`

To debug (will probably be very very much slower): `from BlazeSudio.collisions.lib import collisions`
