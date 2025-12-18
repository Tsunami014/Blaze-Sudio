from stubgen_pyx.stubgen import stubgen
import sys
import os

if '-h' in sys.argv or '--help' in sys.argv or len(sys.argv) > 1:
    print("Usage: "+sys.argv[0]+" [-h/--help] [--force/-f]")
    exit()

os.chdir(os.path.abspath(__file__+"/../../../"))
sys.path.append(os.getcwd())
import BlazeSudio.speed
BlazeSudio.speed._COMPILING = True

MODULES = []

base = "./BlazeSudio"

for root, dirs, files in os.walk(base):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, base).replace(os.sep, '/')
        if f.endswith('.pyx'):
            MODULES.append(rel_path[:-4])

print(f"Found modules: {MODULES}")


if len(MODULES) > 0:
    print("Compiling files...")
    forced = '-f' in sys.argv or '--force' in sys.argv
    def up2date(src, dst):
        if not os.path.exists(dst):
            return False
        return os.path.getmtime(src) < os.path.getmtime(dst)

    for name in MODULES:
        src = f"{base}/{name}.pyx"
        dst = f"{base}/{name}.pyi"
        if (not forced) and up2date(src, dst):
            print(f"File up-to-date: {name}")
            continue

        print(f"Compiling {name}...")
        # This also compiles it too for whatever reason
        stubgen(
            src,
            define_macros=[("Py_LIMITED_API", "0x030B0000")],
            py_limited_api=True
        )
else:
    print("No compile modules found!")


print("Finished!")

