import os, shutil

os.mkdir("temp")
os.chdir(os.path.join(os.getcwd() + "/temp"))
os.system("git clone https://github.com/Tsunami014/Blaze-Sudio.git")
print("Removing unnececary folders for installation")
shutil.rmtree("Blaze-Sudio/utils")
shutil.rmtree("Blaze-Sudio/elementgen")

os.chdir(os.path.join(os.getcwd(), "Blaze-Sudio", "graphics"))
shutil.move("setup.py", "./../setup.py")
os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..")))
os.system("pip install .")
os.chdir(os.path.abspath(os.path.join(os.getcwd(), "..", "..")))

print('Recursively deleting all temporary files that we don\'t need anymore...')
while os.path.exists("temp"):
    try:
        shutil.rmtree("temp")
    except Exception as e:
        os.chmod(e.filename, 0o777)
print("Done!")
