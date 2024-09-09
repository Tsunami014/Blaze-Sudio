from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    packages = [i for i in fh.readlines() if i]

setup(
    name='Blaze-Sudio',
    version='2.4.0',
    license='Apache',
    description='This is the really cool game engine!',
    url='https://github.com/Tsunami014/Blaze-Sudio',
    download_url='https://github.com/Tsunami014/Blaze-Sudio/archive/refs/tags/v2.4.0-beta.tar.gz',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    package_data={'BlazeSudio' :['BlazeSudio/data/*', 'BlazeSudio/bot/preferencesDefault.json']},
    author='Tsunami014 (Max)',
    author_email='tsunami014@duck.com',
    install_requires=packages,
    keywords=['Python', 'games', 'engine'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Build Tools',
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows"
        # ~~No one~~ **I don't** like~~s~~ Apple
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
