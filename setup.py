from setuptools import setup, find_packages
import codecs
import os
import re
import sys

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = re.sub(re.escape('<!-- Pypi ignore -->')+'.*?'+re.escape('<!-- End Pypi ignore -->'), '', long_description)

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    installPackages = [i for i in fh.readlines() if ((not i.startswith('#')) and i)]

# Check if 'debug' is in the extras
if any('debug' in arg for arg in sys.argv):
    packages = find_packages()
else:
    packages = find_packages(exclude=('BlazeSudio.collisions.lib', 'BlazeSudio.debug'))

setup(
    name='Blaze-Sudio',
    version='3.1.0',
    license='Apache',
    description='This is the really cool game engine!',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    download_url='https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v3.1.0.tar.gz',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=packages,
    include_package_data=True,
    package_data={'BlazeSudio': [
        'elementGen/nodes/*.py', 
        'ldtk/internal-icons.png',
        'graphics/defaultTheme/*',
        'graphics/GUI/textboxify/data/**'
    ], 'BlazeSudio.collisions': ['**/*.so', '**/*.pyd']},
    author='Tsunami014',
    author_email='tsunami014@duck.com',
    install_requires=installPackages,
    keywords=['Python', 'games', 'engine'],
    scripts=['BlazeSudio/BlazeSudio'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Build Tools',
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows"
        # ~~No one~~ **I don't** like Apple
    ]
)

# Development Status options: 
# 1 - Planning
# 2 - Pre-Alpha
# 3 - Alpha
# 4 - Beta
# 5 - Production/Stable
# 6 - Mature
# 7 - Inactive
