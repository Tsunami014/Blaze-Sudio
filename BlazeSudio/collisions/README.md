TO BUILD THIS FOR YOUR DEVICE:
1. `pip install cython setuptools`
2. Make sure you can run the `stubgen` command. On Linux, you need to `sudo apt install mypy`. On any other OS, I have no clue what you need to do, you're on your own.
3. `cd BlazeSudio/collisions/`
4. `python3 setup.py build_ext --inplace`
5. Wait for it to finish :)

```bash
cd BlazeSudio/collisions/
python3 setup.py build_ext --inplace
```

PLEASE NOTE: If you are using precompiled ones I may have forgotten to compile them and they may be behind. Just sayin', thass all...

# How to use
Regular: `from BlazeSudio import collisions`

To debug (will probably be very very much slower): `from BlazeSudio.collisions.lib import collisions`

// TODO: Compile for Windows and Linux at the same time