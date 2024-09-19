from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()
    long_description = re.sub(re.escape('<!-- Pypi ignore -->')+'.*'+re.escape('<!-- End Pypi ignore -->'), '', long_description)

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    packages = [i for i in fh.readlines() if i]

setup(
    name='Blaze-Sudio',
    version='3.0.1',
    license='Apache',
    description='This is the really cool game engine!',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    download_url='https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v3.0.1.tar.gz',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={'BlazeSudio' :['BlazeSudio/data/*'], 'BlazeSudio.collisions': ['**/*.so', '**/*.pyd']},
    author='Tsunami014 (Max)',
    author_email='tsunami014@duck.com',
    install_requires=packages,
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
