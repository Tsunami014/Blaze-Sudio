import sys
import os

def is_synced():
    return 'run_sync' in sys.argv

def explanation():
    return """HOW TO USE:
In LDtk, in 'Project settings', you can add custom commands. Make a new one, specify when you want to run it, and use the command below - then you should be all set!

To find the command used to sync, find the path to your global interpreter (on at least Linux you can run "which python3"), but \
it is EXTREMELY HIGHLY RECOMMENDED to use a virtual environment and make a local path so others can't see your file system structure.
\
i.e. instead of C:/Users/Bob/AppData/Roaming/python/python3.12.3/bin/python3, ../../.venv/bin/python3.
\
If you are here because the script isn\'t working, you either did it wrong or someone else did it for their file system and you'll have to do this yourself. \
Please also *try* not to commit it. If you need any help remember to reach out on Discord.
"""

def generate_sync_code(file, fromdir):
    return f"""Once you've found your python interpreter path, put this command in LDtk:
path/to/python/env {file} run_sync
And if you need help here is (roughly) the script this thinks you'll need: (don't rely on it, but at least try it)
{os.path.relpath(sys.executable, fromdir)} {file} run_sync"""
    #return f'{os.path.relpath(sys.executable, fromdir)} {file} run_sync'
    #return f'cd "{basedir}";{sys.executable} "{file}" run_sync'
