import sys, os

def is_synced():
    return 'run_sync' in sys.argv

def explanation():
    return "HOW TO USE:\nIn LDtk, in 'Project settings', you can add custom commands. Make a new one, specify when you want to run it, and use the command below - then you should be all set!"

def generate_sync_code(file, fromdir):
    return f'{os.path.relpath(sys.executable, fromdir)} {file} run_sync'
    #return f'cd "{basedir}";{sys.executable} "{file}" run_sync'
